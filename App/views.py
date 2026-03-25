from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def saved_jobs(request):
    return render(request, 'saved-jobs.html')   

def jobs(request):
    return render(request, 'jobs.html')

def companies(request):
    return render(request, 'companies.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')