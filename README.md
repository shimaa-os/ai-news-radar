# ⚡ AI News Radar

An advanced, real-time artificial intelligence intelligence feed tracking frontier models, autonomous agent protocols, physical robotics, and high-impact policy shifts.

🔗 **Live Dashboard:** [https://shimaa-os.github.io/ai-news-radar/](https://shimaa-os.github.io/ai-news-radar/)

---

## ✨ Features

- **🔍 Real-Time Instant Search:** Full-text instant filtering across headlines, summaries, domains, and sources with keyboard shortcuts (`/` or `⌘K` to focus, `Esc` to clear).
- **🏷️ Editorial Sector Filters:** Minimalist OpenAI-style inverted pills for **Frontier Models**, **Robotics & Silicon**, **Cybersecurity**, **Policy & Governance**, **Infrastructure & Energy**, and **Science & Research**.
- **⭐ Bookmarks & Favorites:** Save articles to read later with persistent `localStorage` support and a dedicated Bookmarks view tab.
- **📐 Dual Layout Engine:** Seamless toggle between a responsive **Editorial 2-Column Grid** and a compact **Research Table/List View**.
- **📋 Share & Copy:** One-click article URL copying with sleek monochrome toast alerts.
- **🕒 Live Telemetry Clock:** Real-time UTC status ticker with live pulse monitor indicator.
- **🎨 OpenAI-Inspired Monochromatic Canvas:** Pitch-black `#000000` palette, razor-sharp 1px hairline borders, and zero tacky "AI emoji" tropes.
- **✨ Vector Iconography & Cinematic Motion:** Powered by **Lucide Icons** and **GSAP (GreenSock)** for buttery 60fps staggered card entrances and count-up metrics.

---

## 🤖 Automated 24/7 Cloud Pipeline

This repository is self-updating via GitHub Actions (`.github/workflows/update_news.yml`):
- **Continuous Schedule:** Runs automatically every hour in the GitHub cloud (no local machine or servers required).
- **Multi-Source Aggregator:** Fetches fresh breaking news from Google News AI, TechCrunch AI, The Verge AI, and Ars Technica.
- **Intelligent Classification:** Automatically deduplicates, tags, and classifies new stories into 6 domain sectors.
- **Auto-Deployment:** Commits and pushes fresh news directly to `main`, triggering instantaneous GitHub Pages publishing.

---

## 🚀 Getting Started

### Local Viewing
Simply open `index.html` in your favorite web browser:
```bash
# Windows
start index.html

# macOS
open index.html

# Linux
xdg-open index.html
```

### Live Deployment
The project is hosted live on GitHub Pages:
👉 **[https://shimaa-os.github.io/ai-news-radar/](https://shimaa-os.github.io/ai-news-radar/)**

---

## 🛠️ Architecture
- **HTML5 & CSS3:** Pitch-black canvas, CSS custom properties, hairline borders, CSS grid, and responsive flexbox.
- **Icons:** [Lucide Icons](https://lucide.dev/) via official CDN for pixel-perfect vector symbols.
- **Animations:** [GSAP (GreenSock)](https://gsap.com/) for fluid 60fps staggered entrances and telemetry count-ups.
- **Vanilla JavaScript:** High-performance DOM manipulation, search debounce/filtering, state management, and `localStorage` persistence.
- **Automated Pipeline:** Python 3.11 with standard libraries (`urllib`, `xml.etree.ElementTree`, `re`, `json`).
- **Typography:** Google Fonts (`Inter` & `JetBrains Mono`).

---

## 📄 License
MIT License
