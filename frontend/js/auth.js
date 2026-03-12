/**
 * Skillify – Auth Helper (Demo + Firebase)
 */

// ── Demo Auth (localStorage when Firebase not configured) ──────────────────

const DemoAuth = {
    getCurrentUser() {
        const u = localStorage.getItem('skillify_user');
        return u ? JSON.parse(u) : null;
    },
    register(email, password, name) {
        const users = JSON.parse(localStorage.getItem('skillify_users') || '{}');
        if (users[email]) return Promise.reject({ message: 'Email already registered.' });
        const user = { uid: 'u_' + Date.now(), email, name: name || email.split('@')[0], isNew: true };
        users[email] = { ...user, password };
        localStorage.setItem('skillify_users', JSON.stringify(users));
        localStorage.setItem('skillify_user', JSON.stringify(user));
        return Promise.resolve(user);
    },
    login(email, password) {
        const users = JSON.parse(localStorage.getItem('skillify_users') || '{}');
        const u = users[email];
        if (!u || u.password !== password) return Promise.reject({ message: 'Invalid email or password.' });
        const user = { uid: u.uid, email: u.email, name: u.name };
        localStorage.setItem('skillify_user', JSON.stringify(user));
        return Promise.resolve(user);
    },
    logout() {
        localStorage.removeItem('skillify_user');
        return Promise.resolve();
    },
    googleLogin() {
        // Simulate Google login in demo mode
        const user = {
            uid: 'g_' + Date.now(),
            email: 'demo@gmail.com',
            name: 'Demo User',
            isNew: !localStorage.getItem('skillify_google_used')
        };
        localStorage.setItem('skillify_google_used', '1');
        localStorage.setItem('skillify_user', JSON.stringify(user));
        return Promise.resolve(user);
    }
};

// ── Main Auth Module ────────────────────────────────────────────────────────

const Auth = {
    getCurrentUser() {
        if (IS_DEMO) return DemoAuth.getCurrentUser();
        // For real Firebase: check sessionStorage cache first (instant)
        // firebaseAuth.currentUser may be null before onAuthStateChanged fires
        const cached = localStorage.getItem('skillify_fb_user');
        return cached ? JSON.parse(cached) : null;
    },

    async register(email, password, name) {
        if (IS_DEMO) {
            const user = await DemoAuth.register(email, password, name);
            return user;
        }
        const cred = await firebaseAuth.createUserWithEmailAndPassword(email, password);
        await cred.user.updateProfile({ displayName: name });
        const user = { uid: cred.user.uid, email: cred.user.email, name, isNew: true };
        localStorage.setItem('skillify_fb_user', JSON.stringify(user));
        return user;
    },

    async login(email, password) {
        if (IS_DEMO) return DemoAuth.login(email, password);
        const cred = await firebaseAuth.signInWithEmailAndPassword(email, password);
        const user = { uid: cred.user.uid, email: cred.user.email, name: cred.user.displayName };
        localStorage.setItem('skillify_fb_user', JSON.stringify(user));
        return user;
    },

    async googleLogin() {
        if (IS_DEMO) return DemoAuth.googleLogin();
        const provider = new firebase.auth.GoogleAuthProvider();
        const result = await firebaseAuth.signInWithPopup(provider);
        const user = { uid: result.user.uid, email: result.user.email, name: result.user.displayName };
        localStorage.setItem('skillify_fb_user', JSON.stringify(user));
        return user;
    },

    async logout() {
        if (IS_DEMO) return DemoAuth.logout();
        localStorage.removeItem('skillify_fb_user');
        return firebaseAuth.signOut();
    },

    requireAuth() {
        const user = this.getCurrentUser();
        if (!user) { window.location.href = 'auth.html'; return null; }
        return user;
    }
};

// ── Profile Helpers ────────────────────────────────────────────────────────

const Profile = {
    async get(uid) {
        try {
            const res = await fetch(`${BACKEND_URL}/profile/${uid}`);
            if (!res.ok) return null;
            return await res.json();
        } catch {
            // Fallback to localStorage if backend offline
            const p = localStorage.getItem(`skillify_profile_${uid}`);
            return p ? JSON.parse(p) : null;
        }
    },

    async save(data) {
        try {
            const res = await fetch(`${BACKEND_URL}/profile`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await res.json();
            localStorage.setItem(`skillify_profile_${data.uid}`, JSON.stringify(result.profile || data));
            return result;
        } catch {
            // Offline fallback
            localStorage.setItem(`skillify_profile_${data.uid}`, JSON.stringify(data));
            return { success: true, profile: data };
        }
    },

    getLocal(uid) {
        const p = localStorage.getItem(`skillify_profile_${uid}`);
        return p ? JSON.parse(p) : null;
    }
};

// ── Toast Notifications ────────────────────────────────────────────────────

const Toast = {
    container: null,
    init() {
        if (!document.querySelector('.toast-container')) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        } else {
            this.container = document.querySelector('.toast-container');
        }
    },
    show(msg, type = 'info', duration = 3500) {
        if (!this.container) this.init();
        const icons = { success: '✅', error: '❌', info: 'ℹ️', warn: '⚠️' };
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${msg}</span>`;
        this.container.appendChild(toast);
        setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(100%)'; setTimeout(() => toast.remove(), 300); }, duration);
    },
    success(msg) { this.show(msg, 'success'); },
    error(msg) { this.show(msg, 'error'); },
    info(msg) { this.show(msg, 'info'); }
};

// Initialize toast
Toast.init();
