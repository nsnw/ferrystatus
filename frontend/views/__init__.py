from django.shortcuts import render

# Create your views here.

def sailings(request):
    return render(request, 'frontend/sailings.html')

def ferries(request):
    return render(request, 'frontend/ferries.html')
