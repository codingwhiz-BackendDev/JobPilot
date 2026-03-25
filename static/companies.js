/* ============================================
   COMPANIES PAGE LOGIC
   ============================================ */

const companiesData = [
    {
        id: 1,
        name: "TechCorp",
        logo: "TC",
        description: "Leading technology innovators building cloud solutions",
        jobs: 12,
        tags: ["SaaS", "Cloud", "Enterprise"],
        rating: 4.8,
        founded: 2015
    },
    {
        id: 2,
        name: "StartupXYZ",
        logo: "SX",
        description: "Next-gen SaaS platform for businesses",
        jobs: 8,
        tags: ["SaaS", "Startup", "B2B"],
        rating: 4.6,
        founded: 2021
    },
    {
        id: 3,
        name: "DesignStudio",
        logo: "DS",
        description: "Creative design agency focused on user experience",
        jobs: 5,
        tags: ["Design", "Agency", "Creative"],
        rating: 4.7,
        founded: 2018
    },
    {
        id: 4,
        name: "CloudTech",
        logo: "CT",
        description: "Cloud infrastructure leader powering millions",
        jobs: 15,
        tags: ["Cloud", "Infrastructure", "Enterprise"],
        rating: 4.9,
        founded: 2010
    },
    {
        id: 5,
        name: "InnovateCo",
        logo: "IC",
        description: "AI and ML innovators transforming industries",
        jobs: 10,
        tags: ["AI", "Machine Learning", "Research"],
        rating: 4.8,
        founded: 2019
    },
    {
        id: 6,
        name: "InfraScale",
        logo: "IS",
        description: "Infrastructure automation and DevOps solutions",
        jobs: 7,
        tags: ["DevOps", "Infrastructure", "Tools"],
        rating: 4.5,
        founded: 2017
    },
    {
        id: 7,
        name: "DataInsight",
        logo: "DI",
        description: "Data analytics and business intelligence",
        jobs: 6,
        tags: ["Analytics", "Data", "Business"],
        rating: 4.7,
        founded: 2016
    },
    {
        id: 8,
        name: "SecureVault",
        logo: "SV",
        description: "Cybersecurity solutions for enterprises",
        jobs: 9,
        tags: ["Security", "Enterprise", "SaaS"],
        rating: 4.8,
        founded: 2014
    },
    {
        id: 9,
        name: "MobileFirst",
        logo: "MF",
        description: "Mobile app development and consulting",
        jobs: 4,
        tags: ["Mobile", "iOS", "Android"],
        rating: 4.6,
        founded: 2020
    },
    {
        id: 10,
        name: "MediaHub",
        logo: "MH",
        description: "Content creation and digital media platform",
        jobs: 11,
        tags: ["Media", "Content", "Platform"],
        rating: 4.7,
        founded: 2018
    }
];

let filteredCompanies = [...companiesData];

// Render companies
function renderCompanies() {
    const container = document.getElementById('companiesGrid');
    if (!container) return;

    if (filteredCompanies.length === 0) {
        container.innerHTML = '<div style="text-align: center; padding: 3rem; grid-column: 1 / -1;"><p>No companies found matching your search.</p></div>';
        return;
    }

    container.innerHTML = filteredCompanies.map(company => `
        <div class="company-card animate-cardEntrance hover-lift" onclick="viewCompanyDetails(${company.id})">
            <div class="company-logo-large">${company.logo}</div>
            <div class="company-name-large">${company.name}</div>
            <div class="company-desc">${company.description}</div>
            
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; gap: 0.5rem; margin-bottom: 0.75rem;">
                    ${Array(Math.floor(company.rating)).fill('⭐').join('')}
                    <span style="color: var(--text-secondary); font-size: 0.9rem;">${company.rating}/5</span>
                </div>
            </div>

            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem;">
                ${company.tags.slice(0, 2).map(tag => `<span class="tag" style="font-size: 0.75rem;">${tag}</span>`).join('')}
            </div>

            <div class="company-stat">${company.jobs} open positions</div>
            
            <button class="btn-secondary btn-full" style="margin-top: 1rem;" onclick="event.stopPropagation(); viewCompanyJobs(${company.id})">View Jobs</button>
        </div>
    `).join('');

    // Add stagger animation
    container.classList.add('stagger');
}

// Search and filter
function filterCompanies() {
    const searchValue = document.getElementById('companySearch')?.value.toLowerCase() || '';
    const sortValue = document.getElementById('companySortBy')?.value || 'popular';

    let filtered = companiesData.filter(company => 
        company.name.toLowerCase().includes(searchValue) ||
        company.description.toLowerCase().includes(searchValue) ||
        company.tags.some(tag => tag.toLowerCase().includes(searchValue))
    );

    // Sort
    switch(sortValue) {
        case 'newest':
            filtered.sort((a, b) => b.founded - a.founded);
            break;
        case 'a-z':
            filtered.sort((a, b) => a.name.localeCompare(b.name));
            break;
        case 'jobs':
            filtered.sort((a, b) => b.jobs - a.jobs);
            break;
        case 'popular':
        default:
            filtered.sort((a, b) => b.rating - a.rating);
    }

    filteredCompanies = filtered;
    renderCompanies();
}

// View company details
function viewCompanyDetails(companyId) {
    const company = companiesData.find(c => c.id === companyId);
    if (company) {
        alert(`${company.name}\n\n${company.description}\n\nOpen positions: ${company.jobs}\nRating: ${company.rating}/5\n\nIn a real application, this would show detailed company information.`);
    }
}

// View company jobs
function viewCompanyJobs(companyId) {
    const company = companiesData.find(c => c.id === companyId);
    if (company) {
        window.location.href = `jobs.html?company=${company.name}`;
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('companySearch')?.addEventListener('input', filterCompanies);
    document.getElementById('companySortBy')?.addEventListener('change', filterCompanies);
    
    // Initial render
    filterCompanies();
});
