/* ============================================
   JOB DETAILS PAGE LOGIC
   ============================================ */

// Mock detailed job data
const jobsDatabase = {
    1: {
        id: 1,
        title: "Senior Frontend Engineer",
        company: "TechCorp",
        logo: "TC",
        salary: "$120K - $150K",
        location: "USA",
        type: "Full-time",
        posted: "2 days ago",
        tags: ["React", "TypeScript", "Remote", "Senior"],
        description: "We're building the future of web applications and we need an experienced Frontend Engineer to join our team. You'll work with cutting-edge technologies and have the opportunity to shape our product's direction.",
        responsibilities: [
            "Design and develop responsive, high-performance web interfaces",
            "Lead frontend architecture decisions and code reviews",
            "Collaborate with UX/UI designers to implement pixel-perfect designs",
            "Mentor junior developers and share your expertise",
            "Optimize application performance and ensure cross-browser compatibility",
            "Implement automated testing and maintain code quality standards"
        ],
        requirements: [
            "5+ years of professional frontend development experience",
            "Expert-level proficiency with React and TypeScript",
            "Deep understanding of modern JavaScript/ES6+",
            "Experience with state management (Redux, Zustand, or similar)",
            "Strong knowledge of web performance optimization",
            "Experience with testing frameworks (Jest, React Testing Library)",
            "Excellent communication and teamwork skills"
        ],
        about: "TechCorp is a leading technology company specializing in cloud solutions and web applications. We're a team of 200+ passionate developers, designers, and product managers working on products used by millions of users worldwide."
    },
    2: {
        id: 2,
        title: "Full Stack Developer",
        company: "StartupXYZ",
        logo: "SX",
        salary: "$100K - $130K",
        location: "UK",
        type: "Full-time",
        posted: "1 day ago",
        tags: ["Node.js", "React", "MongoDB", "Full Stack"],
        description: "Join our fast-growing startup and help us scale our platform. You'll work on both frontend and backend, directly impacting our product's success.",
        responsibilities: [
            "Develop full-stack features from concept to deployment",
            "Build RESTful APIs and optimize database queries",
            "Create responsive frontend interfaces with React",
            "Participate in product discussions and contribute ideas",
            "Maintain and improve existing codebase",
            "Collaborate with the design team to implement user-centric features"
        ],
        requirements: [
            "3+ years of full-stack development experience",
            "Proficiency with Node.js and Express",
            "Strong React knowledge",
            "MongoDB or other NoSQL database experience",
            "Understanding of RESTful API design",
            "Good problem-solving skills",
            "Ability to work in a fast-paced environment"
        ],
        about: "StartupXYZ is a Series A funded startup building the next generation of SaaS solutions. We're a lean team of 30 people with big ambitions and a focus on innovation."
    },
    3: {
        id: 3,
        title: "UX/UI Designer",
        company: "DesignStudio",
        logo: "DS",
        salary: "$90K - $120K",
        location: "Canada",
        type: "Full-time",
        posted: "3 days ago",
        tags: ["Figma", "Design Systems", "Remote", "UI/UX"],
        description: "Create beautiful and intuitive user experiences for our suite of products. You'll lead design decisions and build comprehensive design systems.",
        responsibilities: [
            "Design user interfaces for web and mobile applications",
            "Conduct user research and usability testing",
            "Create and maintain design systems and component libraries",
            "Collaborate with product and engineering teams",
            "Develop wireframes, prototypes, and high-fidelity mockups",
            "Ensure design consistency across all products"
        ],
        requirements: [
            "3+ years of UX/UI design experience",
            "Mastery of Figma or similar design tools",
            "Strong understanding of design principles and typography",
            "Experience building design systems",
            "Portfolio demonstrating your design work",
            "Knowledge of user-centered design methodologies",
            "Excellent communication skills"
        ],
        about: "DesignStudio is a creative design agency working with Fortune 500 companies and innovative startups. We're passionate about creating products that delight users."
    }
};

// Get job ID from URL
function getJobId() {
    const params = new URLSearchParams(window.location.search);
    return parseInt(params.get('id')) || 1;
}

