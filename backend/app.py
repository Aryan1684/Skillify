"""
Skillify - Main Flask Application
=================================
Run with: python app.py
API Base: http://localhost:5000/api
"""

import os
import json
import firebase_admin
from firebase_admin import credentials
from flask import Flask
from flask_cors import CORS
from routes.test_routes import test_bp
from routes.skill_routes import skill_bp
from routes.auth_routes import auth_bp

app = Flask(__name__, 
            static_folder='../frontend', 
            static_url_path='')
CORS(app)

# Initialize Firebase Admin SDK
firebase_service_account = os.environ.get('FIREBASE_SERVICE_ACCOUNT')

try:
    if firebase_service_account:
        # Initialize using environment variable (for Production/Railway)
        service_account_info = json.loads(firebase_service_account)
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase Admin SDK initialized from environment variable.")
    else:
        # Initialize using local file (for Development)
        cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Admin SDK initialized from local JSON file.")
        else:
            print("⚠️ Warning: Firebase credentials not found (Env mapping or JSON file). Using demo mode.")
except Exception as e:
    print(f"❌ Error initializing Firebase Admin SDK: {e}")

# Register blueprints
app.register_blueprint(test_bp, url_prefix='/api')
app.register_blueprint(skill_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')


@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/api/status')
def api_status():
    return {
        "message": "Skillify API is running!",
        "version": "1.0.0-demo",
        "endpoints": {
            "skill_test": "GET /api/test/<skill>",
            "submit_test": "POST /api/test/submit",
            "profile": "GET/POST /api/profile/<uid>",
            "skill_share": "GET/POST /api/skill-share",
            "borrow": "GET/POST /api/borrow",
            "courses": "GET/POST /api/courses"
        }
    }


if __name__ == '__main__':
    print("🚀 Skillify API starting on http://localhost:5000")
    app.run(debug=True, port=5000)
