# Choralchart — Roadmap

Effort and impact are rated Low / Med / High.
★ = came directly from assistant director feedback (Feb 2026).

---

## From the Assistant Director

| Branch | Idea | Effort | Impact |
|--------|------|--------|--------|
| `fix/layout-polish` | Never allow a section to be one person wide (warn) ★ | Low | High |
| `feature/ordering` | Up/down row ordering, not just left/right ★ | Med | High |
| `feature/roster-management` | Singer withdrawal: adjust row without full rebuild ★ | Med | High |
| `feature/roster-management` | .xlsx input support (real-world rosters from Excel) ★ | Med | Med |
| `feature/mixed-seating` | Shuffle/mix mode: no same-voice-part neighbors ★ | Med | Med |
| `feature/undo-redo` | Undo/redo for drag-and-drop and edits ★ | High | High |
| `feature/sharing` | Shareable link to send chart to students ★ | High | High |
| `feature/sharing` | "Living document" link that updates in place ★ | High | High |
| `feature/persistence` | Save and reload charts across sessions ★ | High | High |
| `feature/piece-specific-roles` | Piece-specific role assignment (cross-part roles) ★ | High | Med |

---

## Other Ideas

| Branch | Idea | Effort | Impact |
|--------|------|--------|--------|
| `feature/save-load` | Save chart to a file and reload it later (JSON export/import) | Low | High |
| `fix/layout-polish` | View full roster with scrolling on smaller windows | Low | Med |
| `fix/export` | Save full image snapshot from smaller windows (html2canvas clips on small viewports) | Low | Med |
| `fix/layout-polish` | Centeredness shifts when scrollbar appears/disappears | Low | Med |
| `fix/layout-polish` | Conductor label not centered (row label throws it off) | Low | Med |
| `feature/branding` | Add favicon | Low | Low |
| `feature/branding` | Add logo | Low | Med |
| `fix/layout-polish` | "Enter your roster" input styling matches other text boxes | Low | Low |
| `feature/sample-rosters` | Ship sample CSVs (SATB, Men's, Women's, etc.) | Low | Med |
| `fix/layout-polish` | Seat number toggle from either edge or both | Low | Low |
| `feature/height-warning` | Warn when a tall singer is placed in front of a shorter one | Low | High |
| `fix/stagger` | Stagger/grid switch (fix odd/even centering ghost-stagger) | Med | Med |
| `fix/layout-polish` | Include empty chairs on edges option | Med | Low |
| `feature/animations` | Animate flip, drag-and-drop, height toggle | Med | Low |
| `qa/cross-platform` | Test on Windows, macOS, iOS, Android browsers | Med | High |

---

## Tabled

| Branch | Idea | Notes |
|--------|------|-------|
| `feature/curved-rows` | Curved rows | Removed from UI — code on branch, known visual bugs |
| `feature/piece-specific-roles` | Complicated/combined ensemble layouts | Needs design work before implementation |

---

## Done ✓

| Feature | Notes |
|---------|-------|
| Hosting | Live at https://choralchart.onrender.com (Render, free tier) |
| Navbar | Sticky ChoralChart navbar on every page |
| Footer | Shared footer with copyright and GitHub link |
| README | Setup instructions, CSV format, tech stack |
| Manual roster entry | Paste-by-part textarea entry with optional height parsing (`Name, 5'10"`) |
| Optional heights | Singer height is optional; unknown heights sort to the middle of their group |
| Random roster polish | ±5 variation per section, diverse names, unknown parts get random gender |
| Unified `/configure` route | Both entry methods post to the same URL |
| PNG export | Replaced `window.print()` with html2canvas PNG download (full chart, not just visible area) |
| Dual scrollbar fix | Chart scrolls within panel, no body-level horizontal scroll |
| Edit page URL | Configure now posts directly to `/edit` (was `/preview`) |
| ✕ button fix | Remove-section button width and height corrected on roster entry page |
| ~~PDF export~~ | ~~Replaced by PNG export~~ |
| ~~Navbar feature~~ | ~~Done~~ |
