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

    def fetch_language_stats(self, repos: list) -> Dict[str, int]:
        """Fetch detailed language statistics by bytes"""
        language_bytes = {}
        for repo in repos:
            if repo['fork']:
                continue
            url = repo['languages_url']
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                lang_data = response.json()
                for lang, bytes_count in lang_data.items():
                    language_bytes[lang] = language_bytes.get(lang, 0) + bytes_count
            except Exception as e:
                print(f"Warning: Could not fetch languages for {repo['name']}: {e}")
        return language_bytes

    def calculate_stats(self) -> Dict[str, Any]:
        """Calculate GitHub statistics"""
        user_data = self.fetch_user_data()
        repos = self.fetch_repos()

        # Filter out forked repos for some stats
        owned_repos = [r for r in repos if not r['fork']]

        # Calculate stars
        total_stars = sum(r['stargazers_count'] for r in owned_repos)

        # Get top repositories by stars
        top_repos = sorted(owned_repos, key=lambda x: x['stargazers_count'], reverse=True)[:3]
        top_repos_data = [
            {
                'name': r['name'],
                'description': r['description'] or 'No description',
                'stars': r['stargazers_count'],
                'language': r['language'] or 'N/A'
            }
            for r in top_repos
        ]

        # Calculate languages with byte counts
        print("Fetching language statistics...")
        language_bytes = self.fetch_language_stats(repos)

        # Calculate percentages
        total_bytes = sum(language_bytes.values())
        language_percentages = []
        if total_bytes > 0:
            for lang, bytes_count in sorted(language_bytes.items(), key=lambda x: x[1], reverse=True)[:5]:
                percentage = (bytes_count / total_bytes) * 100
                language_percentages.append((lang, percentage))

        stats = {
            'username': self.username,
            'name': user_data.get('name', self.username),
            'bio': user_data.get('bio', ''),
            'followers': user_data['followers'],
            'following': user_data['following'],
            'public_repos': user_data['public_repos'],
            'total_stars': total_stars,
            'language_percentages': language_percentages,
            'top_repos': top_repos_data,
            'updated_at': datetime.now().strftime('%B %d, %Y at %I:%M %p UTC')
        }

        return stats


