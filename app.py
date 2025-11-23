from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import qrcode
import base64
from io import BytesIO
import uuid
import os
import traceback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tablets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Tablet(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    batch_number = db.Column(db.String(50), nullable=False)
    mfg_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    composition = db.Column(db.Text, nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    use_cases = db.Column(db.Text, nullable=False)
    side_effects = db.Column(db.Text)
    precautions = db.Column(db.Text)
    storage_instructions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'manufacturer': self.manufacturer,
            'batch_number': self.batch_number,
            'mfg_date': self.mfg_date.strftime('%Y-%m-%d'),
            'expiry_date': self.expiry_date.strftime('%Y-%m-%d'),
            'composition': self.composition,
            'dosage': self.dosage,
            'use_cases': self.use_cases,
            'side_effects': self.side_effects,
            'precautions': self.precautions,
            'storage_instructions': self.storage_instructions
        }

# Initialize database
with app.app_context():
    try:
        db.create_all()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

# Global error handler for JSON errors
@app.errorhandler(Exception)
def handle_error(error):
    print(f"Error occurred: {str(error)}")
    traceback.print_exc()
    return jsonify({
        'success': False,
        'error': str(error),
        'type': type(error).__name__
    }), 500

# ROOT ROUTE
@app.route('/')
def index():
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pharmaceutical QR Code Manager</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0;
                min-height: 600px;
            }
            
            .form-section, .qr-section {
                padding: 30px;
            }
            
            .form-section {
                border-right: 1px solid #eee;
            }
            
            .section-title {
                font-size: 1.5em;
                margin-bottom: 20px;
                color: #333;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: 600;
                color: #555;
            }
            
            .form-group input,
            .form-group textarea {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 14px;
                transition: border-color 0.3s;
            }
            
            .form-group input:focus,
            .form-group textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .form-group textarea {
                height: 80px;
                resize: vertical;
            }
            
            .form-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
            }
            
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
                width: 100%;
            }
            
            .btn:hover {
                transform: translateY(-2px);
            }
            
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            
            .qr-display {
                text-align: center;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                min-height: 300px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            
            .qr-code {
                max-width: 250px;
                border: 3px solid #667eea;
                border-radius: 10px;
                padding: 10px;
                background: white;
            }
            
            .tablet-info {
                margin-top: 20px;
                padding: 15px;
                background: white;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                max-width: 300px;
            }
            
            .success-message {
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                border-left: 4px solid #28a745;
            }
            
            .error-message {
                background: #f8d7da;
                color: #721c24;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                border-left: 4px solid #dc3545;
            }
            
            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid rgba(255,255,255,.3);
                border-radius: 50%;
                border-top-color: #fff;
                animation: spin 1s ease-in-out infinite;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            @media (max-width: 768px) {
                .content {
                    grid-template-columns: 1fr;
                }
                
                .form-section {
                    border-right: none;
                    border-bottom: 1px solid #eee;
                }
                
                .form-row {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📋 Pharmaceutical QR Code Manager</h1>
                <p>Create and manage QR codes for tablet information</p>
            </div>
            
            <div class="content">
                <div class="form-section">
                    <h2 class="section-title">Add New Tablet</h2>
                    
                    <div id="messages"></div>
                    
                    <form id="tabletForm">
                        <div class="form-group">
                            <label for="name">Tablet Name *</label>
                            <input type="text" id="name" name="name" required placeholder="e.g., Paracetamol">
                        </div>
                        
                        <div class="form-group">
                            <label for="manufacturer">Manufacturer *</label>
                            <input type="text" id="manufacturer" name="manufacturer" required placeholder="e.g., ABC Pharmaceuticals">
                        </div>
                        
                        <div class="form-group">
                            <label for="batch_number">Batch Number *</label>
                            <input type="text" id="batch_number" name="batch_number" required placeholder="e.g., BTH001234">
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label for="mfg_date">Manufacturing Date *</label>
                                <input type="date" id="mfg_date" name="mfg_date" required>
                            </div>
                            
                            <div class="form-group">
                                <label for="expiry_date">Expiry Date *</label>
                                <input type="date" id="expiry_date" name="expiry_date" required>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label for="composition">Composition *</label>
                            <textarea id="composition" name="composition" placeholder="Active ingredients and their quantities" required></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="dosage">Dosage *</label>
                            <input type="text" id="dosage" name="dosage" placeholder="e.g., 500mg twice daily" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="use_cases">Medical Uses *</label>
                            <textarea id="use_cases" name="use_cases" placeholder="Conditions this medication treats" required></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="side_effects">Side Effects</label>
                            <textarea id="side_effects" name="side_effects" placeholder="Common side effects"></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="precautions">Precautions</label>
                            <textarea id="precautions" name="precautions" placeholder="Important precautions and warnings"></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="storage_instructions">Storage Instructions</label>
                            <textarea id="storage_instructions" name="storage_instructions" placeholder="How to store this medication"></textarea>
                        </div>
                        
                        <button type="submit" class="btn" id="submitBtn">Create Tablet & Generate QR Code</button>
                    </form>
                </div>
                
                <div class="qr-section">
                    <h2 class="section-title">Generated QR Code</h2>
                    
                    <div class="qr-display" id="qrDisplay">
                        <p>Fill out the form and submit to generate a QR code</p>
                    </div>
                </div>
            </div>
        </div>

        <script>
            document.getElementById('tabletForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData(this);
                const data = Object.fromEntries(formData);
                
                const submitBtn = document.getElementById('submitBtn');
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="loading"></span> Processing...';
                
                // Clear previous messages
                document.getElementById('messages').innerHTML = '';
                
                try {
                    // Create tablet with better error handling
                    const response = await fetch('/api/tablets', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });
                    
                    // Check if response is ok
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    // Check if response has content
                    const contentType = response.headers.get("content-type");
                    if (!contentType || !contentType.includes("application/json")) {
                        throw new Error("Server didn't return JSON! Check server logs.");
                    }
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        // Show success message
                        document.getElementById('messages').innerHTML = `
                            <div class="success-message">
                                ✅ Tablet created successfully! Generating QR code...
                            </div>
                        `;
                        
                        // Generate QR code
                        const qrResponse = await fetch(`/api/qrcode/${result.tablet_id}`);
                        
                        if (!qrResponse.ok) {
                            throw new Error(`QR generation failed! status: ${qrResponse.status}`);
                        }
                        
                        const qrData = await qrResponse.json();
                        
                        // Display QR code
                        document.getElementById('qrDisplay').innerHTML = `
                            <img src="${qrData.qr_code}" alt="QR Code" class="qr-code">
                            <div class="tablet-info">
                                <h3>${qrData.tablet_info.name}</h3>
                                <p><strong>Manufacturer:</strong> ${qrData.tablet_info.manufacturer}</p>
                                <p><strong>Batch:</strong> ${qrData.tablet_info.batch_number}</p>
                                <p><strong>Expires:</strong> ${qrData.tablet_info.expiry_date}</p>
                                <button onclick="downloadQR('${qrData.qr_code}', '${qrData.tablet_info.name}_${qrData.tablet_info.batch_number}.png')" class="btn" style="margin-top: 10px; padding: 8px 16px; font-size: 14px;">
                                    Download QR Code
                                </button>
                            </div>
                        `;
                        
                        document.getElementById('messages').innerHTML = `
                            <div class="success-message">
                                ✅ Tablet created and QR code generated successfully!
                            </div>
                        `;
                        
                        // Reset form
                        this.reset();
                    } else {
                        document.getElementById('messages').innerHTML = `
                            <div class="error-message">
                                ❌ Error: ${result.error || 'Unknown error occurred'}
                            </div>
                        `;
                    }
                } catch (error) {
                    console.error('Full error:', error);
                    document.getElementById('messages').innerHTML = `
                        <div class="error-message">
                            ❌ Error: ${error.message}<br>
                            <small>Check browser console for more details</small>
                        </div>
                    `;
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Create Tablet & Generate QR Code';
                }
            });
            
            function downloadQR(dataUrl, filename) {
                const link = document.createElement('a');
                link.download = filename;
                link.href = dataUrl;
                link.click();
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

# API Routes with improved error handling
@app.route('/api/tablets', methods=['POST'])
def create_tablet():
    try:
        print("Received POST request to /api/tablets")
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data received'
            }), 400
        
        print(f"Data received: {data}")
        
        tablet = Tablet(
            name=data['name'],
            manufacturer=data['manufacturer'],
            batch_number=data['batch_number'],
            mfg_date=datetime.strptime(data['mfg_date'], '%Y-%m-%d').date(),
            expiry_date=datetime.strptime(data['expiry_date'], '%Y-%m-%d').date(),
            composition=data['composition'],
            dosage=data['dosage'],
            use_cases=data['use_cases'],
            side_effects=data.get('side_effects', ''),
            precautions=data.get('precautions', ''),
            storage_instructions=data.get('storage_instructions', '')
        )
        
        db.session.add(tablet)
        db.session.commit()
        
        print(f"Tablet created successfully with ID: {tablet.id}")
        
        return jsonify({
            'success': True,
            'tablet_id': tablet.id,
            'message': 'Tablet created successfully'
        }), 201
        
    except KeyError as e:
        error_msg = f'Missing required field: {str(e)}'
        print(f"KeyError: {error_msg}")
        return jsonify({'success': False, 'error': error_msg}), 400
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error creating tablet: {error_msg}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': error_msg}), 500

