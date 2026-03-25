/* ============================================
   JOBS LISTING PAGE LOGIC
   ============================================ */

// Extended mock data (fallback if API is empty/unreachable)
let allJobs = [
    {
        id: 1,
        title: "Senior Frontend Engineer",
        company: "TechCorp",
        logo: "TC",
        salary: "$120K - $150K",
        salaryRange: "100k-150k",
        location: "USA",
        type: "Full-time",
        tags: ["React", "TypeScript", "Remote"],
        description: "We're looking for an experienced Frontend Engineer to join our growing team.",
        posted: "2 days ago"
    },
    {
        id: 2,
        title: "Full Stack Developer",
        company: "StartupXYZ",
        logo: "SX",
        salary: "$100K - $130K",
        salaryRange: "100k-150k",
        location: "UK",
        type: "Full-time",
        tags: ["Node.js", "React", "MongoDB"],
        description: "Help us build the next generation of web applications.",
        posted: "1 day ago"
    },
    {
        id: 3,
        title: "UX/UI Designer",
        company: "DesignStudio",
        logo: "DS",
        salary: "$90K - $120K",
        salaryRange: "50k-100k",
        location: "Canada",
        type: "Full-time",
        tags: ["Figma", "Design Systems", "Remote"],
        description: "Create beautiful and intuitive user experiences for our products.",
        posted: "3 days ago"
    },
    {
        id: 4,
        title: "Backend Engineer",
        company: "CloudTech",
        logo: "CT",
        salary: "$110K - $140K",
        salaryRange: "100k-150k",
        location: "USA",
        type: "Full-time",
        tags: ["Python", "PostgreSQL", "AWS"],
        description: "Build scalable backend systems for millions of users.",
        posted: "1 week ago"
    },
    {
        id: 5,
        title: "Product Manager",
        company: "InnovateCo",
        logo: "IC",
        salary: "$130K - $160K",
        salaryRange: "150k+",
        location: "Remote",
        type: "Full-time",
        tags: ["Strategy", "Analytics", "Leadership"],
        description: "Lead product vision and strategy for our growing platform.",
        posted: "2 days ago"
    },
    {
        id: 6,
        title: "DevOps Engineer",
        company: "InfraScale",
        logo: "IS",
        salary: "$115K - $145K",
        salaryRange: "100k-150k",
        location: "UK",
        type: "Full-time",
        tags: ["Kubernetes", "Docker", "CI/CD"],
        description: "Optimize our infrastructure and deployment processes.",
        posted: "5 days ago"
    },
    {
        id: 7,
        title: "Junior Developer",
        company: "TechCorp",
        logo: "TC",
        salary: "$60K - $80K",
        salaryRange: "50k-100k",
        location: "USA",
        type: "Full-time",
        tags: ["JavaScript", "CSS", "HTML"],
        description: "Start your career with us! We mentor junior developers.",
        posted: "3 days ago"
    },
    {
        id: 8,
        title: "Data Scientist",
        company: "DataInsight",
        logo: "DI",
        salary: "$140K - $180K",
        salaryRange: "150k+",
        location: "Remote",
        type: "Full-time",
        tags: ["Python", "ML", "TensorFlow"],
        description: "Transform data into actionable insights with machine learning.",
        posted: "4 days ago"
    },
    {
        id: 9,
        title: "Content Writer",
        company: "MediaHub",
        logo: "MH",
        salary: "$50K - $70K",
        salaryRange: "50k-100k",
        location: "Canada",
        type: "Part-time",
        tags: ["SEO", "Copywriting", "Research"],
        description: "Create compelling content for our growing audience.",
        posted: "1 day ago"
    },
    {
        id: 10,
        title: "Sales Manager",
        company: "SalesPro",
        logo: "SP",
        salary: "$80K - $110K",
        salaryRange: "100k-150k",
        location: "USA",
        type: "Full-time",
        tags: ["Sales", "Leadership", "CRM"],
        description: "Lead our sales team to new heights.",
        posted: "2 days ago"
    }
];

const itemsPerPage = 6;
let currentPage = 1;
let filteredJobs = [...allJobs];

// Get URL parameters
function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        search: params.get('q') || '',
        location: params.get('location') || ''
    };
}

