from django.shortcuts import render

# Create your views here.
def home(request, params):
    return render(request, 'frontend/app.html')

def about(request):
    return render(request, 'frontend/about.html')

def faq(request):
    return render(request, 'frontend/faq.html')

def privacy(request):
    return render(request, 'frontend/privacy.html')
