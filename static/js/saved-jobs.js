/* ============================================
   SAVED JOBS PAGE LOGIC
   ============================================ */

// All jobs database for reference
const allJobsData = [
    {
        id: 1,
        title: "Senior Frontend Engineer",
        company: "TechCorp",
        logo: "TC",
        salary: "$120K - $150K",
        location: "USA",
        type: "Full-time",
        tags: ["React", "TypeScript", "Remote"],
        posted: "2 days ago",
        savedDate: new Date()
    },
    {
        id: 2,
        title: "Full Stack Developer",
        company: "StartupXYZ",
        logo: "SX",
        salary: "$100K - $130K",
        location: "UK",
        type: "Full-time",
        tags: ["Node.js", "React", "MongoDB"],
        posted: "1 day ago",
        savedDate: new Date()
    },
    {
        id: 3,
        title: "UX/UI Designer",
        company: "DesignStudio",
        logo: "DS",
        salary: "$90K - $120K",
        location: "Canada",
        type: "Full-time",
        tags: ["Figma", "Design Systems", "Remote"],
        posted: "3 days ago",
        savedDate: new Date()
    },
    {
        id: 4,
        title: "Backend Engineer",
        company: "CloudTech",
        logo: "CT",
        salary: "$110K - $140K",
        location: "USA",
        type: "Full-time",
        tags: ["Python", "PostgreSQL", "AWS"],
        posted: "1 week ago",
        savedDate: new Date()
    },
    {
        id: 5,
        title: "Product Manager",
        company: "InnovateCo",
        logo: "IC",
        salary: "$130K - $160K",
        location: "Remote",
        type: "Full-time",
        tags: ["Strategy", "Analytics", "Leadership"],
        posted: "2 days ago",
        savedDate: new Date()
    },
    {
        id: 6,
        title: "DevOps Engineer",
        company: "InfraScale",
        logo: "IS",
        salary: "$115K - $145K",
        location: "UK",
        type: "Full-time",
        tags: ["Kubernetes", "Docker", "CI/CD"],
        posted: "5 days ago",
        savedDate: new Date()
    },
    {
        id: 7,
        title: "Junior Developer",
        company: "TechCorp",
        logo: "TC",
        salary: "$60K - $80K",
        location: "USA",
        type: "Full-time",
        tags: ["JavaScript", "CSS", "HTML"],
        posted: "3 days ago",
        savedDate: new Date()
    },
    {
        id: 8,
        title: "Data Scientist",
        company: "DataInsight",
        logo: "DI",
        salary: "$140K - $180K",
        location: "Remote",
        type: "Full-time",
        tags: ["Python", "ML", "TensorFlow"],
        posted: "4 days ago",
        savedDate: new Date()
    }
];

let savedJobs = [];
let sortOrder = 'recent';

// Get saved jobs
function getSavedJobs() {
    const savedIds = JSON.parse(localStorage.getItem('savedJobs') || '[]');
    return allJobsData.filter(job => savedIds.includes(job.id));
}

// Render saved jobs
function renderSavedJobs() {
    savedJobs = getSavedJobs();

    // Update count
    const countEl = document.getElementById('saveCount');
    if (countEl) {
        countEl.textContent = savedJobs.length;
    }

    // Show/hide empty state
    const emptyState = document.getElementById('emptyState');
    const savedJobsList = document.getElementById('savedJobsList');

    if (savedJobs.length === 0) {
        if (emptyState) emptyState.style.display = 'flex';
        if (savedJobsList) savedJobsList.innerHTML = '';
        return;
    } else {
        if (emptyState) emptyState.style.display = 'none';
    }

    // Sort jobs
    const sortedJobs = [...savedJobs].sort((a, b) => {
        switch(sortOrder) {
            case 'salary-high':
                return parseInt(b.salary) - parseInt(a.salary);
            case 'salary-low':
                return parseInt(a.salary) - parseInt(b.salary);
            case 'title':
                return a.title.localeCompare(b.title);
            case 'recent':
            default:
                return new Date(b.savedDate) - new Date(a.savedDate);
        }
    });

    // Render
    if (savedJobsList) {
        savedJobsList.innerHTML = sortedJobs.map(job => `
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
                    <button class="save-btn saved" onclick="event.stopPropagation(); removeFromSaved(${job.id})">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                            <polyline points="17 21 17 13 7 13 7 21"></polyline>
                            <polyline points="7 3 7 8 15 8"></polyline>
                        </svg>
                    </button>
                </div>
            </div>
        `).join('');

        // Add stagger animation
        savedJobsList.classList.add('stagger');
    }
}

// Remove from saved
function removeFromSaved(jobId) {
    let saved = JSON.parse(localStorage.getItem('savedJobs') || '[]');
    const index = saved.indexOf(jobId);
    
    if (index > -1) {
        saved.splice(index, 1);
    }
    
    localStorage.setItem('savedJobs', JSON.stringify(saved));
    renderSavedJobs();
}

// Go to job details
function goToJobDetails(jobId) {
    window.location.href = `job-details.html?id=${jobId}`;
}

// Sort saved jobs
function changeSortOrder(newOrder) {
    sortOrder = newOrder;
    renderSavedJobs();
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    const sortSelect = document.getElementById('savedJobsSort');
    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            changeSortOrder(e.target.value);
        });
    }

    renderSavedJobs();
});

// Add CSS for empty state
const style = document.createElement('style');
style.textContent = `
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 2rem;
        text-align: center;
    }

    .empty-icon {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: var(--surface);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.5rem;
        color: var(--text-tertiary);
    }

    .empty-state h2 {
        margin-bottom: 0.5rem;
        color: var(--text-primary);
    }

    .empty-state p {
        max-width: 400px;
        margin-bottom: 2rem;
    }

    .saved-jobs-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid var(--border);
    }

    .count-info {
        font-weight: 600;
        color: var(--text-primary);
    }

    .sort-select {
        padding: 0.5rem 1rem;
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        background: var(--surface);
        color: var(--text-primary);
        font-family: var(--font-family);
        cursor: pointer;
    }

    .saved-jobs-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
    }

    @media (max-width: 768px) {
        .saved-jobs-header {
            flex-direction: column;
            gap: 1rem;
            align-items: flex-start;
        }

        .sort-select {
            width: 100%;
        }

        .saved-jobs-list {
            grid-template-columns: 1fr;
        }
    }
`;
document.head.appendChild(style);
