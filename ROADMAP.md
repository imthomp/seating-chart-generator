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
| `feature/sample-rosters` | Ship sample CSVs (SATB, Men's, Women's, etc.) | Low | Med |
| `fix/layout-polish` | Conductor label not centered (row label throws it off) | Low | Med |
| `fix/layout-polish` | Seat number toggle from either edge or both | Low | Low |
| `fix/layout-polish` | Fix weird horizontal scrolling on large charts | Low | Med |
| `feature/height-warning` | Warn when a tall singer is placed in front of a shorter one | Low | High |
| `fix/export` | Improve PDF export (currently just `window.print()`) | Med | High |
| `fix/stagger` | Stagger/grid switch (fix odd/even centering ghost-stagger) | Med | Med |
| `fix/layout-polish` | Include empty chairs on edges option | Med | Low |
| `feature/navbar` | Add a nav bar as the app grows | Low | Low |
| `feature/animations` | Animate flip, drag-and-drop, height toggle | Med | Low |

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
