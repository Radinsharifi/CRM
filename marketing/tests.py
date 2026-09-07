from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import CallRecord, Category, Customer


class OwnershipVisibilityTests(TestCase):
	def setUp(self):
		user_model = get_user_model()
		self.marketer = user_model.objects.create_user(
			username='marketer', password='password'
		)
		self.other_marketer = user_model.objects.create_user(
			username='other-marketer', password='password'
		)
		self.superuser = user_model.objects.create_superuser(
			username='admin', password='password', email='admin@example.com'
		)
		self.category = Category.objects.create(name='Enterprise')
		self.customer = Customer.objects.create(
			full_name='First Contact Full Name',
			company_name='First Company',
			category=self.category,
			phone_number='1111111111',
			created_by=self.marketer,
		)
		self.other_customer = Customer.objects.create(
			full_name='Second Contact Full Name',
			company_name='Second Company',
			phone_number='2222222222',
			created_by=self.other_marketer,
		)
		self.legacy_customer = Customer.objects.create(
			full_name='Legacy Contact Full Name',
			company_name='Legacy Company',
			phone_number='3333333333',
		)
		self.call = self._create_call(self.customer, self.marketer)
		self.other_call = self._create_call(self.other_customer, self.other_marketer)
		self.legacy_call = self._create_call(self.legacy_customer, None)

	def _create_call(self, customer, created_by):
		return CallRecord.objects.create(
			customer=customer,
			created_by=created_by,
			result='Successful',
			follow_up_date=timezone.localdate(),
		)

	def test_regular_user_sees_only_owned_customers(self):
		self.client.force_login(self.marketer)

		response = self.client.get(reverse('marketing:customer_list'))

		self.assertContains(response, 'First Company')
		self.assertNotContains(response, 'Second Company')
		self.assertNotContains(response, 'Legacy Company')
		self.assertEqual(
			self.client.get(
				reverse('marketing:customer_detail', args=[self.other_customer.pk])
			).status_code,
			404,
		)

	def test_call_form_contains_only_owned_customers_and_rejects_other_customer(self):
		self.client.force_login(self.marketer)

		response = self.client.get(reverse('marketing:call_create'))

		self.assertContains(response, 'First Company')
		self.assertNotContains(response, 'Second Company')
		self.assertNotContains(response, 'Legacy Company')

		response = self.client.post(
			reverse('marketing:call_create'),
			{
				'customer': self.other_customer.pk,
				'contact_person': 'Contact',
				'mobile': '09121111111',
				'result': 'Successful',
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(CallRecord.objects.count(), 3)

	def test_regular_user_sees_only_owned_calls_and_cannot_access_or_delete_other_call(self):
		self.client.force_login(self.marketer)

		response = self.client.get(reverse('marketing:call_list'))

		self.assertContains(response, 'First Company')
		self.assertNotContains(response, 'Second Company')
		self.assertNotContains(response, 'Legacy Company')
		self.assertEqual(
			self.client.get(
				reverse('marketing:call_detail', args=[self.other_call.pk])
			).status_code,
			404,
		)
		self.assertEqual(
			self.client.post(
				reverse('marketing:call_delete', args=[self.other_call.pk])
			).status_code,
			404,
		)
		self.assertTrue(CallRecord.objects.filter(pk=self.other_call.pk).exists())

	def test_dashboard_and_customer_history_are_scoped(self):
		self.client.force_login(self.marketer)

		dashboard = self.client.get(reverse('marketing:dashboard'))
		customer_detail = self.client.get(
			reverse('marketing:customer_detail', args=[self.customer.pk])
		)

		self.assertEqual(dashboard.context['total_customers'], 1)
		self.assertEqual(dashboard.context['calls_today_count'], 1)
		self.assertEqual(dashboard.context['pending_followups'], 1)
		self.assertEqual(list(dashboard.context['recent_calls']), [self.call])
		self.assertEqual(list(customer_detail.context['call_history']), [self.call])

	def test_customer_creation_paths_assign_authenticated_user(self):
		self.client.force_login(self.marketer)

		self.client.post(
			reverse('marketing:customer_create'),
			{
				'full_name': 'New Contact Full Name',
				'company_name': 'New Company',
				'phone_number': '4444444444',
			},
		)
		self.client.post(
			reverse('marketing:customer_create_js'),
			{
				'full_name': 'Quick Contact Full Name',
				'company_name': 'Quick Company',
				'phone_number': '5555555555',
			},
		)

		self.assertTrue(
			Customer.objects.filter(
				company_name='New Company', created_by=self.marketer
			).exists()
		)
		self.assertTrue(
			Customer.objects.filter(
				company_name='Quick Company', created_by=self.marketer
			).exists()
		)

	def test_superuser_sees_all_customers_calls_and_history(self):
		self.client.force_login(self.superuser)

		customers = self.client.get(reverse('marketing:customer_list'))
		calls = self.client.get(reverse('marketing:call_list'))
		dashboard = self.client.get(reverse('marketing:dashboard'))
		customer_detail = self.client.get(
			reverse('marketing:customer_detail', args=[self.customer.pk])
		)

		self.assertContains(customers, 'First Company')
		self.assertContains(customers, 'Second Company')
		self.assertContains(customers, 'Legacy Company')
		self.assertContains(calls, 'First Company')
		self.assertContains(calls, 'Second Company')
		self.assertContains(calls, 'Legacy Company')
		self.assertEqual(dashboard.context['total_customers'], 3)
		self.assertEqual(dashboard.context['calls_today_count'], 3)
		self.assertEqual(dashboard.context['pending_followups'], 3)
		self.assertEqual(
			list(customer_detail.context['call_history']), [self.call]
		)

	def test_owner_can_edit_customer_and_call_with_prefilled_data(self):
		self.client.force_login(self.marketer)

		customer_response = self.client.get(
			reverse('marketing:customer_update', args=[self.customer.pk])
		)
		call_response = self.client.get(
			reverse('marketing:call_update', args=[self.call.pk])
		)

		self.assertContains(customer_response, 'First Company')
		self.assertContains(customer_response, 'First Contact Full Name')
		self.assertContains(call_response, 'Successful')

	def test_owner_can_delete_customer_and_call(self):
		self.client.force_login(self.marketer)

		self.assertEqual(
			self.client.post(
				reverse('marketing:call_delete', args=[self.call.pk])
			).status_code,
			302,
		)
		self.assertFalse(CallRecord.objects.filter(pk=self.call.pk).exists())

		self.assertEqual(
			self.client.post(
				reverse('marketing:customer_delete', args=[self.customer.pk])
			).status_code,
			302,
		)
		self.assertFalse(Customer.objects.filter(pk=self.customer.pk).exists())

	def test_owner_cannot_edit_or_delete_other_users_records(self):
		self.client.force_login(self.marketer)

		self.assertEqual(
			self.client.get(
				reverse('marketing:customer_update', args=[self.other_customer.pk])
			).status_code,
			404,
		)
		self.assertEqual(
			self.client.get(
				reverse('marketing:call_update', args=[self.other_call.pk])
			).status_code,
			404,
		)
		self.assertEqual(
			self.client.post(
				reverse('marketing:customer_delete', args=[self.other_customer.pk])
			).status_code,
			404,
		)

	def test_customer_list_can_filter_by_category(self):
		self.client.force_login(self.marketer)

		response = self.client.get(
			reverse('marketing:customer_list'),
			{'category': self.category.pk},
		)

		self.assertContains(response, 'First Company')
		self.assertNotContains(response, 'Second Company')

	def test_call_duration_is_required_in_form_and_saved(self):
		self.client.force_login(self.marketer)

		missing_duration = self.client.post(
			reverse('marketing:call_create'),
			{'customer': self.customer.pk, 'result': 'No duration'},
		)
		self.assertEqual(missing_duration.status_code, 200)
		self.assertEqual(CallRecord.objects.count(), 3)

		created = self.client.post(
			reverse('marketing:call_create'),
			{
				'customer': self.customer.pk,
				'result': 'Timed call',
				'duration_minutes': 12,
				'follow_up_date': timezone.localdate().isoformat(),
			},
		)
		self.assertEqual(created.status_code, 302)
		self.assertTrue(
			CallRecord.objects.filter(
				customer=self.customer,
				result='Timed call',
				duration_minutes=12,
			).exists()
		)

# Create your tests here.
