import re
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Job


def index(request):
    return render(request, "index.html")


def saved_jobs(request):
    return render(request, "jobs.html")


def jobs(request):
    return render(request, "jobs.html")


def job_details(request):
    return render(request, "job_details.html")


def companies(request):
    return render(request, "companies.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def _job_to_dict(job: Job) -> dict:
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company.name,
        "logo": job.company.logo_text,
        "salary": job.salary,
        "salaryRange": job.salary_range,
        "location": job.location,
        "type": job.job_type,
        "tags": job.tags or [],
        "posted": job.posted_text,
        "description": job.description,
    }


def _safe_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def api_jobs(request):
    """
    GET /api/jobs/?q=django&location=Remote&page=1&page_size=50
    """
    if request.method != "GET":
        return JsonResponse({"error": "Only GET supported"}, status=405)

    q = (request.GET.get("q") or "").strip()
    location = (request.GET.get("location") or "").strip()
    page = _safe_int(request.GET.get("page"), 1)
    page_size = _safe_int(request.GET.get("page_size"), 50)
    page_size = max(1, min(page_size, 200))

    qs = Job.objects.select_related("company").all()

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(company__name__icontains=q))

    if location:
        # Scraped location strings can vary slightly; be forgiving.
        qs = qs.filter(location__icontains=location)

    qs = qs.order_by("-scraped_at")

    start = (page - 1) * page_size
    end = start + page_size

    jobs = qs[start:end]

    return JsonResponse(
        {
            "jobs": [_job_to_dict(job) for job in jobs],
            "page": page,
            "page_size": page_size,
            "total": qs.count(),
        }
    )


def api_jobs_featured(request):
    """
    GET /api/jobs/featured/?limit=6
    """
    if request.method != "GET":
        return JsonResponse({"error": "Only GET supported"}, status=405)

    limit = _safe_int(request.GET.get("limit"), 6)
    limit = max(1, min(limit, 50))

    qs = Job.objects.select_related("company").order_by("-scraped_at")[:limit]
    return JsonResponse({"jobs": [_job_to_dict(job) for job in qs]})


def api_job_detail(request, job_id: int):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET supported"}, status=405)

    job = get_object_or_404(Job.objects.select_related("company"), pk=job_id)
    related = (
        Job.objects.select_related("company")
        .filter(company=job.company)
        .exclude(pk=job.pk)
        .order_by("-scraped_at")[:3]
    )

    # Frontend expects arrays; we currently store full description only.
    # If you later add structured responsibilities/requirements fields, update this.
    responsibilities = []
    requirements = []
    about = ""

    # Tiny heuristic: split around common headings inside the scraped text.
    text = job.description or ""
    m_about = re.search(r"(Role Overview|About the job|About this role)\s*(.+)", text, flags=re.I | re.S)
    if m_about:
        about = m_about.group(2).strip()[:2000]
    elif text:
        about = text.strip()[:2000]

    return JsonResponse(
        {
            **_job_to_dict(job),
            "about": about,
            "responsibilities": responsibilities,
            "requirements": requirements,
            "related_jobs": [_job_to_dict(j) for j in related],
        }
    )


def api_jobs_by_ids(request):
    """
    GET /api/jobs/by-ids/?ids=1,2,3
    Used by the frontend to render saved jobs without mock data.
    """
    if request.method != "GET":
        return JsonResponse({"error": "Only GET supported"}, status=405)

    ids_raw = request.GET.get("ids") or ""
    ids = []
    for part in ids_raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.append(int(part))
        except ValueError:
            continue

    if not ids:
        return JsonResponse({"jobs": []})

    qs = Job.objects.select_related("company").filter(pk__in=ids)
    qs = sorted(qs, key=lambda j: ids.index(j.pk))

    return JsonResponse({"jobs": [_job_to_dict(job) for job in qs]})