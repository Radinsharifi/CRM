from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, TemplateView, DetailView, UpdateView, View
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Customer, CallRecord

def visible_customers(user):
    if user.is_superuser:
        return Customer.objects.all()
    return Customer.objects.filter(created_by=user)


def visible_calls(user):
    if user.is_superuser:
        return CallRecord.objects.all()
    return CallRecord.objects.filter(created_by=user)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'marketing/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        calls = visible_calls(self.request.user)
        context['total_customers'] = visible_customers(self.request.user).count()
        context['calls_today_count'] = calls.filter(created_at__date=today).count()
        context['pending_followups'] = calls.filter(follow_up_date=today).count()
        context['recent_calls'] = calls.select_related('customer')[:5]
        return context

# --- CUSTOMER PAGES ---
class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'marketing/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        customers = visible_customers(self.request.user)
        category_id = self.request.GET.get('category')
        if category_id:
            customers = customers.filter(category_id=category_id)
        return customers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
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
    fields = [
        'company_name', 'full_name', 'category', 'phone_number', 'email',
        'field_of_activity', 'job_title', 'landline', 'mobile',
        'website', 'acquisition_source'
    ]
    success_url = reverse_lazy('marketing:customer_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'marketing/customer_form.html'
    fields = CustomerCreateView.fields
    success_url = reverse_lazy('marketing:customer_list')

    def get_queryset(self):
        return visible_customers(self.request.user)

# --- CALL RECORD PAGES ---
class CallListView(LoginRequiredMixin, ListView):
    model = CallRecord
    template_name = 'marketing/call_list.html'
    context_object_name = 'calls'

    def get_queryset(self):
        return visible_calls(self.request.user)

class CallDetailView(LoginRequiredMixin, DetailView):
    model = CallRecord
    template_name = 'marketing/call_detail.html'

    def get_queryset(self):
        return visible_calls(self.request.user)

class CallCreateView(LoginRequiredMixin, CreateView):
    model = CallRecord
    template_name = 'marketing/call_form.html'
    fields = [
        'customer', 'result', 'duration_minutes', 'notes', 'follow_up_date'
    ]
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
    fields = CallCreateView.fields
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
            Customer.objects.create(
                company_name=company,
                full_name=full_name,
                phone_number=phone or '',
                created_by=request.user
            )
            # Redirect back to the call add page
            return redirect('marketing:call_create')
        return redirect('marketing:call_create')