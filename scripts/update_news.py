import os, json, re, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone

FEEDS = [
    ("Google News AI", "https://news.google.com/rss/search?q=Artificial+Intelligence+AI&hl=en-US&gl=US&ceid=US:en"),
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology-lab")
]

def clean_html(raw_html):
    if not raw_html:
        return ""
    clean = re.sub(r"<[^>]+>", "", raw_html)
    clean = clean.replace("&amp;", "&").replace("&quot;", '"').replace("&apos;", "'").replace("&#39;", "'").replace("&lt;", "<").replace("&gt;", ">")
    return " ".join(clean.split()).strip()

def classify_category(text):
    t = text.lower()
    if any(k in t for k in ["robot", "humanoid", "hardware", "chip", "npu", "silicon", "sensor", "wearable", "glasses", "device", "semiconductor"]):
        return "Robotics & Hardware", "bot", "cyan"
    elif any(k in t for k in ["security", "hack", "cyber", "vulnerability", "malware", "zero-day", "defense", "recovery", "threat"]):
        return "Cybersecurity", "shield-check", "rose"
    elif any(k in t for k in ["policy", "law", "act", "regulation", "bill", "congress", "senate", "eu ai act", "penalties", "court", "fda", "copyright", "governance"]):
        return "Policy & Governance", "file-text", "amber"
    elif any(k in t for k in ["energy", "nuclear", "grid", "power", "datacenter", "data center", "infrastructure", "100mw", "cooling"]):
        return "Infrastructure & Energy", "zap", "emerald"
    elif any(k in t for k in ["research", "science", "genome", "biology", "math", "proof", "climate", "lunar", "quantum", "weather", "arxiv", "paper"]):
        return "Science & Research", "flask-conical", "indigo"
    else:
        return "Frontier Models", "cpu", "purple"

def fetch_feed(feed_name, url):
    items = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            # Channel items (RSS 2.0)
            for item in root.findall(".//item")[:10]:
                title = clean_html(item.findtext("title", ""))
                link = item.findtext("link", "")
                desc = clean_html(item.findtext("description", ""))
                pub_date = item.findtext("pubDate", "")
                
                # Extract source if available
                source_elem = item.find("source")
                source = source_elem.text.strip() if (source_elem is not None and source_elem.text) else feed_name
                
                # Format timestamp
                now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
                
                # Clean up title if ends with " - Source"
                if " - " in title:
                    parts = title.rsplit(" - ", 1)
                    title = parts[0].strip()
                    if source == feed_name and len(parts[1]) < 35:
                        source = parts[1].strip()
                
                if len(desc) < 25:
                    desc = f"Latest developments and updates concerning {title}. Read full coverage on {source}."
                if len(desc) > 280:
                    desc = desc[:277] + "..."
                    
                if title and link:
                    items.append({
                        "headline": title,
                        "summary": desc,
                        "source": source,
                        "timestamp": now_str,
                        "url": link
                    })
    except Exception as e:
        print(f"Warning: Failed to fetch {feed_name}: {e}")
    return items

def update_index_html():
    target_paths = [p for p in ["radar.html", "index.html"] if os.path.exists(p)]
    html = None
    chosen_path = None
    match = None

    for p in target_paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            m = re.search(r"const STORIES_DATA\s*=\s*(\[.*?\]);", content, re.DOTALL)
            if m:
                html = content
                chosen_path = p
                match = m
                break
        except Exception as e:
            continue

    if not match:
        print("Could not find STORIES_DATA in any target HTML file")
        return
    
    index_path = chosen_path
        
    try:
        existing_stories = json.loads(match.group(1))
    except Exception as e:
        print(f"Error parsing existing JSON: {e}")
        return

    existing_urls = {s.get("url", "").lower() for s in existing_stories}
    existing_headlines = {re.sub(r"[^a-z0-9]", "", s.get("headline", "").lower()) for s in existing_stories}

    new_stories = []
    for feed_name, url in FEEDS:
        items = fetch_feed(feed_name, url)
        for item in items:
            u = item["url"].lower()
            clean_h = re.sub(r"[^a-z0-9]", "", item["headline"].lower())
            
            if u not in existing_urls and clean_h not in existing_headlines:
                cat, icon, color = classify_category(f"{item['source']} {item['headline']} {item['summary']}")
                story_obj = {
                    "id": f"story-{int(datetime.now().timestamp())}-{len(new_stories)}",
                    "headline": item["headline"],
                    "summary": item["summary"],
                    "source": item["source"],
                    "timestamp": item["timestamp"],
                    "url": item["url"],
                    "category": cat,
                    "icon": icon,
                    "color": color
                }
                new_stories.append(story_obj)
                existing_urls.add(u)
                existing_headlines.add(clean_h)

    print(f"Found {len(new_stories)} brand new stories!")
    if not new_stories:
        print("No updates needed. Feed is already up to date.")
        return

    # Prepend new stories and keep top 60
    combined = new_stories + existing_stories
    combined = combined[:65]

    updated_json_str = json.dumps(combined, ensure_ascii=False)
    for p in target_paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                c = f.read()
            m = re.search(r"const STORIES_DATA\s*=\s*(\[.*?\]);", c, re.DOTALL)
            if m:
                new_c = c[:m.start(1)] + updated_json_str + c[m.end(1):]
                with open(p, "w", encoding="utf-8") as f:
                    f.write(new_c)
                print(f"Successfully updated {p} with {len(new_stories)} new stories!")
        except Exception as err:
            print(f"Error updating {p}: {err}")

if __name__ == "__main__":
    update_index_html()
