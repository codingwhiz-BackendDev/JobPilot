import requests
from django.shortcuts import render
from .models import Job
from django.utils import timezone
from datetime import timedelta

def index(request):
    jobs = Job.objects.all()[:10]
    context = {
        'jobs':jobs
    }
    return render(request, "index.html", context)

def jobs(request):
    jobs_list = []
    cached_jobs = None

    if request.method == "POST":
        query = request.POST.get("query", "").lower().strip()

        print("===== JOB SCRAPER STARTED =====")
        print(f"User searched for: {query}")

        # Find cached jobs
        cached_jobs = Job.objects.filter(title__icontains=query).order_by('-created_at')

        CACHE_DURATION = timedelta(days=1)  # 24 hours

        if cached_jobs.exists():
            latest_job = cached_jobs.first()

            # Check if cache is still valid
            if latest_job.created_at > timezone.now() - CACHE_DURATION:
                print("Using cached jobs (less than 24 hours old)")
                print(f"Returning {cached_jobs.count()} cached jobs")

                jobs_list = list(
                    cached_jobs.values('title', 'company', 'location', 'link')
                )

                return render(request, "jobs.html", {
                    "jobs": jobs_list,
                    "cached_jobs": cached_jobs
                })

            else:
                print("Cache expired. Fetching new jobs...")

        else:
            print("No cached jobs found. Scraping RemoteOK...")

        # Fetch from RemoteOK
        api_url = "https://remoteok.com/api"

        try:
            response = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
            print(f"Website status: {response.status_code}")

            if response.status_code != 200:
                print("Error fetching jobs from API.")
                return render(request, "jobs.html", {"jobs": jobs_list})

            data = response.json()
            print(f"Total jobs received from API: {len(data)-1}")

            search_words = query.split()

            allowed_regions = [
                "united states", "usa", "us",
                "uk", "united kingdom",
                "canada",
                "europe", "eu",
                "remote"
            ]

            for job in data[1:]:
                title = (job.get("position") or "").lower()
                company = job.get("company") or "Unknown"
                location = (job.get("location") or "remote").lower()
                link = job.get("url")

                if link and not link.startswith("https://"):
                    link = "https://remoteok.com" + link

                # Match search words
                if search_words and not any(word in title for word in search_words):
                    continue

                # Region filter
                if not any(region in location for region in allowed_regions):
                    continue

                # Avoid duplicates
                job_obj, created = Job.objects.get_or_create(
                    link=link,
                    defaults={
                        "title": title.title(),
                        "company": company,
                        "location": location.title(),
                    }
                )

                jobs_list.append({
                    "title": job_obj.title,
                    "company": job_obj.company,
                    "location": job_obj.location,
                    "link": job_obj.link
                })

                if created:
                    print("\n--- NEW JOB SAVED ---")
                else:
                    print("\n--- JOB ALREADY EXISTS ---")

                print(job_obj)

            print(f"\nTotal jobs returned: {len(jobs_list)}")
            print("===== SCRAPER FINISHED =====")

        except Exception as e:
            print("Error:", e)

    return render(request, "jobs.html", {
        "jobs": jobs_list,
        "cached_jobs": cached_jobs
    })
    
def saved_jobs(request):
    return render(request, "jobs.html")

def job_details(request):
    return render(request, "job_details.html")

def companies(request):
    return render(request, "companies.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")