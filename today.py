#!/usr/bin/env python3
"""
GitHub Profile README Generator
Fetches GitHub stats and generates themed SVG graphics
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any
import os
import html


class GitHubStats:
    def __init__(self, username: str, token: str = None):
        self.username = username
        self.token = token
        self.headers = {}
        if token:
            self.headers['Authorization'] = f'token {token}'

    def fetch_user_data(self) -> Dict[str, Any]:
        """Fetch basic user information"""
        url = f'https://api.github.com/users/{self.username}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_repos(self) -> list:
        """Fetch all user repositories"""
        repos = []
        page = 1
        while True:
            url = f'https://api.github.com/users/{self.username}/repos?per_page=100&page={page}'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            repos.extend(data)
            page += 1
        return repos

    def calculate_stats(self) -> Dict[str, Any]:
        """Calculate GitHub statistics"""
        user_data = self.fetch_user_data()
        repos = self.fetch_repos()

        # Filter out forked repos for some stats
        owned_repos = [r for r in repos if not r['fork']]

        # Calculate stars
        total_stars = sum(r['stargazers_count'] for r in owned_repos)

        # Calculate languages
        languages = {}
        for repo in owned_repos:
            if repo['language']:
                languages[repo['language']] = languages.get(repo['language'], 0) + 1

        # Get top languages
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]

        stats = {
            'username': self.username,
            'name': user_data.get('name', self.username),
            'bio': user_data.get('bio', ''),
            'followers': user_data['followers'],
            'following': user_data['following'],
            'public_repos': user_data['public_repos'],
            'total_stars': total_stars,
            'top_languages': top_languages,
            'updated_at': datetime.now().strftime('%B %d, %Y at %I:%M %p UTC')
        }

        return stats


def generate_svg(stats: Dict[str, Any], theme: str = 'light') -> str:
    """Generate terminal-style SVG graphic with stats"""

    # Theme colors
    if theme == 'light':
        bg_color = '#f6f8fa'
        text_color = '#24292f'
        key_color = '#953800'  # Rust brown for keys
        value_color = '#0a3069'  # Deep blue for values
        border_color = '#d0d7de'
        ascii_color = '#24292f'
        comment_color = '#c2cfde'
    else:  # dark
        bg_color = '#0d1117'
        text_color = '#c9d1d9'
        key_color = '#f0883e'  # Orange for keys
        value_color = '#58a6ff'  # Light blue for values
        border_color = '#30363d'
        ascii_color = '#c9d1d9'
        comment_color = '#8b949e'

    # No ASCII art - clean minimal design
    ascii_lines = []

    # Generate info lines (terminal style)
    info_lines = []
    y_start = 100
    line_height = 24

    # Use username if name is not set
    display_name = stats['name'] if stats['name'] else stats['username']

    info_data = [
        ('', f"{stats['username']}@github", text_color),  # Username header
        ('-' * 50, '', comment_color),  # Separator
        ('Name', display_name, None),
        ('Role', 'Senior Security Engineer', None),
        ('Certs', 'CCSP | CISSP', None),
        ('', '', text_color),  # Empty line
    ]

    # Add core skills - expanded
    info_data.extend([
        ('Security', '', None),
        ('', '  • DevSecOps & Security Architecture', None),
        ('', '  • Cloud Security (AWS, Azure)', None),
        ('', '  • Threat Modeling & Risk Assessment', None),
        ('', '  • Incident Response & Investigation', None),
        ('', '  • Container Security & Orchestration', None),
        ('', '  • Vulnerability Management', None),
        ('', '  • Application Security', None),
        ('', '  • Compliance & Standards Development', None),
        ('', '', text_color),  # Empty line
    ])

    # Add languages section
    info_data.extend([
        ('Languages', '', None),
        ('', '  • Python | PowerShell | Bash', None),
    ])

    # Add detected languages from repos
    if stats['top_languages']:
        for lang, count in stats['top_languages'][:5]:
            if lang.lower() not in ['python']:  # Avoid duplicates
                info_data.append(('', f"  • {lang}", None))

    info_data.extend([
        ('', '', text_color),
    ])

    # Add tools & platforms
    info_data.extend([
        ('Tools', '', None),
        ('', '  • IAM & Identity Management', None),
        ('', '  • SIEM & Log Analysis', None),
        ('', '  • Security Automation & CI/CD', None),
        ('', '  • Containers & Kubernetes', None),
        ('', '  • Infrastructure as Code', None),
    ])

    for i, (key, value, custom_color) in enumerate(info_data):
        y_pos = y_start + (i * line_height)

        if custom_color:
            # Special formatting (separator or empty line)
            info_lines.append(f'<text x="50" y="{y_pos}" class="comment">{html.escape(key)}</text>')
        elif key == '':
            # Value only (for languages list or header)
            info_lines.append(f'<text x="50" y="{y_pos}" class="value">{html.escape(value)}</text>')
        else:
            # Key-value pair
            info_lines.append(f'<text x="50" y="{y_pos}" class="key">{html.escape(key)}:</text>')
            info_lines.append(f'<text x="250" y="{y_pos}" class="value">{html.escape(value)}</text>')

    # Join all lines
    info_lines_svg = '\n        '.join(info_lines)

    svg = f'''<svg width="900" height="750" xmlns="http://www.w3.org/2000/svg">
    <style>
        text {{
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 16px;
        }}
        .ascii {{
            fill: {ascii_color};
            font-size: 14px;
            white-space: pre;
        }}
        .key {{
            fill: {key_color};
            font-weight: 600;
        }}
        .value {{
            fill: {value_color};
        }}
        .comment {{
            fill: {comment_color};
        }}
        .header {{
            fill: {text_color};
            font-weight: 700;
            font-size: 18px;
        }}
        .footer {{
            fill: {comment_color};
            font-size: 12px;
        }}
    </style>

    <!-- Background -->
    <rect width="900" height="750" fill="{bg_color}" rx="10"/>
    <rect width="880" height="730" x="10" y="10" fill="{bg_color}" stroke="{border_color}" stroke-width="2" rx="8"/>

    <!-- Title -->
    <text x="50" y="60" class="header">💻 {html.escape(display_name)}'s GitHub Profile</text>

    <!-- Info Section -->
    <g>
        {info_lines_svg}
    </g>

    <!-- Footer -->
    <text x="50" y="720" class="footer">Last updated: {html.escape(stats['updated_at'])}</text>
</svg>'''

    return svg


def main():
    username = 'kholcomb'
    token = os.getenv('GITHUB_TOKEN')

    print(f"Fetching GitHub stats for @{username}...")

    try:
        gh = GitHubStats(username, token)
        stats = gh.calculate_stats()

        print(f"✓ Found {stats['public_repos']} repositories")
        print(f"✓ Total stars: {stats['total_stars']}")
        print(f"✓ Followers: {stats['followers']}")

        # Generate SVGs
        print("\nGenerating SVG graphics...")

        light_svg = generate_svg(stats, 'light')
        with open('light_mode.svg', 'w', encoding='utf-8') as f:
            f.write(light_svg)
        print("✓ Generated light_mode.svg")

        dark_svg = generate_svg(stats, 'dark')
        with open('dark_mode.svg', 'w', encoding='utf-8') as f:
            f.write(dark_svg)
        print("✓ Generated dark_mode.svg")

        # Save stats cache
        os.makedirs('cache', exist_ok=True)
        with open('cache/stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
        print("✓ Saved stats cache")

        print("\n✅ All done!")

    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == '__main__':
    main()
