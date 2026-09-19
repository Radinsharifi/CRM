from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, TemplateView, DetailView, UpdateView, View
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CallRecordForm, CallReminderForm, CustomerForm, TomorrowTaskForm
from .models import Category, CallRecord, CallReminder, Customer, TomorrowTask

def visible_customers(user):
    if user.is_superuser:
        return Customer.objects.all()
    return Customer.objects.filter(created_by=user)


def visible_calls(user):
    if user.is_superuser:
        return CallRecord.objects.all()
    return CallRecord.objects.filter(created_by=user)


def visible_reminders(user):
    if user.is_superuser:
        return CallReminder.objects.all()
    return CallReminder.objects.filter(created_by=user)


def visible_tomorrow_tasks(user):
    if user.is_superuser:
        return TomorrowTask.objects.all()
    return TomorrowTask.objects.filter(created_by=user)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'marketing/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        calls = visible_calls(self.request.user)
        reminders = visible_reminders(self.request.user)
        tomorrow_tasks = visible_tomorrow_tasks(self.request.user)
        context['total_customers'] = visible_customers(self.request.user).count()
        context['calls_today_count'] = calls.filter(created_at__date=today).count()
        context['pending_followups'] = calls.filter(follow_up_date=today).count()
        context['reminders_count'] = reminders.count()
        context['open_tomorrow_tasks_count'] = tomorrow_tasks.filter(is_completed=False).count()
        context['recent_calls'] = calls.select_related('customer')[:5]
        recent_activities = []
        for call in calls.select_related('customer')[:5]:
            recent_activities.append({
                'title': 'ثبت تماس با',
                'customer': call.customer.company_name,
                'description': f'نتیجه: {call.result}',
                'created_at': call.created_at,
                'created_by': call.created_by.get_full_name() if call.created_by else 'ثبت نشده',
                'url': reverse_lazy('marketing:call_detail', kwargs={'pk': call.pk}),
                'icon': 'call',
            })
        for reminder in reminders.select_related('customer')[:5]:
            recent_activities.append({
                'title': 'ثبت یادآوری برای',
                'customer': reminder.customer.company_name,
                'description': reminder.subject,
                'created_at': reminder.created_at,
                'created_by': reminder.created_by.get_full_name() if reminder.created_by else 'ثبت نشده',
                'url': reverse_lazy('marketing:reminder_detail', kwargs={'pk': reminder.pk}),
                'icon': 'reminder',
            })
        for task in tomorrow_tasks.prefetch_related(
            'new_customer_follow_ups', 'existing_customer_follow_ups'
        )[:5]:
            customers = list(task.new_customer_follow_ups.all()) + list(task.existing_customer_follow_ups.all())
            recent_activities.append({
                'title': 'ثبت کار پیگیری برای',
                'customer': ', '.join(customer.company_name for customer in customers) or 'پیگیری‌های متنی',
                'description': task.rate_inquiry_follow_ups or task.bill_of_lading_follow_ups or 'کار فردا',
                'created_at': task.created_at,
                'created_by': task.created_by.get_full_name() if task.created_by else 'ثبت نشده',
                'url': reverse_lazy('marketing:tomorrow_task_detail', kwargs={'pk': task.pk}),
                'icon': 'task',
            })
        context['recent_activities'] = sorted(
            recent_activities,
            key=lambda activity: activity['created_at'],
            reverse=True
        )[:5]
        return context

# --- CUSTOMER PAGES ---
class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'marketing/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        customers = visible_customers(self.request.user).order_by('-created_at')
        category_id = self.request.GET.get('category')
        company_name = self.request.GET.get('company_name', '').strip()
        if category_id:
            customers = customers.filter(category_id=category_id)
        if company_name:
            customers = customers.filter(company_name__icontains=company_name)
        return customers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['company_name_query'] = self.request.GET.get('company_name', '')
        return context

