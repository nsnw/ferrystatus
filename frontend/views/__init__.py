from django.shortcuts import render

# Single view for the frontend - we'll handle everything else with React
def app(request, params):
    return render(request, 'frontend/app.html')