def generate_svg(stats: Dict[str, Any], theme: str = 'light') -> str:
    """Generate terminal-style SVG graphic with stats"""

    # Theme colors - Solarized
    if theme == 'light':
        # Solarized Light
        bg_color = '#fdf6e3'  # base3
        text_color = '#657b83'  # base00
        key_color = '#cb4b16'  # orange for keys
        value_color = '#268bd2'  # blue for values
        border_color = '#93a1a1'  # base1
        ascii_color = '#657b83'  # base00
        comment_color = '#93a1a1'  # base1
        chart_colors = ['#268bd2', '#859900', '#b58900', '#dc322f', '#6c71c4']  # blue, green, yellow, red, violet
    else:  # dark - Solarized Dark
        bg_color = '#002b36'  # base03
        text_color = '#839496'  # base0
        key_color = '#cb4b16'  # orange for keys
        value_color = '#268bd2'  # blue for values
        border_color = '#586e75'  # base01
        ascii_color = '#839496'  # base0
        comment_color = '#586e75'  # base01
        chart_colors = ['#268bd2', '#859900', '#b58900', '#dc322f', '#6c71c4']  # blue, green, yellow, red, violet

    # Use username if name is not set
    display_name = stats['name'] if stats['name'] else stats['username']

    y_start = 100
    line_height = 24
    left_x = 50
    right_x = 480

    # Box drawing characters for riced CLI aesthetic
    box_top_left = '╭'
    box_top_right = '╮'
    box_bottom_left = '╰'
    box_bottom_right = '╯'
    box_horizontal = '─'
    box_vertical = '│'
    box_divider = '├─────────────────────────────────────────────────────────────────────────────────────╮'

    # LEFT COLUMN DATA
    left_column_data = [
        ('', f"{stats['username']}@github", text_color),  # Username header
        ('separator', '─' * 50, comment_color),  # Separator
        ('Name', display_name, None),
        ('Role', 'Senior Security Engineer', None),
        ('TimeZone', 'Pacific Standard Time', None),
        ('Certs', 'CCSP | CISSP (ISC2 #521659)', None),
        ('Status', 'Open to opportunities', None),
        ('divider', '', None),  # Section divider
        ('Interests', '', None),
        ('', '  • AI/LLM Security &', None),
        ('', '    Safety Engineering', None),
        ('', '  • Security Automation &', None),
        ('', '    DevSecOps', None),
        ('', '  • Cloud-Native Security', None),
        ('', '    Architecture', None),
        ('', '  • DevSecOps & Security', None),
        ('', '    Architecture', None),
        ('', '  • Cloud Security', None),
        ('', '    (AWS, Azure)', None),
        ('', '  • Threat Modeling &', None),
        ('', '    Risk Assessment', None),
        ('', '  • Incident Response &', None),
        ('', '    Investigation', None),
    ]

    # RIGHT COLUMN DATA
    right_column_data = [
        ('', '', text_color),  # Empty line to align with separator
        ('', '', text_color),  # Empty line
        ('', '', text_color),  # Empty line
        ('', '', text_color),  # Empty line
        ('', '', text_color),  # Empty line
        ('', '', text_color),  # Empty line
        ('', '', text_color),  # Empty line
        ('', '', text_color),  # Empty line to align with Interests header
        ('', '', text_color),  # Empty line
        ('', '  • Container Security &', None),
        ('', '    Orchestration', None),
        ('', '  • Vulnerability Management', None),
        ('', '  • Application Security', None),
        ('', '  • Compliance & Standards', None),
        ('', '    Development', None),
        ('', '  • IAM & Identity Management', None),
        ('', '  • SIEM & Log Analysis', None),
        ('', '  • Security Automation', None),
        ('', '    & CI/CD', None),
        ('', '  • Containers & Kubernetes', None),
        ('', '  • Infrastructure as Code', None),
    ]

    # Generate left column
    info_lines = []
    for i, (key, value, custom_color) in enumerate(left_column_data):
        y_pos = y_start + (i * line_height)

        if key == 'divider':
            # Add visual section divider
            info_lines.append(f'<text x="{left_x}" y="{y_pos}" class="comment">{"─" * 40}</text>')
        elif key == 'separator':
            info_lines.append(f'<text x="{left_x}" y="{y_pos}" class="comment">{html.escape(value)}</text>')
        elif custom_color:
            info_lines.append(f'<text x="{left_x}" y="{y_pos}" class="comment">{html.escape(key)}</text>')
        elif key == '':
            info_lines.append(f'<text x="{left_x}" y="{y_pos}" class="value">{html.escape(value)}</text>')
        else:
            info_lines.append(f'<text x="{left_x}" y="{y_pos}" class="key">{html.escape(key)}:</text>')
            if value:
                info_lines.append(f'<text x="{left_x + 200}" y="{y_pos}" class="value">{html.escape(value)}</text>')

    # Generate right column
    for i, (key, value, custom_color) in enumerate(right_column_data):
        y_pos = y_start + (i * line_height)

        if key == 'divider':
            # Add visual section divider
            info_lines.append(f'<text x="{right_x}" y="{y_pos}" class="comment">{"─" * 40}</text>')
        elif key == 'separator':
            if value:
                info_lines.append(f'<text x="{right_x}" y="{y_pos}" class="comment">{html.escape(value)}</text>')
        elif custom_color:
            if key:  # Only add if not empty placeholder
                info_lines.append(f'<text x="{right_x}" y="{y_pos}" class="comment">{html.escape(key)}</text>')
        elif key == '':
            if value:  # Only add if not empty placeholder
                info_lines.append(f'<text x="{right_x}" y="{y_pos}" class="value">{html.escape(value)}</text>')
        else:
            info_lines.append(f'<text x="{right_x}" y="{y_pos}" class="key">{html.escape(key)}:</text>')
            if value:
                info_lines.append(f'<text x="{right_x + 120}" y="{y_pos}" class="value">{html.escape(value)}</text>')

    # Join all lines
    info_lines_svg = '\n        '.join(info_lines)

    # Calculate end of columns
    column_end_y = y_start + (max(len(left_column_data), len(right_column_data)) * line_height)

    # Generate language chart
    lang_chart_svg = []
    chart_end_y = column_end_y

    if stats['language_percentages']:
        chart_y = chart_end_y + 40
        # Box top
        lang_chart_svg.append(f'<text x="50" y="{chart_y}" class="comment">╭{"─" * 82}╮</text>')
        lang_chart_svg.append(f'<text x="50" y="{chart_y + 20}" class="comment">│</text>')
        lang_chart_svg.append(f'<text x="60" y="{chart_y + 20}" class="key">Language Distribution</text>')
        lang_chart_svg.append(f'<text x="830" y="{chart_y + 20}" class="comment">│</text>')
        lang_chart_svg.append(f'<text x="50" y="{chart_y + 35}" class="comment">├{"─" * 82}┤</text>')

        chart_start_y = chart_y + 55
        bar_height = 20
        max_bar_width = 400

        for i, (lang, percentage) in enumerate(stats['language_percentages']):
            bar_y = chart_start_y + (i * (bar_height + 10))
            bar_width = (percentage / 100) * max_bar_width
            color = chart_colors[i % len(chart_colors)]

            # Box side
            lang_chart_svg.append(f'<text x="50" y="{bar_y + 14}" class="comment">│</text>')
            # Bar
            lang_chart_svg.append(f'<rect x="70" y="{bar_y}" width="{bar_width}" height="{bar_height}" fill="{color}" rx="3"/>')
            # Language name and percentage
            lang_chart_svg.append(f'<text x="80" y="{bar_y + 14}" class="header" style="font-size: 12px; fill: {bg_color}">{html.escape(lang)}</text>')
            lang_chart_svg.append(f'<text x="{max_bar_width + 80}" y="{bar_y + 14}" class="value" style="font-size: 12px">{percentage:.1f}%</text>')
            lang_chart_svg.append(f'<text x="830" y="{bar_y + 14}" class="comment">│</text>')

        chart_end_y = bar_y + bar_height + 10
        # Box bottom
        lang_chart_svg.append(f'<text x="50" y="{chart_end_y + 15}" class="comment">╰{"─" * 82}╯</text>')
        chart_end_y += 25

    lang_chart_svg_str = '\n    '.join(lang_chart_svg)

    # Generate project highlights
    project_highlights_svg = []
    project_end_y = chart_end_y

    if stats['top_repos']:
        highlights_y = chart_end_y + 40
        # Box top
        project_highlights_svg.append(f'<text x="50" y="{highlights_y}" class="comment">╭{"─" * 82}╮</text>')
        project_highlights_svg.append(f'<text x="50" y="{highlights_y + 20}" class="comment">│</text>')
        project_highlights_svg.append(f'<text x="60" y="{highlights_y + 20}" class="key">Project Highlights</text>')
        project_highlights_svg.append(f'<text x="830" y="{highlights_y + 20}" class="comment">│</text>')
        project_highlights_svg.append(f'<text x="50" y="{highlights_y + 35}" class="comment">├{"─" * 82}┤</text>')

        proj_y = highlights_y + 55
        for i, repo in enumerate(stats['top_repos']):
            if i >= 3:  # Limit to 3 repos
                break
            y_offset = proj_y + (i * 65)

            # Add divider between projects
            if i > 0:
                project_highlights_svg.append(f'<text x="50" y="{y_offset - 10}" class="comment">├{"─" * 82}┤</text>')

            # Box sides for repo entry
            project_highlights_svg.append(f'<text x="50" y="{y_offset}" class="comment">│</text>')
            # Repo name with stars
            stars_text = f"★ {repo['stars']}" if repo['stars'] > 0 else ""
            project_highlights_svg.append(f'<text x="60" y="{y_offset}" class="value" style="font-weight: 600">{html.escape(repo["name"])} <tspan class="comment">{stars_text}</tspan></text>')
            project_highlights_svg.append(f'<text x="830" y="{y_offset}" class="comment">│</text>')

            project_highlights_svg.append(f'<text x="50" y="{y_offset + 20}" class="comment">│</text>')
            # Description (truncate if too long)
            desc = repo['description'][:70] + '...' if len(repo['description']) > 70 else repo['description']
            project_highlights_svg.append(f'<text x="60" y="{y_offset + 20}" class="comment" style="font-size: 13px">{html.escape(desc)}</text>')
            project_highlights_svg.append(f'<text x="830" y="{y_offset + 20}" class="comment">│</text>')

            project_highlights_svg.append(f'<text x="50" y="{y_offset + 38}" class="comment">│</text>')
            # Language tag
            project_highlights_svg.append(f'<text x="60" y="{y_offset + 38}" class="key" style="font-size: 11px">{html.escape(repo["language"])}</text>')
            project_highlights_svg.append(f'<text x="830" y="{y_offset + 38}" class="comment">│</text>')

            project_end_y = y_offset + 50

        # Box bottom
        project_highlights_svg.append(f'<text x="50" y="{project_end_y + 15}" class="comment">╰{"─" * 82}╯</text>')
        project_end_y += 25

    project_highlights_svg_str = '\n    '.join(project_highlights_svg)

    # Calculate total height based on actual content
    footer_y = project_end_y + 40
    total_height = footer_y + 60

    svg = f'''<svg width="900" height="{total_height}" xmlns="http://www.w3.org/2000/svg">
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
    <rect width="900" height="{total_height}" fill="{bg_color}" rx="10"/>
    <rect width="880" height="{total_height - 20}" x="10" y="10" fill="{bg_color}" stroke="{border_color}" stroke-width="2" rx="8"/>

    <!-- Title -->
    <text x="50" y="60" class="header">{html.escape(display_name)}'s GitHub Profile</text>

    <!-- Info Section -->
    <g>
        {info_lines_svg}
    </g>

    <!-- Language Chart -->
    <g>
        {lang_chart_svg_str}
    </g>

    <!-- Project Highlights -->
    <g>
        {project_highlights_svg_str}
    </g>

    <!-- Footer -->
    <text x="50" y="{footer_y}" class="footer">Last updated: {html.escape(stats['updated_at'])}</text>
</svg>'''

    return svg


