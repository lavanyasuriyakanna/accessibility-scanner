import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib3

# 🔥 Disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def analyze_webpage(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        # 🔥 Safe request
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()

    except Exception as e:
        return {
            "error": f"Failed to fetch webpage: {str(e)}",
            "score": 0,
            "issues": []
        }

    soup = BeautifulSoup(response.text, 'html.parser')
    issues = []

    # 🔥 IMPORT HERE (avoid circular error)
    try:
        from .ai_vision import generate_alt_text
    except:
        generate_alt_text = lambda x: "AI description unavailable"

    # =============================
    # ✅ CHECK 1: IMAGES ALT TEXT
    # =============================
    images = soup.find_all('img')
    images_without_alt = [img for img in images if not img.get('alt')]

    generated_descriptions = []

    if images_without_alt:
        issues.append({
            'type': 'danger',
            'message': f'{len(images_without_alt)} images missing alt text'
        })

        for img in images_without_alt[:3]:
            src = img.get('src')
            if src:
                abs_url = urljoin(url, src)

                try:
                    gen_alt = generate_alt_text(abs_url)
                except:
                    gen_alt = "AI failed"

                generated_descriptions.append(gen_alt)

        if generated_descriptions:
            issues.append({
                'type': 'success',
                'message': "AI Generated: " + " | ".join(generated_descriptions)
            })
    else:
        issues.append({
            'type': 'success',
            'message': 'All images have alt text'
        })

    # =============================
    # ✅ CHECK 2: LANDMARKS
    # =============================
    landmarks = ['header', 'main', 'footer', 'nav']
    found = [tag for tag in landmarks if soup.find(tag)]

    if len(found) < 2:
        issues.append({
            'type': 'warning',
            'message': f'Weak semantic structure: {", ".join(found) if found else "none"}'
        })
    else:
        issues.append({
            'type': 'success',
            'message': f'Semantic HTML OK: {", ".join(found)}'
        })

    # =============================
    # ✅ CHECK 3: H1 TAG
    # =============================
    h1_tags = soup.find_all('h1')

    if len(h1_tags) == 0:
        issues.append({
            'type': 'danger',
            'message': 'Missing H1 tag'
        })
    elif len(h1_tags) > 1:
        issues.append({
            'type': 'warning',
            'message': f'Multiple H1 tags ({len(h1_tags)})'
        })
    else:
        issues.append({
            'type': 'success',
            'message': 'Proper H1 structure'
        })

    # =============================
    # 🎯 SCORE CALCULATION
    # =============================
    score = 100

    for issue in issues:
        if issue['type'] == 'danger':
            score -= 15
        elif issue['type'] == 'warning':
            score -= 5

    score = max(0, score)

    return {
        "url": url,
        "score": score,
        "issues": issues,
        "title": soup.title.string.strip() if soup.title else "No title"
    }