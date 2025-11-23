# Pharmaceutical QR Code System  
### Never Lose Critical Medicine Information Again

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![QR Code](https://img.shields.io/badge/QR_Code-Security-6C63FF?style=for-the-badge)
![Live](https://img.shields.io/badge/Live_Demo-00D26A?style=for-the-badge&logo=vercel)

**Live Worldwide** → [https://viki916.pythonanywhere.com](https://viki916.pythonanywhere.com)  
**One Scan = Full Medicine Safety Info**  

</div>

---

## Why This Project Exists

Imagine a patient at home, the medicine strip is torn, the box is lost — but the **tiny QR sticker** on the foil is still there.  
One scan → instant access to:

- Drug name & composition  
- Dosage instructions  
- Batch & expiry date  
- Side effects & precautions  
- Manufacturer details  

**No more guesswork. No more expired medicines. No more risks.**

---

## Features That Save Lives

| Feature                         | Description                                                                 |
|---------------------------------|-----------------------------------------------------------------------------|
| Instant QR Generation           | Fill form → get printable high-res QR in < 2 seconds                        |
| Rich Medicine Database          | Stores 15+ fields: uses, side effects, storage, warnings                    |
| Permanent Cloud Access          | Hosted 24×7 — scan from anywhere in the world                             |
| Zero App Required               | Works with any phone camera or QR scanner                                   |
| Download & Print Ready          | PNG + SVG export — perfect for strips, bottles, blister packs              |
| Mobile-First Responsive UI      | Looks stunning on phones, tablets, and desktops                             |
| Lightweight & Fast              | < 5 MB deployment, blazing fast even on slow connections                    |

---

## Tech Stack (Modern & Minimal)

| Layer          | Technology                                   |
|----------------|----------------------------------------------|
| Backend        | Python 3.11 + Flask 3.x                      |
| Database       | SQLite (with SQLAlchemy)                      |
| QR Generation  | qrcode[pil] + Pillow                         |
| Frontend       | Jinja2 templates + Vanilla CSS + HTMX touches|
| Hosting        | PythonAnywhere (free tier friendly)          |

---

## Quick Start (Local)

```bash
# 1. Clone
git clone https://github.com/sathvikradhikam/Pharmacetical-QR.git
cd Pharmacetical-QR

# 2. Virtual environment
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Run
python app.py
```


Live Demo
https://viki916.pythonanywhere.com
Try it now:

Create a sample medicine
Download the QR
Scan with your phone → see magic


Real-World Use Cases

Hospital pharmacy labeling
Rural clinics with limited storage
Elderly patients living alone
Travel medication kits
Clinical trials & sample distribution
Veterinary medicines


Roadmap (What’s Coming Next)
Status,Feature
Done,Single QR creation & cloud hosting
Done,Mobile responsive UI
Next,User accounts & private QR library
Next,Batch QR generation (CSV upload)
Next,"Multilingual support (Hindi, Tamil, etc.)"
Next,REST API + OpenAPI docs
Next,PWA + offline scan fallback




































StatusFeatureDoneSingle QR creation & cloud hostingDoneMobile responsive UINextUser accounts & private QR libraryNextBatch QR generation (CSV upload)NextMultilingual support (Hindi, Tamil, etc.)NextREST API + OpenAPI docsNextPWA + offline scan fallback
Star & watch the repo to follow progress!

Project Structure
textPharmacetical-QR/
├── app.py                  Main Flask app
├── models.py               SQLAlchemy models
├── requirements.txt
├── runtime.txt             Python version
├── tablets.db              Auto-created SQLite DB
├── templates/              HTML + Jinja2
├── static/                 CSS, images, downloaded QRs
└── uploads/                Temporary QR storage

Deploy Your Own (Free)

Sign up at PythonAnywhere
Upload files
pip install --user -r requirements.txt
Point WSGI to app.py
Reload → done!


Contributing
Contributions are what make healthcare open-source beautiful!

Fork it
Create your branch (git checkout -b feature/cool-thing)
Commit (git commit -m 'Add cool-thing')
Push & open a Pull Request


License
MIT License © 2025 Sathvik Radhikam
Feel free to use commercially or in hospitals — just keep the license file.


Made with passion for safer medication worldwide
GitHub stars
GitHub forks
Give it a star if you believe every medicine should be scannable!
[Star]**

```
