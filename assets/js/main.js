(async function() {
    try {
        // Load data files
        const [resumeData, stats] = await Promise.all([
            fetch('cache/resume_data.json').then(r => r.json()),
            fetch('cache/stats.json').then(r => r.json())
        ]);

        // Populate bio - use textContent for security
        const bioEl = document.getElementById('bio');
        if (bioEl) bioEl.textContent = resumeData.personal.bio;

        // Populate skills using safe DOM methods
        const skillsGrid = document.getElementById('skills-grid');
        if (skillsGrid && resumeData.skills) {
            Object.entries(resumeData.skills).forEach(([category, skills]) => {
                const categoryDiv = document.createElement('div');
                categoryDiv.className = 'skill-category';

                const heading = document.createElement('h3');
                heading.textContent = category;
                categoryDiv.appendChild(heading);

                const list = document.createElement('ul');
                skills.forEach(skill => {
                    const li = document.createElement('li');
                    li.textContent = skill;
                    list.appendChild(li);
                });
                categoryDiv.appendChild(list);

                skillsGrid.appendChild(categoryDiv);
            });
        }

        // Populate projects using safe DOM methods
        const projectsGrid = document.getElementById('projects-grid');
        if (projectsGrid && stats.top_repos) {
            stats.top_repos.forEach(repo => {
                const card = document.createElement('div');
                card.className = 'project-card';

                const heading = document.createElement('h3');
                const link = document.createElement('a');
                link.href = repo.url;
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
                link.textContent = repo.name;
                heading.appendChild(link);
                card.appendChild(heading);

                const desc = document.createElement('p');
                desc.textContent = repo.description || 'No description available';
                card.appendChild(desc);

                const stars = document.createElement('span');
                stars.className = 'stars';
                stars.textContent = `⭐ ${repo.stars}`;
                card.appendChild(stars);

                projectsGrid.appendChild(card);
            });
        }

        // Populate certifications using safe DOM methods
        const certsList = document.getElementById('certs-list');
        if (certsList && resumeData.personal.certifications) {
            resumeData.personal.certifications.forEach(cert => {
                const certDiv = document.createElement('div');
                certDiv.className = 'cert-item';

                const certName = document.createElement('strong');
                certName.textContent = cert.name;
                certDiv.appendChild(certName);

                certDiv.appendChild(document.createTextNode(` - ${cert.issuer} `));

                const credential = document.createElement('span');
                credential.textContent = `(Credential: ${cert.credential})`;
                credential.style.color = 'var(--fg-secondary)';
                certDiv.appendChild(credential);

                certsList.appendChild(certDiv);
            });
        }

        // Update timestamp
        const lastUpdateEl = document.getElementById('last-update');
        if (lastUpdateEl && stats.updated_at) {
            const date = new Date(stats.updated_at);
            lastUpdateEl.textContent = date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }

    } catch (error) {
        console.error('Error loading data:', error);
        // Graceful degradation: static content still visible
        const bioEl = document.getElementById('bio');
        if (bioEl) {
            bioEl.textContent = 'Senior Security Engineer specializing in AI/LLM Security and Cloud Architecture';
        }
    }
})();
