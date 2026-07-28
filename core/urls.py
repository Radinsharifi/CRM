from . import views
from django.urls import path


urlpatterns = [
    path('customers/', views.view_customer, name='customers'),
    path('dashboard/', views.view_dash, name='dashboard'),
    path('marketers/', views.view_marke, name='marketers'),
    path('reports/', views.view_rep, name="reports" ),
    path('shipments/', views.view_shipments, name='shipments'),
]



