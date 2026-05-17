#!/usr/bin/env python3
"""
Brand Live Pro — Build script for content + template → HTML

Usage:
  python3 build.py

Reads content.json, injects into template.html, outputs index.html
Edit content.json to change copy, metrics, pricing, etc.
"""

import json
import re

# Read content
with open('content.json', 'r') as f:
    content = json.load(f)

# Read template
with open('index.html', 'r') as f:
    html = f.read()

# Helper to build metric cells
def build_metrics(metrics):
    cells = []
    for m in metrics:
        cell = f'''        <div class="metric-cell">
          <div class="metric-value">{m['value']}</div>
          <div class="metric-label">{m['label']}</div>
        </div>'''
        cells.append(cell)
    return '\n'.join(cells)

# Helper to build trust bar items
def build_trust_row(items):
    spans = []
    for item in items:
        spans.append(f"<span><strong>{item['strong']}</strong> {item['text']}</span>")
    return '\n      '.join(spans)

# Helper to build problem cards
def build_problem_cards(cards):
    result = []
    icons = {'users': 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75',
             'chart': 'M3 3v18h18M18.7 8 13 13.7l-3-3L6 14.7',
             'clock': 'M3 3v18h18M18.7 8 13 13.7l-3-3L6 14.7'}

    for card in cards:
        icon_path = icons.get(card['icon'], '')
        result.append(f'''      <div class="problem-card reveal">
        <div class="problem-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="{icon_path}"/></svg>
        </div>
        <h3>{card['h3']}</h3>
        <p>{card['p']}</p>
      </div>''')
    return '\n'.join(result)

# Helper to build proof cards
def build_proof_cards(cards):
    result = []
    for card in cards:
        result.append(f'''      <div class="proof-card reveal">
        <div class="proof-value">{card['value']}</div>
        <div class="proof-label">{card['label']}</div>
        <div class="proof-desc">{card['desc']}</div>
      </div>''')
    return '\n'.join(result)

# Helper to build steps
def build_steps(items):
    result = []
    for i, item in enumerate(items, 1):
        result.append(f'''      <div class="step reveal">
        <div class="step-num">{item['week']}</div>
        <h3>{item['h3']}</h3>
        <p>{item['p']}</p>
      </div>''')
    return '\n'.join(result)

# Helper to build FAQ items
def build_faq(items):
    result = []
    for i, item in enumerate(items):
        open_attr = 'open' if i == 0 else ''
        result.append(f'''      <details class="faq reveal" {open_attr}>
        <summary>{item['q']}<span class="plus"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></span></summary>
        <div class="faq-body">
          {item['a']}
        </div>
      </details>''')
    return '\n'.join(result)

# Helper to build pricing cards
def build_pricing_cards(cards):
    result = []
    for card in cards:
        featured_class = ' featured' if card.get('featured') else ''
        features_html = '\n          '.join([f'<li><span class="check"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg></span>{f}</li>' for f in card['features']])

        result.append(f'''      <div class="price-card{featured_class} reveal" id="audit">
        <span class="price-tag">{card['tag']}</span>
        <div class="price-name">{card['name']}</div>
        <div class="price-desc">{card['desc']}</div>
        <div class="price-num">{card['price']}<span class="small">/ {card['period']}</span></div>
        <ul class="price-features">
          {features_html}
        </ul>
        <a href="{card['cta_link']}" class="btn {'btn-primary' if card.get('featured') else 'btn-ghost'}">
          {card['cta_text']}
          <span class="arrow">→</span>
        </a>
      </div>''')
    return '\n'.join(result)

# Inject content into template
replacements = {
    r'<title>.*?</title>': f"<title>{content['site']['title']}</title>",
    r'<meta name="description" content=".*?">': f'<meta name="description" content="{content["site"]["description"]}">',
    r'<meta property="og:title" content=".*?">': f'<meta property="og:title" content="{content["site"]["title"]}">',
    r'<meta property="og:description" content=".*?">': f'<meta property="og:description" content="{content["site"]["description"]}">',
    r'<meta property="og:url" content=".*?">': f'<meta property="og:url" content="{content["site"]["domain"]}">',
}

for pattern, replacement in replacements.items():
    html = re.sub(pattern, replacement, html)

# Hero metrics
metrics_html = build_metrics(content['hero']['metrics'])
html = re.sub(
    r'<div class="metric-strip reveal">.*?</div>\s*</div>\s*</div>\s*</section>',
    f'<div class="metric-strip reveal">\n{metrics_html}\n      </div>\n    </div>\n  </div>\n</section>',
    html,
    flags=re.DOTALL
)

# Trust bar
trust_html = build_trust_row(content['trust_bar'])
html = re.sub(
    r'<div class="trust-row">.*?</div>',
    f'<div class="trust-row">\n      {trust_html}\n    </div>',
    html,
    flags=re.DOTALL
)

# Problem cards
problem_html = build_problem_cards(content['problem']['cards'])
html = re.sub(
    r'<div class="problem-grid">.*?</div>\s*</div>\s*</section>',
    f'<div class="problem-grid">\n{problem_html}\n    </div>\n  </div>\n</section>',
    html,
    flags=re.DOTALL
)

# Proof cards
proof_html = build_proof_cards(content['proof']['cards'])
html = re.sub(
    r'<div class="proof-grid">.*?</div>\s*</div>\s*</section>',
    f'<div class="proof-grid">\n{proof_html}\n    </div>\n  </div>\n</section>',
    html,
    flags=re.DOTALL
)

# Steps
steps_html = build_steps(content['steps']['items'])
html = re.sub(
    r'<div class="steps">.*?</div>\s*</div>\s*</section>',
    f'<div class="steps">\n{steps_html}\n    </div>\n  </div>\n</section>',
    html,
    flags=re.DOTALL
)

# FAQ
faq_html = build_faq(content['faq']['items'])
html = re.sub(
    r'<div class="faq-grid">.*?</div>\s*</div>\s*</section>',
    f'<div class="faq-grid">\n{faq_html}\n    </div>\n  </div>\n</section>',
    html,
    flags=re.DOTALL
)

# Pricing
pricing_html = build_pricing_cards(content['pricing']['cards'])
html = re.sub(
    r'<div class="pricing-grid">.*?</div>\s*</div>\s*</section>',
    f'<div class="pricing-grid">\n{pricing_html}\n    </div>\n  </div>\n</section>',
    html,
    flags=re.DOTALL
)

# Write output
with open('index.html', 'w') as f:
    f.write(html)

print("✓ Built index.html from content.json")
