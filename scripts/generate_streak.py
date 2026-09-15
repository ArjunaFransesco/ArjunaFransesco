import json
import subprocess
import os
from datetime import datetime, timedelta

def generate_streak_card():
    query = """
    query {
      user(login: "ArjunaFransesco") {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """

    res = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={query}'], capture_output=True, text=True, check=True)
    cal = json.loads(res.stdout)['data']['user']['contributionsCollection']['contributionCalendar']
    total = cal['totalContributions']
    days = [d for w in cal['weeks'] for d in w['contributionDays']]
    days = sorted(days, key=lambda x: x['date'])

    today_str = datetime.now().strftime('%Y-%m-%d')

    max_streak = 0
    longest_streak_days = []
    temp_streak_days = []

    for d in days:
        if d['date'] > today_str:
            continue
        if d['contributionCount'] > 0:
            temp_streak_days.append(d)
            if len(temp_streak_days) > max_streak:
                max_streak = len(temp_streak_days)
                longest_streak_days = list(temp_streak_days)
        else:
            temp_streak_days = []

    current_streak_days = []
    for d in reversed(days):
        if d['date'] > today_str:
            continue
        if d['date'] == today_str and d['contributionCount'] == 0:
            continue
        if d['contributionCount'] > 0:
            current_streak_days.append(d)
        else:
            break

    cur_streak = len(current_streak_days)

    def fmt_range(start_str, end_str):
        if not start_str or not end_str:
            return "Active"
        d1 = datetime.strptime(start_str, "%Y-%m-%d")
        d2 = datetime.strptime(end_str, "%Y-%m-%d")
        m1 = d1.strftime("%b %d")
        m2 = d2.strftime("%b %d")
        return f"{m1} - {m2}"

    total_range = f"{datetime.strptime(days[0]['date'], '%Y-%m-%d').strftime('%b %d, %Y')} - Present"
    cur_range = fmt_range(current_streak_days[-1]['date'], current_streak_days[0]['date']) if current_streak_days else "No Active Streak"
    long_range = fmt_range(longest_streak_days[0]['date'], longest_streak_days[-1]['date']) if longest_streak_days else "No Data"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195" fill="none">
  <style>
    .header {{ font: 600 14px 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; fill: #70a5fd; }}
    .stat {{ font: 700 28px 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; fill: #38bdf8; }}
    .stat-current {{ font: 800 32px 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; fill: #bf91f3; }}
    .date {{ font: 400 11px 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; fill: #787c99; }}
    .ring {{ stroke: #bf91f3; stroke-width: 4; stroke-linecap: round; }}
  </style>
  <rect width="495" height="195" rx="12" fill="#1a1b27" />
  
  <!-- Total Contributions -->
  <g transform="translate(82, 48)" text-anchor="middle">
    <text class="stat" x="0" y="32">{total}</text>
    <text class="header" x="0" y="58">Total Contributions</text>
    <text class="date" x="0" y="80">{total_range}</text>
  </g>

  <!-- Divider 1 -->
  <line x1="165" y1="28" x2="165" y2="167" stroke="#2c2e43" stroke-width="1" />

  <!-- Current Streak (Highlighted) -->
  <g transform="translate(247, 36)" text-anchor="middle">
    <circle cx="0" cy="40" r="32" fill="none" stroke="#2c2e43" stroke-width="4" />
    <circle cx="0" cy="40" r="32" fill="none" class="ring" stroke-dasharray="160 40" stroke-dashoffset="20" />
    <text class="stat-current" x="0" y="51">{cur_streak}</text>
    <text class="header" x="0" y="94">Current Streak</text>
    <text class="date" x="0" y="112">{cur_range}</text>
  </g>

  <!-- Divider 2 -->
  <line x1="330" y1="28" x2="330" y2="167" stroke="#2c2e43" stroke-width="1" />

  <!-- Longest Streak -->
  <g transform="translate(412, 48)" text-anchor="middle">
    <text class="stat" x="0" y="32">{max_streak}</text>
    <text class="header" x="0" y="58">Longest Streak</text>
    <text class="date" x="0" y="80">{long_range}</text>
  </g>
</svg>'''

    output_dir = r"D:\Project\ArjunaFransesco\assets"
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, "streak-stats.svg")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated: {out_file}")

if __name__ == "__main__":
    generate_streak_card()
