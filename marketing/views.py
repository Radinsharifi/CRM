from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, TemplateView, DetailView, View
from django.utils import timezone
from django.shortcuts import redirect
from .models import Customer, CallRecord

class DashboardView(TemplateView):
    template_name = 'marketing/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['total_customers'] = Customer.objects.count()
        context['calls_today_count'] = CallRecord.objects.filter(created_at__date=today).count()
        context['pending_followups'] = CallRecord.objects.filter(follow_up_date=today).count()
        context['recent_calls'] = CallRecord.objects.select_related('customer').all()[:5]
        return context

# --- CUSTOMER PAGES ---
class CustomerListView(ListView):
    model = Customer
    template_name = 'marketing/customer_list.html'
    context_object_name = 'customers'

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'marketing/customer_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Show all history of calls for this customer
        context['call_history'] = self.object.calls.all().order_by('-created_at')
        return context

class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'marketing/customer_form.html'
    fields = ['name', 'company_name', 'phone_number', 'email']
    success_url = reverse_lazy('marketing:customer_list')

# --- CALL RECORD PAGES ---
class CallListView(ListView):
    model = CallRecord
    template_name = 'marketing/call_list.html'
    context_object_name = 'calls'

class CallDetailView(DetailView):
    model = CallRecord
    template_name = 'marketing/call_detail.html'

class CallCreateView(CreateView):
    model = CallRecord
    template_name = 'marketing/call_form.html'
    fields = [
        'customer', 'field_of_activity', 'contact_person', 'job_title', 
        'landline', 'mobile', 'email_at_call', 'website', 
        'acquisition_source', 'result', 'notes', 'follow_up_date'
    ]
    success_url = reverse_lazy('marketing:call_list')

class CallDeleteView(DeleteView):
    model = CallRecord
    template_name = 'marketing/call_confirm_delete.html'
    success_url = reverse_lazy('marketing:call_list')
    
class QuickCustomerCreateView(View):
    def post(self, request):
        company = request.POST.get('company_name')
        name = request.POST.get('name')
        phone = request.POST.get('phone_number')
        
        if company and name and phone:
            new_cust = Customer.objects.create(
                company_name=company,
                name=name,
                phone_number=phone
            )
            # Redirect back to the call add page
            return redirect('marketing:call_create')
        return redirect('marketing:call_create')