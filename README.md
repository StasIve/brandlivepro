# Brand Live Pro — Content & Build System

## Overview

Site structure: **content.json** (editable) → **build.py** (processor) → **index.html** (output)

You edit content in `content.json`, run the build script, and get a fresh `index.html`. No need to touch HTML directly.

## Editing Content

1. Open `content.json`
2. Find the section you want to change (hero, faq, pricing, etc.)
3. Edit the text, stats, or links
4. Save
5. Run the build script (see below)

## Building

From the `sites/brandlivepro/` directory:

```bash
python3 build.py
```

This reads `content.json`, injects values into the template, and outputs `index.html`.

**Done.** Reload your browser to see changes.

## Structure

```json
{
  "site": { /* Meta tags, domain, email */ },
  "nav": { /* Navigation copy */ },
  "hero": { /* Headline, metrics, CTA */ },
  "trust_bar": [ /* 5 trust items */ ],
  "problem": { /* Section copy + 3 cards */ },
  "mechanism": { /* How it works section */ },
  "proof": { /* 8 stat cards */ },
  "steps": { /* 4-step process */ },
  "halo": { /* Halo effect explanation */ },
  "comparison": { /* Comparison table metadata */ },
  "faq": { /* 6 Q&A items */ },
  "pricing": { /* 2 pricing tiers */ },
  "final_cta": { /* Bottom CTA */ }
}
```

## Common Edits

**Change hero headline:**
```json
"hero": {
  "h1_part1": "Your new part 1",
  "h1_accent": "your new accent",
  "h1_part2": "your new part 2"
}
```

**Update a metric:**
```json
"metrics": [
  { "value": "25×", "label": "New metric label" },
  ...
]
```

**Edit FAQ:**
```json
"faq": {
  "items": [
    { "q": "Your question?", "a": "Your answer here." },
    ...
  ]
}
```

**Update pricing:**
```json
"pricing": {
  "cards": [
    { "price": "$200", "period": "one-time", ... }
  ]
}
```

## CTA Links

All `cta_link` fields support:
- `mailto:` links: `mailto:hello@brandlivepro.com?subject=Book%20Audit`
- Calendly links: `https://calendly.com/brandlivepro/audit`
- Any URL

## Deploy

After building:

1. **Local testing:** Open `index.html` in browser
2. **Netlify drag-drop:** Drop `index.html` into Netlify
3. **Publish to domain:** Replace files on brandlivepro.com root

## Troubleshooting

**Build script fails?**
- Ensure Python 3 is installed: `python3 --version`
- Check JSON syntax in `content.json` (use a JSON validator)
- Ensure `index.html` exists in the same directory

**Changes not showing?**
- Run `python3 build.py` again
- Refresh browser (Cmd+Shift+R to clear cache)
- Check browser console for errors

**Lost styling?**
- Don't edit the `<style>` block in HTML
- Style is preserved in the template

---

**Questions?** Edit, build, test. Changes are instant.