// Load jobs from Django backend instead of relying on mock data.
async function loadJobsFromApi() {
    const params = getUrlParams();
    const qs = new URLSearchParams();

    if (params.search) qs.append('q', params.search);
    if (params.location) qs.append('location', params.location);

    // API has a safety cap; keep this small for faster UI.
    qs.append('page_size', '200');

    try {
        const res = await fetch(`/api/jobs/?${qs.toString()}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (data && Array.isArray(data.jobs) && data.jobs.length > 0) {
            allJobs = data.jobs;
        }
    } catch (err) {
        console.warn('Could not load jobs from API, using fallback mock data.', err);
    }
}

// Apply filters
function applyFilters() {
    const searchValue = document.getElementById('searchFilter')?.value || '';
    const mainSearchValue = document.getElementById('mainSearch')?.value || '';
    const selectedLocations = Array.from(document.querySelectorAll('.location-filter:checked')).map(el => el.value);
    const selectedSalaries = Array.from(document.querySelectorAll('.salary-filter:checked')).map(el => el.value);
    const selectedTypes = Array.from(document.querySelectorAll('.type-filter:checked')).map(el => el.value);

    const query = (searchValue || mainSearchValue).toLowerCase();

    filteredJobs = allJobs.filter(job => {
        // Search filter
        if (query && !job.title.toLowerCase().includes(query) && !job.company.toLowerCase().includes(query)) {
            return false;
        }

        // Location filter
        if (selectedLocations.length > 0 && !selectedLocations.includes(job.location)) {
            return false;
        }

        // Salary filter
        if (selectedSalaries.length > 0 && !selectedSalaries.includes(job.salaryRange)) {
            return false;
        }

        // Type filter
        if (selectedTypes.length > 0 && !selectedTypes.includes(job.type)) {
            return false;
        }

        return true;
    });

    currentPage = 1;
    renderJobs();
    updateResults();
}

// Render jobs
function renderJobs() {
    const container = document.getElementById('jobsList');
    if (!container) return;

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const paginatedJobs = filteredJobs.slice(start, end);

    if (paginatedJobs.length === 0) {
        container.innerHTML = '<div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 3rem;"><p>No jobs found matching your criteria.</p></div>';
        return;
    }

    container.innerHTML = paginatedJobs.map(job => `
        <div class="job-card animate-cardEntrance" onclick="goToJobDetails(${job.id})">
            <div class="job-header">
                <div class="company-logo">${job.logo}</div>
                <div class="job-title-group">
                    <div class="job-title">${job.title}</div>
                    <div class="company-name">${job.company}</div>
                </div>
            </div>
            <div class="job-meta">
                <span class="meta-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                        <circle cx="12" cy="10" r="3"></circle>
                    </svg>
                    ${job.location}
                </span>
                <span class="job-salary">${job.salary}</span>
                <span class="meta-item">${job.posted}</span>
            </div>
            <div class="job-tags">
                ${job.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
            <div class="job-footer">
                <button class="btn-primary" onclick="event.stopPropagation()">Apply</button>
                <button class="save-btn" onclick="event.stopPropagation(); toggleSaveJob(${job.id})">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                        <polyline points="17 21 17 13 7 13 7 21"></polyline>
                        <polyline points="7 3 7 8 15 8"></polyline>
                    </svg>
                </button>
            </div>
        </div>
    `).join('');

    // Add stagger animation
    container.classList.add('stagger');
}

// Update results info
function updateResults() {
    const info = document.getElementById('resultsInfo');
    if (info) {
        info.innerHTML = `Showing <strong>${filteredJobs.length}</strong> job${filteredJobs.length !== 1 ? 's' : ''}`;
    }
}

// Render pagination
function renderPagination() {
    const container = document.getElementById('pagination');
    if (!container || filteredJobs.length === 0) return;

    const totalPages = Math.ceil(filteredJobs.length / itemsPerPage);
    let html = '';

    // Previous button
    if (currentPage > 1) {
        html += `<button class="pagination-item" onclick="goToPage(${currentPage - 1})">←</button>`;
    }

    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        if (i === currentPage) {
            html += `<button class="pagination-item active">${i}</button>`;
        } else if (Math.abs(i - currentPage) <= 2 || i === 1 || i === totalPages) {
            html += `<button class="pagination-item" onclick="goToPage(${i})">${i}</button>`;
        } else if (Math.abs(i - currentPage) === 3) {
            html += `<span class="pagination-item">...</span>`;
        }
    }

    // Next button
    if (currentPage < totalPages) {
        html += `<button class="pagination-item" onclick="goToPage(${currentPage + 1})">→</button>`;
    }

    container.innerHTML = html;
}

// Go to page
function goToPage(page) {
    currentPage = page;
    renderJobs();
    renderPagination();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Toggle save job
function toggleSaveJob(jobId) {
    let saved = JSON.parse(localStorage.getItem('savedJobs') || '[]');
    const index = saved.indexOf(jobId);
    
    if (index > -1) {
        saved.splice(index, 1);
    } else {
        saved.push(jobId);
    }
    
    localStorage.setItem('savedJobs', JSON.stringify(saved));
}

// Navigate to job details
function goToJobDetails(jobId) {
    window.location.href = `/job-details/?id=${jobId}`;
}

// Clear filters
function clearFilters() {
    document.getElementById('searchFilter').value = '';
    document.getElementById('mainSearch').value = '';
    document.querySelectorAll('.location-filter, .salary-filter, .type-filter').forEach(el => el.checked = false);
    applyFilters();
}

// Event listeners
document.addEventListener('DOMContentLoaded', async () => {
    // Apply URL params if present
    const params = getUrlParams();
    if (params.search) {
        const searchInput = document.getElementById('mainSearch');
        if (searchInput) searchInput.value = params.search;
    }
    if (params.location) {
        const locationInput = document.querySelector(`.location-filter[value="${params.location}"]`);
        if (locationInput) locationInput.checked = true;
    }

    // Add event listeners
    document.getElementById('searchFilter')?.addEventListener('input', applyFilters);
    document.getElementById('mainSearch')?.addEventListener('input', applyFilters);
    document.querySelectorAll('.location-filter, .salary-filter, .type-filter').forEach(el => {
        el.addEventListener('change', applyFilters);
    });
    document.getElementById('clearFilters')?.addEventListener('click', clearFilters);

    await loadJobsFromApi();

    // Initial render
    applyFilters();
    renderPagination();
});
