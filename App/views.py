from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
import requests
import xml.etree.ElementTree as ET
from .models import Job


def index(request):
    jobs = Job.objects.all()[:10]
    context = {'jobs': jobs}
    return render(request, "index.html", context)


def jobs(request):
    jobs_list = []
    cached_jobs = None

    if request.method == "GET":
        jobs_list = list(
            Job.objects.all()
            .order_by('-created_at')
            .values('title', 'company', 'location', 'link')[:50]
        )

        return render(request, "jobs.html", {
            "jobs": jobs_list
        })

    if request.method == "POST":
        query = request.POST.get("query", "").lower().strip()

        print("\n===== JOB SCRAPER STARTED =====")
        print("User searched for:", query)

        cached_jobs = Job.objects.filter(title__icontains=query).order_by('-created_at')

        CACHE_DURATION = timedelta(days=1)

        if cached_jobs.exists():
            latest_job = cached_jobs.first()

            if latest_job.created_at > timezone.now() - CACHE_DURATION:
                print("Using cached jobs")
                print("Cached jobs:", cached_jobs.count())

                jobs_list = list(
                    cached_jobs.values('title', 'company', 'location', 'link')
                )

                return render(request, "jobs.html", {
                    "jobs": jobs_list,
                    "cached_jobs": cached_jobs
                })
        else:
            print("No cached jobs found. Scraping sites...")

        search_words = query.split()

        try:

            # -------------------------
            # RemoteOK
            # -------------------------
            print("\nFetching jobs from RemoteOK...")
            try:
                response = requests.get(
                    "https://remoteok.com/api",
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=10
                )
                data = response.json()

                print("RemoteOK jobs received:", len(data) - 1)

                for job in data[1:]:
                    title = (job.get("position") or "").lower()
                    company = job.get("company") or "Unknown"
                    location = (job.get("location") or "remote").lower()
                    link = job.get("url")

                    if not link or not title:
                        continue

                    if search_words and not any(word in title for word in search_words):
                        continue

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
                        print("RemoteOK NEW JOB:", job_obj)

            except requests.exceptions.Timeout:
                print("RemoteOK request timed out.")
            except requests.exceptions.RequestException as e:
                print(f"RemoteOK request error: {e}")
            except Exception as e:
                print(f"RemoteOK unexpected error: {e}")

            # -------------------------
            # Remotive
            # -------------------------
            print("\nFetching jobs from Remotive...")
            try:
                response = requests.get(
                    "https://remotive.com/api/remote-jobs",
                    timeout=10
                )
                data = response.json()

                print("Remotive jobs received:", len(data["jobs"]))

                for job in data["jobs"]:
                    title = (job.get("title") or "").lower()
                    company = job.get("company_name") or "Unknown"
                    link = job.get("url")

                    if not link or not title:
                        continue

                    if search_words and not any(word in title for word in search_words):
                        continue

                    job_obj, created = Job.objects.get_or_create(
                        link=link,
                        defaults={
                            "title": title.title(),
                            "company": company,
                            "location": "Remote",
                        }
                    )

                    jobs_list.append({
                        "title": job_obj.title,
                        "company": job_obj.company,
                        "location": job_obj.location,
                        "link": job_obj.link
                    })

                    if created:
                        print("Remotive NEW JOB:", job_obj)

            except requests.exceptions.Timeout:
                print("Remotive request timed out.")
            except requests.exceptions.RequestException as e:
                print(f"Remotive request error: {e}")
            except Exception as e:
                print(f"Remotive unexpected error: {e}")

            # -------------------------
            # Arbeitnow
            # -------------------------
            print("\nFetching jobs from Arbeitnow...")
            try:
                response = requests.get(
                    "https://www.arbeitnow.com/api/job-board-api",
                    timeout=10
                )
                data = response.json()

                print("Arbeitnow jobs received:", len(data["data"]))

                for job in data["data"]:
                    title = (job.get("title") or "").lower()
                    company = job.get("company_name") or "Unknown"
                    location = (job.get("location") or "Remote")
                    link = job.get("url")

                    if not link or not title:
                        continue

                    if search_words and not any(word in title for word in search_words):
                        continue

                    job_obj, created = Job.objects.get_or_create(
                        link=link,
                        defaults={
                            "title": title.title(),
                            "company": company,
                            "location": location,
                        }
                    )

                    jobs_list.append({
                        "title": job_obj.title,
                        "company": job_obj.company,
                        "location": job_obj.location,
                        "link": job_obj.link
                    })

                    if created:
                        print("Arbeitnow NEW JOB:", job_obj)

            except requests.exceptions.Timeout:
                print("Arbeitnow request timed out.")
            except requests.exceptions.RequestException as e:
                print(f"Arbeitnow request error: {e}")
            except Exception as e:
                print(f"Arbeitnow unexpected error: {e}")

            # -------------------------
            # Jobicy — FIX: fetch all jobs (no tag filter) then filter locally
            # The tag param was returning 0 results for most queries
            # -------------------------
            print("\nFetching jobs from Jobicy...")
            try:
                jobicy_url = "https://jobicy.com/api/v2/remote-jobs?count=50"

                response = requests.get(
                    jobicy_url,
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=10
                )
                data = response.json()

                jobicy_jobs = data.get("jobs", [])
                print("Jobicy jobs received:", len(jobicy_jobs))

                for job in jobicy_jobs:
                    title = (job.get("jobTitle") or "").lower()
                    company = job.get("companyName") or "Unknown"
                    location = job.get("jobGeo") or "Remote"
                    link = job.get("url") or ""

                    if not link or not title:
                        continue

                    if search_words and not any(word in title for word in search_words):
                        continue

                    job_obj, created = Job.objects.get_or_create(
                        link=link,
                        defaults={
                            "title": title.title(),
                            "company": company,
                            "location": location,
                        }
                    )

                    jobs_list.append({
                        "title": job_obj.title,
                        "company": job_obj.company,
                        "location": job_obj.location,
                        "link": job_obj.link
                    })

                    if created:
                        print("Jobicy NEW JOB:", job_obj)

            except requests.exceptions.Timeout:
                print("Jobicy request timed out.")
            except requests.exceptions.RequestException as e:
                print(f"Jobicy request error: {e}")
            except Exception as e:
                print(f"Jobicy unexpected error: {e}")

            # -------------------------
            # The Muse — FIX: search across multiple pages and pass keyword
            # as a category hint; filter all results locally by search_words
            # -------------------------
            print("\nFetching jobs from The Muse...")
            try:
                muse_total = 0
                for page in range(1, 4):  # fetch pages 1, 2, 3 = up to 60 results
                    muse_url = (
                        f"https://www.themuse.com/api/public/jobs"
                        f"?descending=true&page={page}&per_page=20"
                    )

                    response = requests.get(
                        muse_url,
                        headers={"User-Agent": "Mozilla/5.0"},
                        timeout=10
                    )
                    data = response.json()
                    muse_jobs = data.get("results", [])

                    if not muse_jobs:
                        break

                    for job in muse_jobs:
                        title = (job.get("name") or "").lower()
                        company = (job.get("company") or {}).get("name") or "Unknown"

                        locations = job.get("locations") or []
                        location = locations[0].get("name") if locations else "Remote"

                        short_name = (job.get("company") or {}).get("short_name") or ""
                        job_short_name = job.get("short_name") or ""
                        link = (
                            f"https://www.themuse.com/jobs/{short_name}/{job_short_name}"
                            if short_name and job_short_name else ""
                        )

                        if not link or not title:
                            continue

                        if search_words and not any(word in title for word in search_words):
                            continue

                        job_obj, created = Job.objects.get_or_create(
                            link=link,
                            defaults={
                                "title": title.title(),
                                "company": company,
                                "location": location,
                            }
                        )

                        jobs_list.append({
                            "title": job_obj.title,
                            "company": job_obj.company,
                            "location": job_obj.location,
                            "link": job_obj.link
                        })

                        muse_total += 1

                        if created:
                            print("The Muse NEW JOB:", job_obj)

                print(f"The Muse jobs collected: {muse_total}")

            except requests.exceptions.Timeout:
                print("The Muse request timed out.")
            except requests.exceptions.RequestException as e:
                print(f"The Muse request error: {e}")
            except Exception as e:
                print(f"The Muse unexpected error: {e}")

            # -------------------------
            # Adzuna
            # -------------------------
            print("\nFetching jobs from Adzuna...")
            try:
                ADZUNA_APP_ID = "0b6cb544"
                ADZUNA_APP_KEY = "8cc0d13f2d15e24bbf813268afaee354"

                adzuna_query = query.replace(" ", "%20")
                url = (
                    f"https://api.adzuna.com/v1/api/jobs/gb/search/1"
                    f"?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}"
                    f"&results_per_page=20&what={adzuna_query}"
                )

                response = requests.get(url, timeout=10)
                data = response.json()

                results = data.get("results", [])
                print("Adzuna jobs received:", len(results))

                for job in results:
                    title = (job.get("title") or "").lower()
                    company = (job.get("company") or {}).get("display_name") or "Unknown"
                    location = (job.get("location") or {}).get("display_name") or "Unknown"
                    link = job.get("redirect_url") or job.get("url") or ""

                    if search_words and not any(word in title for word in search_words):
                        continue

                    if not link:
                        continue

                    job_obj, created = Job.objects.get_or_create(
                        link=link,
                        defaults={
                            "title": title.title(),
                            "company": company,
                            "location": location,
                        }
                    )

                    jobs_list.append({
                        "title": job_obj.title,
                        "company": job_obj.company,
                        "location": job_obj.location,
                        "link": job_obj.link
                    })

                    if created:
                        print("Adzuna NEW JOB:", job_obj)

            except requests.exceptions.Timeout:
                print("Adzuna request timed out.")
            except requests.exceptions.RequestException as e:
                print(f"Adzuna request error: {e}")
            except Exception as e:
                print(f"Adzuna unexpected error: {e}")

            # -------------------------
            # We Work Remotely — FIX: added allow_redirects=True to handle
            # the 301s that were causing 7 feeds to silently fail
            # -------------------------
            print("\nFetching jobs from We Work Remotely (RSS)...")

            WWR_RSS_FEEDS = [
                "https://weworkremotely.com/categories/remote-programming-jobs.rss",
                "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss",
                "https://weworkremotely.com/categories/remote-design-jobs.rss",
                "https://weworkremotely.com/categories/remote-marketing-jobs.rss",
                "https://weworkremotely.com/categories/remote-product-jobs.rss",
                "https://weworkremotely.com/categories/remote-customer-support-jobs.rss",
                "https://weworkremotely.com/categories/remote-sales-jobs.rss",
                "https://weworkremotely.com/categories/remote-writing-jobs.rss",
                "https://weworkremotely.com/categories/remote-business-exec-management-jobs.rss",
                "https://weworkremotely.com/categories/remote-finance-legal-jobs.rss",
                "https://weworkremotely.com/categories/remote-human-resources-jobs.rss",
                "https://weworkremotely.com/categories/remote-data-science-jobs.rss",
            ]

            WWR_RSS_HEADERS = {
                "User-Agent": "Mozilla/5.0 (compatible; RSS reader)",
                "Accept": "application/rss+xml, application/xml, text/xml",
            }

            wwr_total = 0

            for feed_url in WWR_RSS_FEEDS:
                try:
                    rss_response = requests.get(
                        feed_url,
                        headers=WWR_RSS_HEADERS,
                        timeout=10,
                        allow_redirects=True,  # FIX: follow 301 redirects
                    )

                    if rss_response.status_code != 200:
                        print(f"WWR RSS feed returned {rss_response.status_code}: {feed_url}")
                        continue

                    root = ET.fromstring(rss_response.content)
                    channel = root.find("channel")

                    if channel is None:
                        continue

                    items = channel.findall("item")

                    for item in items:
                        raw_title = (item.findtext("title") or "").strip()
                        link = (item.findtext("link") or "").strip()
                        region = (item.findtext("region") or "Remote").strip()

                        if ": " in raw_title:
                            parts = raw_title.split(": ", 1)
                            company = parts[0].strip()
                            title = parts[1].strip().lower()
                        else:
                            company = "Unknown"
                            title = raw_title.lower()

                        if not link or not title:
                            continue

                        if search_words and not any(word in title for word in search_words):
                            continue

                        job_obj, created = Job.objects.get_or_create(
                            link=link,
                            defaults={
                                "title": title.title(),
                                "company": company,
                                "location": region if region else "Remote",
                            }
                        )

                        jobs_list.append({
                            "title": job_obj.title,
                            "company": job_obj.company,
                            "location": job_obj.location,
                            "link": job_obj.link
                        })

                        wwr_total += 1

                        if created:
                            print("We Work Remotely NEW JOB:", job_obj)

                except requests.exceptions.Timeout:
                    print(f"WWR RSS feed timed out: {feed_url}")
                except ET.ParseError as e:
                    print(f"WWR RSS parse error for {feed_url}: {e}")
                except requests.exceptions.RequestException as e:
                    print(f"WWR RSS request error for {feed_url}: {e}")

            print(f"We Work Remotely jobs collected: {wwr_total}")

            print("\nTotal jobs collected:", len(jobs_list))
            print("===== SCRAPER FINISHED =====\n")

        except Exception as e:
            print("Error:", e)

    return render(request, "jobs.html", {
        "jobs": jobs_list,
        "cached_jobs": cached_jobs
    })
    
def companies(request):
    # Pull one representative job per unique company name
    # so we get location + link without loading every job row
    from django.db.models import Count, Max
 
    company_data = (
        Job.objects
        .values('company', 'location')
        .annotate(
            job_count=Count('id'),
            latest_link=Max('link'),   
        )
        .order_by('company')
    )
 
    return render(request, "companies.html", {
        "companies": company_data,
        "total": company_data.count(),
    })
 
    
def saved_jobs(request):
    return render(request, "jobs.html")

def job_details(request):
    return render(request, "job_details.html")

 

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")