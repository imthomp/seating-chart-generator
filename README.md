# ChoralChart

A web app for generating choir seating charts. Upload a roster or enter singer counts by voice part, configure the layout, then drag-and-drop to fine-tune.

**Live demo:** [choralchart.onrender.com](http://choralchart.onrender.com)

> The free Render instance sleeps after 15 minutes of inactivity — first load may take ~30 seconds.

---

## Running Locally

```bash
pip install -r requirements.txt
python app.py
```

Open [http://localhost:5000](http://localhost:5000).

---

## CSV Format

To upload a real roster, use a CSV with these columns:

```
name,voice_part,height
John Smith,Tenor 1,72
Jane Doe,Soprano 2,64.5
Bob Johnson,Bass,74
```

- `name` — singer's name
- `voice_part` — any label (Soprano, Alto 1, Tenor 2, Bass, etc.)
- `height` — height in inches; used to place taller singers toward the back

---

## Tech Stack

- [Flask](https://flask.palletsprojects.com/) — Python web framework
- [Gunicorn](https://gunicorn.org/) — WSGI server for production
- [Render](https://render.com/) — hosting