@app.route('/api/tablets/<tablet_id>', methods=['GET'])
def get_tablet(tablet_id):
    try:
        tablet = Tablet.query.get_or_404(tablet_id)
        return jsonify(tablet.to_dict()), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@app.route('/api/qrcode/<tablet_id>')
def generate_qr_code(tablet_id):
    try:
        print(f"Generating QR code for tablet ID: {tablet_id}")
        tablet = Tablet.query.get_or_404(tablet_id)
        
        # Create QR code data URL - THIS IS WHERE THE NETWORK IP IS USED
        base_url = request.url_root
        qr_data = f"{base_url}info/{tablet_id}"
        
        print(f"QR Code will point to: {qr_data}")
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        print("QR code generated successfully")
        
        return jsonify({
            'qr_code': f"data:image/png;base64,{img_str}",
            'qr_data': qr_data,
            'tablet_info': tablet.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

# Web Interface for Information Display
@app.route('/info/<tablet_id>')
def tablet_info(tablet_id):
    try:
        tablet = Tablet.query.get_or_404(tablet_id)
        
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ tablet.name }} - Medication Information</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                    color: #333;
                }
                .container {
                    background: white;
                    border-radius: 12px;
                    padding: 30px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                .header {
                    text-align: center;
                    border-bottom: 2px solid #007bff;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }
                .tablet-name {
                    color: #007bff;
                    font-size: 2.5em;
                    margin: 0;
                    font-weight: bold;
                }
                .manufacturer {
                    color: #666;
                    font-size: 1.2em;
                    margin: 10px 0;
                }
                .info-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }
                .info-card {
                    background: #f8f9fa;
                    border-left: 4px solid #007bff;
                    padding: 20px;
                    border-radius: 8px;
                }
                .info-title {
                    font-weight: bold;
                    color: #007bff;
                    font-size: 1.1em;
                    margin-bottom: 10px;
                }
                .info-content {
                    line-height: 1.6;
                }
                .dates {
                    display: flex;
                    justify-content: space-between;
                    flex-wrap: wrap;
                    gap: 20px;
                    margin: 20px 0;
                }
                .date-card {
                    flex: 1;
                    min-width: 200px;
                    text-align: center;
                    padding: 15px;
                    border-radius: 8px;
                }
                .mfg-date {
                    background: #d4edda;
                    color: #155724;
                }
                .exp-date {
                    background: #f8d7da;
                    color: #721c24;
                }
                .warning {
                    background: #fff3cd;
                    color: #856404;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 20px 0;
                    border-left: 4px solid #ffc107;
                }
                .batch-info {
                    background: #e7f3ff;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 class="tablet-name">{{ tablet.name }}</h1>
                    <p class="manufacturer">{{ tablet.manufacturer }}</p>
                </div>
                
                <div class="batch-info">
                    <strong>Batch Number:</strong> {{ tablet.batch_number }}
                </div>
                
                <div class="dates">
                    <div class="date-card mfg-date">
                        <h3>Manufacturing Date</h3>
                        <p><strong>{{ tablet.mfg_date.strftime('%d %B %Y') }}</strong></p>
                    </div>
                    <div class="date-card exp-date">
                        <h3>Expiry Date</h3>
                        <p><strong>{{ tablet.expiry_date.strftime('%d %B %Y') }}</strong></p>
                    </div>
                </div>
                
                {% if (tablet.expiry_date - today).days < 30 and (tablet.expiry_date - today).days >= 0 %}
                <div class="warning">
                    <strong>⚠️ Warning:</strong> This medication expires in {{ (tablet.expiry_date - today).days }} days.
                </div>
                {% elif (tablet.expiry_date - today).days < 0 %}
                <div class="warning" style="background: #f8d7da; color: #721c24;">
                    <strong>🚫 EXPIRED:</strong> This medication expired. DO NOT USE.
                </div>
                {% endif %}
                
                <div class="info-grid">
                    <div class="info-card">
                        <div class="info-title">💊 Composition & Dosage</div>
                        <div class="info-content">
                            <p><strong>Active Ingredients:</strong> {{ tablet.composition }}</p>
                            <p><strong>Dosage:</strong> {{ tablet.dosage }}</p>
                        </div>
                    </div>
                    
                    <div class="info-card">
                        <div class="info-title">🏥 Medical Uses</div>
                        <div class="info-content">{{ tablet.use_cases }}</div>
                    </div>
                    
                    {% if tablet.side_effects %}
                    <div class="info-card">
                        <div class="info-title">⚠️ Side Effects</div>
                        <div class="info-content">{{ tablet.side_effects }}</div>
                    </div>
                    {% endif %}
                    
                    {% if tablet.precautions %}
                    <div class="info-card">
                        <div class="info-title">⚡ Precautions</div>
                        <div class="info-content">{{ tablet.precautions }}</div>
                    </div>
                    {% endif %}
                    
                    {% if tablet.storage_instructions %}
                    <div class="info-card">
                        <div class="info-title">🏠 Storage Instructions</div>
                        <div class="info-content">{{ tablet.storage_instructions }}</div>
                    </div>
                    {% endif %}
                </div>
                
                <div style="text-align: center; margin-top: 30px; color: #666; font-size: 0.9em;">
                    <p>Always consult your healthcare provider.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return render_template_string(html_template, tablet=tablet, today=date.today(), datetime=datetime)
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>", 404

# ============================================================================
# THIS IS THE IMPORTANT PART - AUTOMATIC IP DETECTION
# ============================================================================
if __name__ == '__main__':
    import socket
    
    def get_local_ip():
        """Automatically detect the local network IP address"""
        try:
            # Create a socket to get the local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    local_ip = get_local_ip()
    
    print("=" * 70)
    print("🚀 PHARMACEUTICAL QR CODE MANAGER")
    print("=" * 70)
    print(f"\n📱 Access from THIS LAPTOP:")
    print(f"   http://localhost:5000")
    print(f"\n📱 Access from PHONE/TABLET (same WiFi):")
    print(f"   http://{local_ip}:5000")
    print(f"\n📊 Database: tablets.db")
    print(f"\n⚠️  IMPORTANT INSTRUCTIONS:")
    print(f"   1. Other devices must be on the SAME WiFi network")
    print(f"   2. When creating QR codes, use the phone URL: http://{local_ip}:5000")
    print(f"   3. Allow port 5000 in Windows Firewall if needed")
    print("=" * 70)
    print()
    
    # Run the app with network access enabled
    app.run(debug=True, host='0.0.0.0', port=5000)