class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'marketing/customer_detail.html'

    def get_queryset(self):
        return visible_customers(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['call_history'] = visible_calls(self.request.user).filter(
            customer=self.object
        ).order_by('-created_at')
        return context

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'marketing/customer_form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('marketing:customer_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'marketing/customer_form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('marketing:customer_list')

    def get_queryset(self):
        return visible_customers(self.request.user)

# --- CALL RECORD PAGES ---
class CallsHubView(LoginRequiredMixin, TemplateView):
    template_name = 'marketing/calls_hub.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        context['calls_count'] = visible_calls(self.request.user).count()
        context['today_calls_count'] = visible_calls(self.request.user).filter(created_at__date=today).count()
        reminders = visible_reminders(self.request.user)
        context['reminders_count'] = reminders.count()
        context['today_reminders_count'] = reminders.filter(follow_up_date=today).count()
        context['tomorrow_tasks_count'] = visible_tomorrow_tasks(self.request.user).filter(is_completed=False).count()
        return context


class CallListView(LoginRequiredMixin, ListView):
    model = CallRecord
    template_name = 'marketing/call_list.html'
    context_object_name = 'calls'
    paginate_by = 10

    def get_queryset(self):
        calls = visible_calls(self.request.user)
        if self.request.GET.get('today') == '1':
            calls = calls.filter(created_at__date=timezone.localdate())
        return calls

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today_only'] = self.request.GET.get('today') == '1'
        return context

class CallDetailView(LoginRequiredMixin, DetailView):
    model = CallRecord
    template_name = 'marketing/call_detail.html'

    def get_queryset(self):
        return visible_calls(self.request.user)

class CallCreateView(LoginRequiredMixin, CreateView):
    model = CallRecord
    template_name = 'marketing/call_form.html'
    form_class = CallRecordForm
    success_url = reverse_lazy('marketing:call_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['customer'].queryset = visible_customers(self.request.user)
        return form
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CallUpdateView(LoginRequiredMixin, UpdateView):
    model = CallRecord
    template_name = 'marketing/call_form.html'
    form_class = CallRecordForm
    success_url = reverse_lazy('marketing:call_list')

    def get_queryset(self):
        return visible_calls(self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['customer'].queryset = visible_customers(self.request.user)
        return form


class CallDeleteView(LoginRequiredMixin, DeleteView):
    model = CallRecord
    template_name = 'marketing/call_confirm_delete.html'
    success_url = reverse_lazy('marketing:call_list')

    def get_queryset(self):
        return visible_calls(self.request.user)


class ReminderListView(LoginRequiredMixin, ListView):
    model = CallReminder
    template_name = 'marketing/reminder_list.html'
    context_object_name = 'reminders'
    paginate_by = 10

    def get_queryset(self):
        return visible_reminders(self.request.user).select_related('customer', 'created_by')


class ReminderDetailView(LoginRequiredMixin, DetailView):
    model = CallReminder
    template_name = 'marketing/reminder_detail.html'

    def get_queryset(self):
        return visible_reminders(self.request.user).select_related('customer', 'created_by')


class ReminderCreateView(LoginRequiredMixin, CreateView):
    model = CallReminder
    form_class = CallReminderForm
    template_name = 'marketing/reminder_form.html'
    success_url = reverse_lazy('marketing:reminder_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['customer'].queryset = visible_customers(self.request.user)
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ReminderUpdateView(LoginRequiredMixin, UpdateView):
    model = CallReminder
    form_class = CallReminderForm
    template_name = 'marketing/reminder_form.html'
    success_url = reverse_lazy('marketing:reminder_list')

    def get_queryset(self):
        return visible_reminders(self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['customer'].queryset = visible_customers(self.request.user)
        return form


class ReminderDeleteView(LoginRequiredMixin, DeleteView):
    model = CallReminder
    template_name = 'marketing/reminder_confirm_delete.html'
    success_url = reverse_lazy('marketing:reminder_list')

    def get_queryset(self):
        return visible_reminders(self.request.user)


class TomorrowTaskListView(LoginRequiredMixin, ListView):
    model = TomorrowTask
    template_name = 'marketing/tomorrow_task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        return visible_tomorrow_tasks(self.request.user).prefetch_related(
            'new_customer_follow_ups', 'existing_customer_follow_ups'
        ).select_related('created_by')


class TomorrowTaskDetailView(LoginRequiredMixin, DetailView):
    model = TomorrowTask
    template_name = 'marketing/tomorrow_task_detail.html'

    def get_queryset(self):
        return visible_tomorrow_tasks(self.request.user).prefetch_related(
            'new_customer_follow_ups', 'existing_customer_follow_ups'
        ).select_related('created_by')


class TomorrowTaskCreateView(LoginRequiredMixin, CreateView):
    model = TomorrowTask
    form_class = TomorrowTaskForm
    template_name = 'marketing/tomorrow_task_form.html'
    success_url = reverse_lazy('marketing:tomorrow_task_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['new_customer_follow_ups'].queryset = visible_customers(self.request.user)
        form.fields['existing_customer_follow_ups'].queryset = visible_customers(self.request.user)
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TomorrowTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = TomorrowTask
    form_class = TomorrowTaskForm
    template_name = 'marketing/tomorrow_task_form.html'
    success_url = reverse_lazy('marketing:tomorrow_task_list')

    def get_queryset(self):
        return visible_tomorrow_tasks(self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['new_customer_follow_ups'].queryset = visible_customers(self.request.user)
        form.fields['existing_customer_follow_ups'].queryset = visible_customers(self.request.user)
        return form


class TomorrowTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = TomorrowTask
    template_name = 'marketing/tomorrow_task_confirm_delete.html'
    success_url = reverse_lazy('marketing:tomorrow_task_list')

    def get_queryset(self):
        return visible_tomorrow_tasks(self.request.user)


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'marketing/customer_confirm_delete.html'
    success_url = reverse_lazy('marketing:customer_list')

    def get_queryset(self):
        return visible_customers(self.request.user)
    
class QuickCustomerCreateView(LoginRequiredMixin, View):
    def post(self, request):
        company = request.POST.get('company_name')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone_number')
        
        if company and full_name:
            customer = Customer.objects.create(
                company_name=company,
                full_name=full_name,
                phone_number=phone or '',
                created_by=request.user
            )
            return_to = request.POST.get('return_to') or reverse_lazy('marketing:call_create')
            separator = '&' if '?' in str(return_to) else '?'
            return redirect(f'{return_to}{separator}customer_id={customer.pk}')
        return redirect(request.POST.get('return_to') or 'marketing:call_create')