def update_readme_cache_busting(timestamp: str):
    """Update README.md with new cache-busting parameters"""
    readme_path = 'README.md'

    if not os.path.exists(readme_path):
        print(f"Warning: {readme_path} not found, skipping cache-busting update")
        return

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update all SVG references with new timestamp
    # Match patterns like: dark_mode.svg or dark_mode.svg?v=anything
    import re

    # Update dark mode SVG
    content = re.sub(
        r'dark_mode\.svg(\?v=[^"]+)?',
        f'dark_mode.svg?v={timestamp}',
        content
    )

    # Update light mode SVG
    content = re.sub(
        r'light_mode\.svg(\?v=[^"]+)?',
        f'light_mode.svg?v={timestamp}',
        content
    )

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated README.md cache-busting parameters to ?v={timestamp}")


def main():
    username = 'kholcomb'
    token = os.getenv('GITHUB_TOKEN')

    print(f"Fetching GitHub stats for @{username}...")

    try:
        gh = GitHubStats(username, token)
        stats = gh.calculate_stats()

        print(f"Found {stats['public_repos']} repositories")
        print(f"Total stars: {stats['total_stars']}")
        print(f"Followers: {stats['followers']}")

        # Generate SVGs
        print("\nGenerating SVG graphics...")

        light_svg = generate_svg(stats, 'light')
        with open('light_mode.svg', 'w', encoding='utf-8') as f:
            f.write(light_svg)
        print("Generated light_mode.svg")

        dark_svg = generate_svg(stats, 'dark')
        with open('dark_mode.svg', 'w', encoding='utf-8') as f:
            f.write(dark_svg)
        print("Generated dark_mode.svg")

        # Save stats cache
        os.makedirs('cache', exist_ok=True)
        with open('cache/stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
        print("Saved stats cache")

        # Update README with cache-busting parameters
        # Use a simpler timestamp format for the query parameter
        cache_timestamp = datetime.now().strftime('%Y-%m-%d-%H%M')
        update_readme_cache_busting(cache_timestamp)

        print("\nAll done!")

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == '__main__':
    main()
