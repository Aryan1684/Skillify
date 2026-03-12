# Skillify

Skillify is a platform designed to facilitate skill sharing, learning, borrowing resources, and community engagement. The project consists of a full-stack architecture with a web frontend and a Python backend.

## Features
- **Dashboard**: Overview of user activities.
- **Skill Sharing**: Connect with others to share and learn new skills.
- **Borrow**: Borrow and lend resources within the community.
- **Learn**: Access learning materials and test your skills.
- **Authentication**: Secure login and registration flows via Firebase.

## Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python (Flask)
- **Database/Auth**: Firebase

## Project Structure
- `frontend/`: Contains all client-side code (HTML, CSS, JS).
- `backend/`: Contains the Flask server, API defined via blueprints (`routes/`), and Firebase integration.

## Getting Started

### Prerequisites
- Python 3.x
- Node.js (optional, for any future frontend build tools like live-server)
- Firebase Account and `serviceAccountKey.json` for backend initialization.

### Running the Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Place your Firebase `serviceAccountKey.json` in the `backend/` directory.
5. Run the server:
   ```bash
   python app.py
   ```
   The backend API will run on `http://localhost:5000/api`.

### Running the Frontend
The frontend consists of static files. You can quickly view it by serving the files via any static file server, for example:
   ```bash
   cd frontend
   npx serve .
   ```
Or you can simply open `frontend/index.html` in your browser.

## Contact / Contribution
For any support or to contribute, please feel free to raise an issue or submit a pull request.
