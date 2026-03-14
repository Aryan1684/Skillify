# 🎓 Skillify — Learn, Share & Grow Together

> A full-stack community platform where you can **share skills**, **request learning sessions**, **borrow resources**, and **earn rewards** — all in one place.

---

## 📚 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Pages & Modules](#-pages--modules)
- [Firebase Configuration](#-firebase-configuration)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**Skillify** is a skill-sharing and learning platform built for communities. It connects learners with verified experts, allows users to post and answer questions, borrow learning resources, and earn **Skill Coins** for every contribution.

Whether you want to learn Python, teach UI/UX design, or find someone to guide you through Machine Learning — Skillify makes it happen.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏠 **Dashboard** | Personal hub showing your activity, enrolled sessions, and earned Skill Coins |
| 🤝 **Skill Share** | Community feed to post questions, share knowledge, and connect with experts |
| 📦 **Borrow** | Lend and borrow learning resources within your community |
| 🎓 **Learn** | Browse verified expert sessions or post a custom learning request |
| 🏅 **Quiz** | Test your skills and earn badges for your knowledge |
| 🔐 **Auth** | Secure registration and login powered by Firebase Authentication |
| 🪙 **Skill Coins** | Gamified reward system — earn coins by contributing and requesting sessions |

---

## 🛠 Tech Stack

### Frontend
| Technology | Usage |
|---|---|
| HTML5 / CSS3 | Page structure and styling |
| Vanilla JavaScript | Client-side interactivity |
| Firebase JS SDK | Auth & real-time data on the client |

### Backend
| Technology | Usage |
|---|---|
| Python 3 | Core backend language |
| Flask | Web framework and REST API |
| Firebase Admin SDK | Server-side auth and Firestore integration |
| Railway | Cloud deployment platform |

---

## 📁 Project Structure

```
Skillify/
├── frontend/                   # All client-side code
│   ├── index.html              # Landing / Home page
│   ├── dashboard.html          # User dashboard
│   ├── learn.html              # Browse & request learning sessions
│   ├── skill-share.html        # Community Q&A feed
│   ├── borrow.html             # Resource lending/borrowing
│   ├── test.html               # Skill quiz / badge system
│   ├── auth.html               # Login & registration
│   ├── styles/
│   │   └── main.css            # Global design system & CSS variables
│   └── js/
│       ├── firebase-config.js  # Firebase initialization & BACKEND_URL
│       └── auth.js             # Auth helpers, Profile, Toast, SkillCoins
│
├── backend/                    # Flask REST API
│   ├── app.py                  # App entry point
│   ├── routes/                 # API blueprints (one file per feature)
│   └── serviceAccountKey.json  # Firebase service account (⚠️ NOT committed)
│
├── requirements.txt            # Python dependencies
├── railway.json                # Railway deployment config
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- **Python 3.8+** — [Download](https://python.org)
- **pip** — comes bundled with Python
- **A Firebase project** — [Create one here](https://console.firebase.google.com)
- *(Optional)* **Node.js** — for serving the frontend locally with `npx serve`

---

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aryan1684/Skillify.git
   cd Skillify
   ```

2. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

3. **Create and activate a virtual environment**
   ```bash
   python -m venv venv

   # macOS / Linux
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Add your Firebase service account**

   Download your `serviceAccountKey.json` from the [Firebase Console](https://console.firebase.google.com) under:
   > Project Settings → Service Accounts → Generate new private key

   Place it inside the `backend/` directory:
   ```
   backend/serviceAccountKey.json
   ```

   > ⚠️ **Never commit this file.** It's already listed in `.gitignore`.

6. **Start the Flask server**
   ```bash
   python app.py
   ```

   The backend API will be available at:
   ```
   http://localhost:5000/api
   ```

---

### Frontend Setup

The frontend is made up of plain static files — no build step needed.

**Option 1 — Open directly in browser:**
```bash
open frontend/index.html
# or just double-click the file in your file explorer
```

**Option 2 — Serve locally with Node.js:**
```bash
cd frontend
npx serve .
```
Then visit `http://localhost:3000`.

> 💡 Make sure `js/firebase-config.js` has your Firebase project credentials and the correct `BACKEND_URL` pointing to your running Flask server.

---

## 📄 Pages & Modules

| Page | File | Description |
|---|---|---|
| Home | `index.html` | Landing page with platform overview |
| Dashboard | `dashboard.html` | User's personal activity hub |
| Learn | `learn.html` | Search sessions, browse experts, post custom requests |
| Skill Share | `skill-share.html` | Community feed — ask, answer, share knowledge |
| Borrow | `borrow.html` | Lend and borrow learning resources |
| Quiz | `test.html` | Skill assessment and badge earning |
| Auth | `auth.html` | Login / Register with Firebase Auth |

---

## 🔥 Firebase Configuration

This project uses **Firebase** for both authentication and data storage. You need to configure it in two places:

### 1. Frontend (`frontend/js/firebase-config.js`)
Replace the placeholder config with your own Firebase project credentials:
```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};

const BACKEND_URL = "http://localhost:5000/api"; // Change in production
```

### 2. Backend (`backend/serviceAccountKey.json`)
Download from Firebase Console → Project Settings → Service Accounts.

---

## ☁️ Deployment

This project is configured for deployment on **Railway**.

The `railway.json` file at the root handles the backend service configuration automatically.

**Steps to deploy:**
1. Push your code to GitHub.
2. Go to [Railway](https://railway.app) and create a new project from your GitHub repo.
3. Add the following environment variables in Railway's dashboard:
   - `FIREBASE_CREDENTIALS` — contents of your `serviceAccountKey.json` (as a JSON string)
4. Update `BACKEND_URL` in `frontend/js/firebase-config.js` to point to your Railway deployment URL.
5. Host the `frontend/` folder using [GitHub Pages](https://pages.github.com), [Vercel](https://vercel.com), or [Netlify](https://netlify.com).

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a new branch: `git checkout -b feature/your-feature-name`
3. **Make your changes** and commit: `git commit -m "feat: add your feature"`
4. **Push** to your fork: `git push origin feature/your-feature-name`
5. **Open a Pull Request** on the main repo

Please open an [issue](https://github.com/Aryan1684/Skillify/issues) first for major changes so we can discuss before implementation.

---

## 📜 License

This project is open-source. Feel free to use, modify, and distribute it with attribution.

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/Aryan1684">Aryan</a>
  <br/>
  <sub>⭐ Star this repo if you found it helpful!</sub>
</div>
