# STAR Scholars Circle Website

The official public-facing website for the **STAR Scholars Network** — a global platform showcasing active circles, institution rankings, and community programs.

🌐 **Live Site:** [https://aamodpaudel.github.io/star_modified](https://aamodpaudel.github.io/star_modified)

---

## Overview

This is a static HTML/CSS/JS website hosted on GitHub Pages. It provides:

- **Homepage** — Live upcoming STAR Circles loaded dynamically from the STAR API, institution rankings, and program overviews.
- **Institutions Rankings** — Top 50 global institutions ranked by STAR Circle participation and impact.
- **Full Rankings Page** — Detailed STAR Impact Ranking table for institutions.
- **How Circles Work** — Explainer page covering the circle model, participation flow, and program details.

---

## Project Structure

```
star-scholars-circle-website/
├── index.html              # Main homepage (GitHub Pages entry point)
│
├── pages/                  # Secondary HTML pages
│   ├── rankings.html           # Full STAR Impact Rankings table
│   ├── institutions.html       # Top 50 institutions page
│   ├── how-circles-work.html   # Circle explainer page
│   └── index_table_new.html    # Draft/staging page
│
├── images/                 # All local image assets
│   ├── president.png
│   ├── president-photo.png
│   ├── andrealee.jpg
│   ├── krishnabista.png
│   ├── shyamsharma.png
│   ├── thakur.jpg
│   ├── careerlink-logo.png
│   └── gemini-icon.svg
│
├── scripts/                # Offline Python data processing scripts
│   ├── process_rankings.py     # Generates rankings_data.json from member CSV
│   ├── fix_external.py         # HTML link fixer utility
│   ├── fix_html.py             # HTML cleanup utility
│   └── test_api.py             # API response tester
│
├── data/                   # Static data files
│   └── rankings_data.json      # Pre-processed institution rankings data
│
├── docs/                   # Scoring methodology documentation
│   ├── external_scoring_logic.md
│   ├── external_scoring_logic.pdf
│   ├── internal_scoring_logic.md
│   └── internal_scoring_logic.pdf
│
└── .gitignore
```

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Markup | HTML5 |
| Styling | Tailwind CSS (CDN) |
| Animations | Three.js, GSAP + ScrollTrigger |
| Fonts | Google Fonts (Inter) |
| Data | STAR Scholars REST API + static JSON |
| Hosting | GitHub Pages |

---

## Live Data

The homepage fetches upcoming circles in real time from the STAR Scholars API:

```
GET https://app.starscholars.org/api/v1/groups/list/?group_type=circle&circle_status=1,4
```

The rankings tables are pre-rendered from static data (no runtime CSV dependency).

---

## Rankings Data Pipeline

Institution rankings are generated **offline** using the Python script in `scripts/`:

```bash
# Run locally (requires a member export CSV — never commit this file)
python scripts/process_rankings.py
```

This reads a member export CSV, scores institutions by participation metrics, and outputs `data/rankings_data.json`. The resulting data is then manually baked into the HTML tables.

> ⚠️ **Never commit the member CSV export.** It contains sensitive PII and is blocked by `.gitignore`.

---

## Scoring Methodology

Institution rankings use a weighted rubric across six dimensions:

| Metric | Weight |
|--------|--------|
| Total Circle Participants | 25% |
| Authentic Members | 25% |
| Total Seniority | 15% |
| Country Diversity | 10% |
| Advanced Career Members | 15% |
| Field Diversity | 10% |

Full methodology: [`docs/external_scoring_logic.md`](docs/external_scoring_logic.md)

---

## Development

No build step required — open `index.html` directly in a browser or serve locally:

```bash
# Using Python
python -m http.server 8080

# Using Node.js
npx serve .
```

Then visit `http://localhost:8080`.

---

## Deployment

This site is deployed automatically via **GitHub Pages** from the `main` branch root.

Any push to `main` will update the live site within ~60 seconds.

---

## Related

- 🌐 [STAR Scholars Community Platform](https://app.starscholars.org)
- 🌐 [STAR Scholars Main Website](https://starscholars.org)
- 🔗 [CareerLink Platform](https://github.com/aamodpaudel/careerlink)
