# 💊 Pharmaceutical QR Code System

### *Smart Medicine Tracking Through QR Technology*

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3.3-black?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge&logo=sqlite)
![Status](https://img.shields.io/badge/Status-Live-success?style=for-the-badge)

[🚀 Live Demo](https://viki916.pythonanywhere.com) • [📝 Report Bug](https://github.com/sathvikradhikam/Pharmacetical-QR/issues) • [✨ Request Feature](https://github.com/sathvikradhikam/Pharmacetical-QR/issues)

</div>

---

## 📖 About The Project

A revolutionary Flask-based web application that generates **QR codes for pharmaceutical tablets**, enabling instant access to comprehensive medication information by simply scanning the code. Whether the wrapper is lost or damaged, the embedded QR code ensures critical medical data is always accessible.

### ✨ Key Features

- 🔍 **Instant Information Access** - Scan QR codes to view complete tablet details
- 🏷️ **Comprehensive Data Storage** - Manufacturer, batch number, dates, composition, usage, side effects
- 🌐 **Cloud-Based** - Access from any device, anywhere in the world
- 📱 **Mobile-Friendly** - Responsive design works on all screen sizes
- ⚡ **Fast & Lightweight** - Built with Flask for optimal performance
- 🔒 **Persistent Storage** - SQLite database ensures data integrity
- 📥 **Downloadable QR Codes** - High-quality PNG format for printing

---

## 🛠️ Built With

- **[Flask](https://flask.palletsprojects.com/)** - Lightweight Python web framework
- **[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)** - Database ORM
- **[Python QRCode](https://pypi.org/project/qrcode/)** - QR code generation library
- **[Pillow](https://pillow.readthedocs.io/)** - Image processing
- **[SQLite](https://www.sqlite.org/)** - Embedded database
- **[PythonAnywhere](https://www.pythonanywhere.com/)** - Cloud hosting platform

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/sathvikradhikam/Pharmacetical-QR.git
cd Pharmacetical-QR
```
2. **Create a virtual environment**

```bash
python -m venv venv
```
On Windows:
```
Bashvenv\Scripts\activate
```
On Mac/Linux:
```
Bashsource venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
python app.py
```
5. **Open your browser**
```
http://localhost:5000
```
## 💡 Usage

### Creating QR Codes
1. Navigate to the home page  
2. Fill in the tablet information:
   - Tablet Name
   - Manufacturer
   - Batch Number
   - Manufacturing & Expiry Dates
   - Composition & Dosage
   - Medical Uses
   - Side Effects *(optional)*
   - Precautions *(optional)*
   - Storage Instructions *(optional)*
3. Click **"Create Tablet & Generate QR Code"**
4. Download the high-resolution QR code (PNG)
5. Print and stick it on strips, bottles, or blister packs

### Scanning QR Codes
1. Open any QR scanner or phone camera app
2. Point at the QR code
3. Tap the notification/link
4. Instantly view full medicine details – even without the original box!

---
## 🏗️ Project Architecture
```
User Device (Browser)
↓
Flask Web Application (PythonAnywhere)
↓
┌───────────────────────────────┐
│ Routes & API Endpoints        │
│ - / (Home)                    │
│ - /api/tablets (POST)         │
│ - /api/qrcode/<id>            │
│ - /info/<id>                  │
└───────────────────────────────┘
↓
┌───────────────────────────────┐
│ Business Logic                │
│ - Form validation             │
│ - QR code generation          │
│ - Data retrieval              │
└───────────────────────────────┘
↓
┌───────────────────────────────┐
│ SQLite Database               │
│ - tablets.db                  │
└───────────────────────────────┘
```
📂 Project Structure
Pharmacetical-QR/

├── app.py                 # Main Flask application

├── requirements.txt       # Python dependencies

├── runtime.txt            # Python version for deployment

├── Procfile               # Deployment configuration

├── tablets.db             # SQLite database (auto-generated)

└── README.md              # Project documentation

🌐 Deployment
This project is deployed on PythonAnywhere and accessible worldwide at:
🔗 https://viki916.pythonanywhere.com
Deploy Your Own

Create a free account on PythonAnywhere
Upload project files to /home/yourusername/mysite/
Install dependencies: pip3.11 install --user -r requirements.txt
Configure WSGI file to point to your app.py
Reload the web app

For detailed deployment instructions, see PythonAnywhere Flask Guide https://help.pythonanywhere.com/pages/Flask/.

🤝 Contributing
Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request


📄 License
Distributed under the MIT License. See LICENSE for more information.

👨‍💻 Author
Sathvik Radhikam

GitHub: @sathvikradhikam
Project Link: https://github.com/sathvikradhikam/Pharmacetical-QR


🙏 Acknowledgments

Flask Documentation
Python QRCode Library
PythonAnywhere Hosting
Shields.io for badges
Best README Template



Made with ❤️ for better healthcare
⬆ Back to Top
