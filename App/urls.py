from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('saved-jobs/', views.saved_jobs, name = 'saved-jobs'),
    path('jobs/', views.jobs, name = 'jobs'),
    path('job-details/', views.job_details, name='job-details'),
    path('companies/', views.companies, name = 'companies'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),
 
     
]