// Render job details
async function renderJobDetails() {
    const jobId = getJobId();
    let job = null;

    // Prefer real data from Django.
    try {
        const res = await fetch(`/api/jobs/${jobId}/`);
        if (res.ok) job = await res.json();
    } catch (err) {
        // Ignore and fallback to mock.
        console.warn('Could not load job details from API, using fallback mock data.', err);
    }

    if (!job) job = jobsDatabase[jobId];

    if (!job) {
        document.body.innerHTML = '<div class="container" style="text-align: center; padding: 3rem;"><h2>Job not found</h2><a href="/jobs/" class="btn-primary">Back to Jobs</a></div>';
        return;
    }

    // Render header
    const headerEl = document.getElementById('jobHeader');
    if (headerEl) {
        headerEl.innerHTML = `
            <div style="display: flex; gap: 1.5rem; align-items: start; margin-bottom: 2rem;">
                <div class="company-logo-large" style="width: 80px; height: 80px; margin: 0;">${job.logo}</div>
                <div style="flex: 1;">
                    <h1>${job.title}</h1>
                    <p style="margin-bottom: 1rem; color: var(--text-secondary);">${job.company}</p>
                    <div class="job-meta" style="margin-bottom: 0;">
                        <span class="meta-item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                                <circle cx="12" cy="10" r="3"></circle>
                            </svg>
                            ${job.location}
                        </span>
                        <span class="meta-item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                                <line x1="16" y1="2" x2="16" y2="6"></line>
                                <line x1="8" y1="2" x2="8" y2="6"></line>
                                <line x1="3" y1="10" x2="21" y2="10"></line>
                            </svg>
                            ${job.posted}
                        </span>
                        <span class="meta-item">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="1"></circle>
                                <path d="M12 1v6m0 6v6"></path>
                                <path d="M4.22 4.22l4.24 4.24m-4.24 7.08l4.24 4.24M19.78 4.22l-4.24 4.24m4.24 7.08l-4.24 4.24"></path>
                            </svg>
                            ${job.type}
                        </span>
                    </div>
                </div>
            </div>
        `;
    }

    // Render description
    const descEl = document.getElementById('jobDescription');
    if (descEl) {
        descEl.innerHTML = job.description;
    }

    // Render responsibilities
    const respEl = document.getElementById('responsibilities');
    if (respEl) {
        const responsibilities = job.responsibilities || [];
        respEl.innerHTML = responsibilities.map(item => `<li>${item}</li>`).join('');
    }

    // Render requirements
    const reqEl = document.getElementById('requirements');
    if (reqEl) {
        const requirements = job.requirements || [];
        reqEl.innerHTML = requirements.map(item => `<li>${item}</li>`).join('');
    }

    // Render sidebar
    const sidebarEl = document.getElementById('sidebarContent');
    if (sidebarEl) {
        sidebarEl.innerHTML = `
            <div style="margin-bottom: 1.5rem;">
                <div style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.5rem;">Salary Range</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: var(--primary);">${job.salary}</div>
            </div>
            <div style="margin-bottom: 1.5rem;">
                <div style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.5rem;">Location</div>
                <div style="font-size: 1.125rem; font-weight: 600;">${job.location}</div>
            </div>
            <div style="margin-bottom: 1.5rem;">
                <div style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.5rem;">Job Type</div>
                <div style="font-size: 1.125rem; font-weight: 600;">${job.type}</div>
            </div>
            <div>
                <div style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.75rem;">Skills</div>
                <div class="job-tags">
                    ${job.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            </div>
        `;
    }

    // Render company card
    const companyEl = document.getElementById('companyCard');
    if (companyEl) {
        const aboutText = job.about || jobsDatabase[jobId]?.about || 'A great company with amazing opportunities.';
        companyEl.innerHTML = `
            <div class="company-logo-large">${job.logo}</div>
            <h3>${job.company}</h3>
            <p style="margin-bottom: 1rem;">${aboutText}</p>
            <button class="btn-secondary btn-full" onclick="window.location.href='/companies/'">View All Jobs</button>
        `;
    }

    // Render related jobs
    const relatedEl = document.getElementById('relatedJobs');
    if (relatedEl) {
        const relatedJobs = job.related_jobs && Array.isArray(job.related_jobs)
            ? job.related_jobs
            : Object.values(jobsDatabase)
                .filter(j => j.company === job.company && j.id !== jobId)
                .slice(0, 3);

        if (relatedJobs.length === 0) {
            relatedEl.innerHTML = '<p style="color: var(--text-secondary);">No other jobs from this company at the moment.</p>';
        } else {
            relatedEl.innerHTML = relatedJobs.map(relatedJob => `
                <div class="job-card" onclick="window.location.href='/job-details/?id=${relatedJob.id}'" style="cursor: pointer;">
                    <div class="job-title">${relatedJob.title}</div>
                    <div style="color: var(--text-secondary); margin-bottom: 0.75rem;">${relatedJob.location}</div>
                    <div style="color: var(--primary); font-weight: 600;">${relatedJob.salary}</div>
                </div>
            `).join('');
        }
    }

    // Setup buttons
    document.getElementById('applyBtn')?.addEventListener('click', () => {
        alert('Thank you for your interest! In a real application, this would redirect to an application form.');
    });

    document.getElementById('saveBtn')?.addEventListener('click', function() {
        toggleSaveJob(jobId);
        this.classList.toggle('saved');
        this.textContent = this.classList.contains('saved') ? '✓ Saved' : 'Save Job';
    });

    // Check if job is saved
    const savedJobs = JSON.parse(localStorage.getItem('savedJobs') || '[]');
    if (savedJobs.includes(jobId)) {
        const saveBtn = document.getElementById('saveBtn');
        if (saveBtn) {
            saveBtn.classList.add('saved');
            saveBtn.innerHTML = '✓ Saved';
        }
    }
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

// Share job
function shareJob(platform) {
    const jobId = getJobId();
    const job = jobsDatabase[jobId];
    const url = window.location.href;
    const text = `Check out this job: ${job.title} at ${job.company}`;

    let shareUrl = '';
    
    if (platform === 'twitter') {
        shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`;
    } else if (platform === 'linkedin') {
        shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
    } else if (platform === 'email') {
        shareUrl = `mailto:?subject=${encodeURIComponent(text)}&body=${encodeURIComponent(url)}`;
    }

    if (shareUrl) {
        window.open(shareUrl, '_blank');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    renderJobDetails();
});
