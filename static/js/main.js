/* ============================================
   MAIN LANDING PAGE LOGIC
   ============================================ */

// Mock data - Replace with API call
const mockJobs = [
    {
        id: 1,
        title: "Senior Frontend Engineer",
        company: "TechCorp",
        logo: "TC",
        salary: "$120K - $150K",
        location: "USA",
        tags: ["React", "TypeScript", "Remote"],
        description: "We're looking for an experienced Frontend Engineer to join our growing team."
    },
    {
        id: 2,
        title: "Full Stack Developer",
        company: "StartupXYZ",
        logo: "SX",
        salary: "$100K - $130K",
        location: "UK",
        tags: ["Node.js", "React", "MongoDB"],
        description: "Help us build the next generation of web applications."
    },
    {
        id: 3,
        title: "UX/UI Designer",
        company: "DesignStudio",
        logo: "DS",
        salary: "$90K - $120K",
        location: "Canada",
        tags: ["Figma", "Design Systems", "Remote"],
        description: "Create beautiful and intuitive user experiences for our products."
    },
    {
        id: 4,
        title: "Backend Engineer",
        company: "CloudTech",
        logo: "CT",
        salary: "$110K - $140K",
        location: "USA",
        tags: ["Python", "PostgreSQL", "AWS"],
        description: "Build scalable backend systems for millions of users."
    },
    {
        id: 5,
        title: "Product Manager",
        company: "InnovateCo",
        logo: "IC",
        salary: "$130K - $160K",
        location: "Remote",
        tags: ["Strategy", "Analytics", "Leadership"],
        description: "Lead product vision and strategy for our growing platform."
    },
    {
        id: 6,
        title: "DevOps Engineer",
        company: "InfraScale",
        logo: "IS",
        salary: "$115K - $145K",
        location: "UK",
        tags: ["Kubernetes", "Docker", "CI/CD"],
        description: "Optimize our infrastructure and deployment processes."
    }
];

const mockCompanies = [
    { id: 1, name: "TechCorp", logo: "TC", jobs: 12, description: "Leading technology innovators" },
    { id: 2, name: "StartupXYZ", logo: "SX", jobs: 8, description: "Next-gen SaaS platform" },
    { id: 3, name: "DesignStudio", logo: "DS", jobs: 5, description: "Creative design agency" },
    { id: 4, name: "CloudTech", logo: "CT", jobs: 15, description: "Cloud infrastructure leader" },
    { id: 5, name: "InnovateCo", logo: "IC", jobs: 10, description: "AI and ML innovators" },
    { id: 6, name: "InfraScale", logo: "IS", jobs: 7, description: "Infrastructure automation" }
];

// Render featured jobs
function renderFeaturedJobs(jobs = mockJobs) {
    const container = document.getElementById('featuredJobs');
    if (!container) return;

    container.innerHTML = jobs.slice(0, 3).map(job => `
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
}

// Load featured jobs from Django backend.
async function loadFeaturedJobsFromApi() {
    try {
        const res = await fetch('/api/jobs/featured/?limit=3');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (data && Array.isArray(data.jobs) && data.jobs.length > 0) return data.jobs;
    } catch (err) {
        console.warn('Could not load featured jobs from API, using fallback mock data.', err);
    }
    return mockJobs.slice(0, 3);
}

// Render trending companies
function renderTrendingCompanies() {
    const container = document.getElementById('trendingCompanies');
    if (!container) return;

    container.innerHTML = mockCompanies.slice(0, 6).map(company => `
        <div class="company-card animate-cardEntrance hover-lift">
            <div class="company-logo-large">${company.logo}</div>
            <div class="company-name-large">${company.name}</div>
            <div class="company-desc">${company.description}</div>
            <div class="company-stat">${company.jobs} open positions</div>
        </div>
    `).join('');
}

// Save job to localStorage
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

// Search from hero
function searchJobs() {
    const searchInput = document.getElementById('heroSearch');
    const locationInput = document.getElementById('heroLocation');
    
    if (searchInput && locationInput) {
        const query = searchInput.value;
        const location = locationInput.value;
        
        // Redirect to jobs page with search params
        let url = 'jobs.html';
        if (query || location) {
            const params = new URLSearchParams();
            if (query) params.append('q', query);
            if (location) params.append('location', location);
            url += '?' + params.toString();
        }
        
        window.location.href = url;
    }
}

// Navigate to job details
function goToJobDetails(jobId) {
    window.location.href = `/job-details/?id=${jobId}`;
}

// Allow Enter key in search
document.addEventListener('DOMContentLoaded', async () => {
    const heroSearch = document.getElementById('heroSearch');
    if (heroSearch) {
        heroSearch.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchJobs();
            }
        });
    }

    // Render components
    const featuredJobs = await loadFeaturedJobsFromApi();
    renderFeaturedJobs(featuredJobs);
    renderTrendingCompanies();

    // Add stagger animation class
    const jobsContainer = document.getElementById('featuredJobs');
    const companiesContainer = document.getElementById('trendingCompanies');
    
    if (jobsContainer) jobsContainer.classList.add('stagger');
    if (companiesContainer) companiesContainer.classList.add('stagger');
});
