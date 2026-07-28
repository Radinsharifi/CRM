from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/add/', views.CustomerCreateView.as_view(), name='customer_create'),
    
    path('calls/', views.CallListView.as_view(), name='call_list'),
    path('calls/<int:pk>/', views.CallDetailView.as_view(), name='call_detail'),
    path('calls/add/', views.CallCreateView.as_view(), name='call_create'),
    path('calls/<int:pk>/delete/', views.CallDeleteView.as_view(), name='call_delete'),
    path('customers/quick-add/', views.QuickCustomerCreateView.as_view(), name='customer_create_js'),
]