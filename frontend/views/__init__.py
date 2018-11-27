from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'frontend/routes.html')

def about(request):
    return render(request, 'frontend/about.html')

def sailings(request, params):
    return render(request, 'frontend/sailings.html')

def ferries(request):
    return render(request, 'frontend/ferries.html')

def routes(request, params):
    return render(request, 'frontend/routes.html')
