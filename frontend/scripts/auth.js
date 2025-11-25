// auth.js - Gestion de l'authentification côté frontend

// Stockage et récupération de l'utilisateur connecté
const AUTH_KEY = 'medical_app_auth';

// Stocker les infos utilisateur en localStorage
function storeUserAuth(user) {
    localStorage.setItem(AUTH_KEY, JSON.stringify(user));
}

// Récupérer les infos utilisateur
function getCurrentUser() {
    const userJson = localStorage.getItem(AUTH_KEY);
    return userJson ? JSON.parse(userJson) : null;
}

// Supprimer les infos utilisateur (déconnexion)
function clearUserAuth() {
    localStorage.removeItem(AUTH_KEY);
}

// Vérifier si l'utilisateur est connecté
function isAuthenticated() {
    return getCurrentUser() !== null;
}

// Vérifier si l'utilisateur a le rôle spécifié
function hasRole(role) {
    const user = getCurrentUser();
    return user && user.role === role;
}

// Vérifier si l'utilisateur a l'un des rôles spécifiés
function hasAnyRole(roles) {
    const user = getCurrentUser();
    return user && roles.includes(user.role);
}

// Rediriger si l'utilisateur n'est pas authentifié
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'auth.html'; // Changé de login.html à auth.html
        return false;
    }
    return true;
}

// Rediriger si l'utilisateur n'a pas le rôle requis
function requireRole(role) {
    if (!requireAuth()) return false;
    
    if (!hasRole(role)) {
        alert("Vous n'avez pas les droits nécessaires pour accéder à cette page.");
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

// Rediriger si l'utilisateur n'a aucun des rôles requis
function requireAnyRole(roles) {
    if (!requireAuth()) return false;
    
    if (!hasAnyRole(roles)) {
        alert("Vous n'avez pas les droits nécessaires pour accéder à cette page.");
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

// Connexion
async function login(email, password) {
    try {
        const response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password }),
            credentials: 'include' // Important pour les cookies de session
        });
        
        const data = await response.json();
        
        if (response.ok) {
            storeUserAuth(data.user);
            return { success: true, user: data.user };
        } else {
            return { success: false, message: data.error };
        }
    } catch (error) {
        console.error('Erreur de connexion:', error);
        return { success: false, message: 'Erreur de connexion au serveur' };
    }
}

// Déconnexion
async function logout() {
    try {
        await fetch('http://localhost:5000/logout', {
            method: 'POST',
            credentials: 'include'
        });
        clearUserAuth();
        window.location.href = 'auth.html'; // Changé de login.html à auth.html
    } catch (error) {
        console.error('Erreur de déconnexion:', error);
    }
}

// Vérifier l'état de l'authentification avec le serveur
async function checkAuthStatus() {
    try {
        const response = await fetch('http://localhost:5000/check-auth', {
            credentials: 'include'
        });
        
        const data = await response.json();
        
        if (data.authenticated) {
            storeUserAuth(data.user);
            return true;
        } else {
            clearUserAuth();
            return false;
        }
    } catch (error) {
        console.error('Erreur de vérification d\'authentification:', error);
        return false;
    }
}

// Initialiser l'interface en fonction du rôle
function initializeUI() {
    const user = getCurrentUser();
    
    if (user) {
        // Afficher le nom de l'utilisateur
        const userNameElements = document.querySelectorAll('.user-name');
        userNameElements.forEach(el => {
            el.textContent = user.name;
        });
        
        // Gérer l'affichage des éléments en fonction du rôle
        document.querySelectorAll('[data-role]').forEach(el => {
            const requiredRoles = el.dataset.role.split(',');
            
            if (!hasAnyRole(requiredRoles)) {
                el.style.display = 'none';
            } else {
                el.style.display = '';
            }
        });
    }
}

// Exécuter à chaque chargement de page
document.addEventListener('DOMContentLoaded', function() {
    // Si on est sur une page protégée, vérifier l'authentification
    if (!document.body.classList.contains('public-page')) {
        checkAuthStatus().then(isAuth => {
            if (!isAuth && window.location.pathname !== '/auth.html') { // Changé de login.html à auth.html
                window.location.href = 'auth.html'; // Changé de login.html à auth.html
            } else {
                initializeUI();
            }
        });
    }
    
    // Gérer les boutons de déconnexion
    document.querySelectorAll('.logout-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    });
});