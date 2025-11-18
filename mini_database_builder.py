import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from typing import List, Dict

# List of 2025 races with details (name, URL ID, category notes). Expand as needed from https://www.classemini.com/?mode=courses
RACES = [
    {"name": "La Pornichet Select 2025", "id": 517, "category": "Solo", "url": "https://www.classemini.com/course-fr-517.html"},
    {"name": "Mini en Mai 2025", "id": 518, "category": "Solo", "url": "https://www.classemini.com/course-fr-518.html"},
    {"name": "Mini Fastnet 2025", "id": 520, "category": "Double", "url": "https://www.classemini.com/course-fr-520.html"},
    {"name": "Calvados Cup Course 2 2025", "id": 522, "category": "Solo", "url": "https://www.classemini.com/course-fr-522.html"},
    {"name": "La Boulangère Mini Transat 2025", "id": 524, "category": "Solo (Proto/Serie)", "url": "https://www.classemini.com/course-fr-524.html"},
    {"name": "Solo Med 2025", "id": 529, "category": "Solo", "url": "https://www.classemini.com/course-fr-529.html"},
    {"name": "Imperia Mini Solo 2025", "id": 531, "category": "Solo", "url": "https://www.classemini.com/course-fr-531.html"},
    {"name": "Mare Nostrum 2025", "id": 532, "category": "Double", "url": "https://www.classemini.com/course-fr-532.html"},
    {"name": "Puru Transgasconne 2025", "id": 536, "category": "Double", "url": "https://www.classemini.com/course-fr-536.html"},
    # Add more, e.g., {"name": "Trophée Marie Agnès Péron 2025", "id": 519, "category": "Solo", "url": "..."}  # Find ID via site
]

def scrape_race_results(url: str) -> List[Dict]:
    """
    Scrape a single race page for results.
    Parses the 'Classement' section (often <ol> or <table> with li/tr rows).
    Returns list of dicts: {'position': str, 'number': str, 'boat': str, 'skipper': str, 'time': str}
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return []
    
    soup = BeautifulSoup(response.content, 'lxml')
    results = []
    
    # Look for classement section (common patterns)
    classement = soup.find('div', string=lambda text: text and 'Classement' in text) or soup.find('h2', string=lambda text: text and 'Classement' in text)
    if not classement:
        # Fallback: search for ordered list or table with boat-like content
        ol = soup.find('ol') or soup.find('ul')
        if ol:
            for li in ol.find_all('li', recursive=True)[:50]:  # Limit to top ~50
                text = li.get_text(strip=True)
                if ' - ' in text and any(char.isdigit() for char in text.split('-')[0] if char != ' '):  # e.g., "1. 981 - Boat · Skipper"
                    parts = text.split(' - ', 1)
                    pos = parts[0].strip().split('.')[0].strip()
                    rest = parts[1].strip()
                    num_boat = rest.split(' · ')[0].strip()
                    skipper_time = ' · '.join(rest.split(' · ')[1:]).strip()
                    skipper, time_ = skipper_time.rsplit(' · ', 1) if ' · ' in skipper_time else (skipper_time, '')
                    results.append({
                        'position': pos,
                        'number': num_boat.split()[0] if num_boat else '',
                        'boat': num_boat.split(' ', 1)[1] if ' ' in num_boat else num_boat,
                        'skipper': skipper,
                        'time': time_
                    })
        return results
    
    # Parse siblings or children for list/table
    for elem in classement.find_next_siblings()[:20]:  # Next elements after header
        if elem.name in ['ol', 'ul', 'table']:
            if elem.name == 'table':
                rows = elem.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 4:
                        results.append({
                            'position': cells[0].get_text(strip=True),
                            'number': cells[1].get_text(strip=True),
                            'boat': cells[2].get_text(strip=True),
                            'skipper': cells[3].get_text(strip=True),
                            'time': cells[4].get_text(strip=True) if len(cells) > 4 else ''
                        })
            else:  # List
                for li in elem.find_all('li', recursive=True)[:50]:
                    # Same parsing as fallback
                    text = li.get_text(strip=True)
                    if len(text) > 10 and any(' - ' in text, ' | ' in text):
                        # Adjust split based on format
                        if ' - ' in text:
                            parts = text.split(' - ', 1)
                            pos = parts[0].strip()
                            rest = parts[1]
                        else:
                            parts = text.split(' | ')
                            pos = parts[0].strip()
                            rest = ' | '.join(parts[1:])
                        skipper_time = rest.split(' · ')[1:] if ' · ' in rest else rest.split(' - ')[1:]
                        skipper = ' & '.join(skipper_time[:-1]) if len(skipper_time) > 1 else skipper_time[0]
                        time_ = skipper_time[-1] if len(skipper_time) > 1 else ''
                        num_boat = rest.split()[0] + ' ' + ' '.join(rest.split()[1:rest.split().index(next((w for w in rest.split() if '·' in w), None))])
                        results.append({
                            'position': pos,
                            'number': num_boat.split()[0],
                            'boat': num_boat.split(' ', 1)[1] if len(num_boat.split()) > 1 else '',
                            'skipper': skipper,
                            'time': time_
                        })
            break  # Stop after first matching list/table
    
    return results

# Scrape all races
all_results = []
for race in RACES:
    print(f"Scraping {race['name']}...")
    results = scrape_race_results(race['url'])
    for res in results:
        res['race'] = race['name']
        res['category'] = race['category']
    all_results.extend(results)
    time.sleep(1)  # Rate limit

# Also scrape overall standings
print("Scraping overall standings...")
overall_url = "https://www.classemini.com/?mode=classement"
overall = requests.get(overall_url).text
soup_overall = BeautifulSoup(overall, 'lxml')
overall_results = []
# Parse top standings (adjust if needed for full list)
standings_text = soup_overall.find('div', class_='classement') or soup_overall.body
lines = standings_text.get_text().splitlines()
for line in lines:
    if '.' in line and 'pts' in line:
        parts = line.split('.', 1)
        pos = parts[0].strip()
        rest = parts[1].strip().split('pts')[0].strip()
        skipper = rest.split()[0] + ' ' + ' '.join(rest.split()[1:])
        points = line.split('pts')[1].strip() if 'pts' in line else ''
        overall_results.append({'position': pos, 'skipper': skipper, 'points': points, 'race': 'Overall Championship 2025', 'category': 'Overall'})

# Create DataFrame
df_results = pd.DataFrame(all_results)
df_overall = pd.DataFrame(overall_results)

# Export to Excel with multiple sheets
with pd.ExcelWriter('mini_2025_results.xlsx', engine='openpyxl') as writer:
    df_results.to_excel(writer, sheet_name='All Races', index=False)
    df_overall.to_excel(writer, sheet_name='Overall Standings', index=False)
    # Per-race sheets
    for race in RACES:
        race_df = df_results[df_results['race'] == race['name']]
        if not race_df.empty:
            race_df.to_excel(writer, sheet_name=race['name'][:31], index=False)  # Sheet name limit

print(f"Database built! Check 'mini_2025_results.xlsx' for {len(df_results)} entries across races + overall.")
print("Sample data:\n", df_results.head())
