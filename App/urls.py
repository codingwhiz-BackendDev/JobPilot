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

    # API (used by your frontend JavaScript)
    path('api/jobs/', views.api_jobs, name='api-jobs'),
    path('api/jobs/featured/', views.api_jobs_featured, name='api-jobs-featured'),
    path('api/jobs/by-ids/', views.api_jobs_by_ids, name='api-jobs-by-ids'),
    path('api/jobs/<int:job_id>/', views.api_job_detail, name='api-job-detail'),
     
]