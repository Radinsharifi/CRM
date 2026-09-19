from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/add/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
    
    path('calls/', views.CallsHubView.as_view(), name='calls_hub'),
    path('calls/records/', views.CallListView.as_view(), name='call_list'),
    path('calls/records/<int:pk>/', views.CallDetailView.as_view(), name='call_detail'),
    path('calls/records/add/', views.CallCreateView.as_view(), name='call_create'),
    path('calls/records/<int:pk>/edit/', views.CallUpdateView.as_view(), name='call_update'),
    path('calls/records/<int:pk>/delete/', views.CallDeleteView.as_view(), name='call_delete'),
    path('calls/reminders/', views.ReminderListView.as_view(), name='reminder_list'),
    path('calls/reminders/add/', views.ReminderCreateView.as_view(), name='reminder_create'),
    path('calls/reminders/<int:pk>/', views.ReminderDetailView.as_view(), name='reminder_detail'),
    path('calls/reminders/<int:pk>/edit/', views.ReminderUpdateView.as_view(), name='reminder_update'),
    path('calls/reminders/<int:pk>/delete/', views.ReminderDeleteView.as_view(), name='reminder_delete'),
    path('calls/tomorrow/', views.TomorrowTaskListView.as_view(), name='tomorrow_task_list'),
    path('calls/tomorrow/add/', views.TomorrowTaskCreateView.as_view(), name='tomorrow_task_create'),
    path('calls/tomorrow/<int:pk>/', views.TomorrowTaskDetailView.as_view(), name='tomorrow_task_detail'),
    path('calls/tomorrow/<int:pk>/edit/', views.TomorrowTaskUpdateView.as_view(), name='tomorrow_task_update'),
    path('calls/tomorrow/<int:pk>/delete/', views.TomorrowTaskDeleteView.as_view(), name='tomorrow_task_delete'),
    path('customers/quick-add/', views.QuickCustomerCreateView.as_view(), name='customer_create_js'),
    
]