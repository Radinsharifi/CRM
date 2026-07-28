from django.shortcuts import render

def view_customer(request):
    return render(request, "customers.html")

def view_dash(request):
    return render(request, "dashboard.html")

def view_marke(request):
    return render(request, "marketers.html")

def view_rep(request):
    return render(request, "reports.html")

def view_shipments(request):
    return render(request, "shipments.html")

