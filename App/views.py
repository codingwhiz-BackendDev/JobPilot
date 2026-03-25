import requests
from bs4 import BeautifulSoup
from django.shortcuts import render


def index(request):
    return render(request, "index.html")  

def jobs(request):
    jobs_list = []

    if request.method == "POST":
        query = request.POST.get("query", "").lower().strip()
        print("===== JOB SCRAPER STARTED =====")
        print(f"User searched for: {query}")

        # RemoteOK API endpoint for remote jobs
        api_url = "https://remoteok.com/api"

        try:
            response = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
            print(f"Website status: {response.status_code}")

            if response.status_code != 200:
                print("Error fetching jobs from API.")
                return render(request, "jobs.html", {"jobs": jobs_list})

            data = response.json()
            print(f"Total jobs received from API: {len(data)-1}")  # first element is metadata

            search_words = query.split()
            allowed_regions = [
                "united states", "usa", "us",
                "uk", "united kingdom",
                "canada",
                "europe", "eu",
                "remote"
            ]

            for job in data[1:]:  # skip first element (metadata)
                title = (job.get("position") or "").lower()
                company = job.get("company")
                location = (job.get("location") or "remote").lower()
                link = job.get("url")

                if link and not link.startswith("https://"):
                    link = "https://remoteok.com" + link

                # Match search query words
                if search_words:
                    if not any(word in title for word in search_words):
                        continue

                # Filter only allowed regions
                if not any(region in location for region in allowed_regions):
                    continue

                job_data = {
                    "title": title.title(),
                    "company": company,
                    "location": location.title(),
                    "link": link
                }

                jobs_list.append(job_data)

                print("\n--- JOB ACCEPTED ---")
                print(job_data)

            print(f"\nTotal filtered jobs: {len(jobs_list)}")
            print("===== SCRAPER FINISHED =====")

        except Exception as e:
            print("Error:", e)

    return render(request, "jobs.html", {"jobs": jobs_list})


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

 
 