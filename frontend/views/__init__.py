from django.shortcuts import render

# Create your views here.
def app(request, params):
    return render(request, 'frontend/app.html')
