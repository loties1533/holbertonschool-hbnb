/* ============================================================
   HBnB — scripts.js
   API base : http://localhost:5000/api/v1
   Auth     : JWT dans cookie "token"

   Endpoints confirmés (code Flask Part 3) :
     POST /api/v1/auth/login
       body : { email, password }
       resp : { access_token }

     GET  /api/v1/places/
       resp : [{ id, title, price, latitude, longitude }]

     GET  /api/v1/places/<id>
       resp : { id, title, description, price, latitude, longitude,
                owner: { id, first_name, last_name, email },
                amenities: [{ id, name }] }

     GET  /api/v1/places/<id>/reviews
       resp : [{ id, text, rating, user: { first_name, last_name } }]
              (enrichi côté serveur dans places.py)

     POST /api/v1/reviews/
       header : Authorization: Bearer <token>
       body   : { text, rating, user_id, place_id }
       Note   : user_id écrasé par get_jwt_identity() côté serveur,
                mais requis par validate=True du modèle Flask-RESTX
       resp ok: { id, text, rating, user_id, place_id }
       erreurs: "You cannot review your own place"
                "You have already reviewed this place"
                "Place not found"
   ============================================================ */

'use strict';

const API_BASE = 'http://localhost:5000/api/v1';

/* ─────────────────────────────────────────────
   UTILITAIRES
   ───────────────────────────────────────────── */

/**
 * Lit un cookie par son nom.
 * @param {string} name
 * @returns {string|null}
 */
function getCookie(name) {
    const match = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return match ? decodeURIComponent(match.split('=')[1]) : null;
}

/**
 * Extrait un paramètre GET de l'URL.
 * @param {string} key
 * @returns {string|null}
 */
function getQueryParam(key) {
    return new URLSearchParams(window.location.search).get(key);
}

/**
 * Décode le payload JWT (sans vérification de signature).
 * Flask-JWT-Extended place le user_id dans le champ "sub".
 * @param {string} token
 * @returns {string}
 */
function getUserIdFromToken(token) {
    try {
        return JSON.parse(atob(token.split('.')[1])).sub || '';
    } catch (_) {
        return '';
    }
}

/**
 * Échappe les caractères HTML (protection XSS).
 * @param {string|number} str
 * @returns {string}
 */
function escapeHtml(str) {
    if (str === null || str === undefined) { return ''; }
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

/**
 * Génère les étoiles ★/☆ pour une note de 1 à 5.
 * Exemple : renderStars(4) → "★★★★☆"
 * @param {number} rating
 * @returns {string}
 */
function renderStars(rating) {
    const n = Math.max(1, Math.min(5, parseInt(rating, 10) || 0));
    return '\u2605'.repeat(n) + '\u2606'.repeat(5 - n);
}

/** Affiche un spinner dans un élément. */
function showLoader(el) {
    el.innerHTML = `
        <div class="state-container">
            <div class="loader"></div>
            <p>Loading&hellip;</p>
        </div>`;
}

/** Affiche une erreur en état vide dans un conteneur. */
function showStateError(el, msg) {
    el.innerHTML = `
        <div class="state-container">
            <p class="error-msg">${escapeHtml(msg)}</p>
        </div>`;
}

/**
 * Affiche un message de feedback (erreur ou succès) dans un div.
 * @param {HTMLElement} el
 * @param {string} msg
 * @param {'error'|'success'} type
 */
function showFeedback(el, msg, type) {
    el.className    = type === 'success' ? 'success-msg' : 'error-msg';
    el.textContent  = msg;
    el.style.display = 'block';
}

function hideFeedback(el) {
    el.style.display = 'none';
    el.textContent   = '';
}


/* ─────────────────────────────────────────────
   ROUTEUR — initialise la bonne page
   ───────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    if (path.includes('login.html'))      { initLogin();     }
    else if (path.includes('place.html')) { initPlace();     }
    else if (path.includes('add_review')) { initAddReview(); }
    else                                  { initIndex();     }
});


/* ═════════════════════════════════════════════
   PAGE : login.html — TASK 1
   ─────────────────────────────────────────────
   POST /api/v1/auth/login
   body : { email, password }
   ok   : stocke cookie "token" + redirect index.html
   fail : affiche message dans #login-error
   ═════════════════════════════════════════════ */

function initLogin() {
    const form     = document.getElementById('login-form');
    const errorBox = document.getElementById('login-error');
    if (!form) { return; }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        hideFeedback(errorBox);

        const email    = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const btn      = form.querySelector('button[type="submit"]');

        btn.disabled    = true;
        btn.textContent = 'Logging in\u2026';

        try {
            await loginUser(email, password);
        } catch (err) {
            showFeedback(errorBox, err.message, 'error');
            btn.disabled    = false;
            btn.textContent = 'Login';
        }
    });
}

async function loginUser(email, password) {
    let response;
    try {
        response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
    } catch (_) {
        throw new Error('Cannot reach the server. Is the API running on localhost:5000?');
    }

    if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.error || 'Invalid credentials. Please try again.');
    }

    const data = await response.json();
    // Stockage du JWT dans un cookie de session (path=/ → accessible sur toutes les pages)
    document.cookie = `token=${encodeURIComponent(data.access_token)}; path=/`;
    window.location.href = 'index.html';
}


/* ═════════════════════════════════════════════
   PAGE : index.html — TASK 2
   ─────────────────────────────────────────────
   - Vérifie auth → affiche/masque #login-link
   - GET /api/v1/places/ → cartes .place-card
   - Filtre #price-filter côté client
   ═════════════════════════════════════════════ */

let allPlaces = [];

function initIndex() {
    const token     = getCookie('token');
    const loginLink = document.getElementById('login-link');

    // Login link : visible si non connecté, caché si connecté
    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'inline';
    }

    fetchPlaces(token);
    initPriceFilter();
}

/**
 * GET /api/v1/places/
 * Réponse : [{ id, title, price, latitude, longitude }]
 */
async function fetchPlaces(token) {
    const list = document.getElementById('places-list');
    showLoader(list);

    const headers = {};
    if (token) { headers['Authorization'] = `Bearer ${token}`; }

    try {
        const res = await fetch(`${API_BASE}/places/`, { headers });
        if (!res.ok) { throw new Error(`Server error ${res.status}`); }
        allPlaces = await res.json();
        displayPlaces(allPlaces);
    } catch (err) {
        showStateError(list, `Could not load places: ${err.message}`);
    }
}

/**
 * Crée les .place-card dans #places-list.
 * Format affiché aligné sur le screenshot :
 *   [Title]
 *   Price per night: $X
 *   [View Details button]
 */
function displayPlaces(places) {
    const list = document.getElementById('places-list');
    list.innerHTML = '';

    if (!places.length) {
        list.innerHTML = `
            <div class="state-container">
                <p>No places match your filter.</p>
            </div>`;
        return;
    }

    places.forEach((place, index) => {
        const article = document.createElement('article');
        // CLASSE IMPOSÉE
        article.className       = 'place-card';
        article.dataset.price   = place.price;
        article.style.animationDelay = `${index * 0.05}s`;

        article.innerHTML = `
            <h3>${escapeHtml(place.title)}</h3>
            <p class="price">Price per night: $${escapeHtml(place.price)}</p>
            <a href="place.html?id=${escapeHtml(place.id)}" class="details-button">View Details</a>
        `;
        list.appendChild(article);
    });
}

/**
 * Filtre les .place-card selon le prix sélectionné.
 * Options : 10 / 50 / 100 / "all" (All)
 */
function initPriceFilter() {
    const select = document.getElementById('price-filter');
    if (!select) { return; }

    select.addEventListener('change', () => {
        const value = select.value;
        document.querySelectorAll('.place-card').forEach(card => {
            const price = parseFloat(card.dataset.price);
            card.style.display = (value === 'all' || price <= parseFloat(value)) ? '' : 'none';
        });
    });
}


/* ═════════════════════════════════════════════
   PAGE : place.html — TASK 3
   ─────────────────────────────────────────────
   - GET /api/v1/places/<id>          → détails
   - GET /api/v1/places/<id>/reviews  → reviews
   - #add-review visible si connecté
   ═════════════════════════════════════════════ */

function initPlace() {
    const placeId = getQueryParam('id');
    if (!placeId) { window.location.href = 'index.html'; return; }

    const token     = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (loginLink) { loginLink.style.display = token ? 'none' : 'inline'; }

    // Section "Add a Review" : visible seulement si connecté
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    fetchPlaceDetails(token, placeId);
    fetchPlaceReviews(token, placeId);

    if (token) { initInlineReviewForm(token, placeId); }
}

/**
 * GET /api/v1/places/<place_id>
 * Réponse : { id, title, description, price, latitude, longitude,
 *              owner: { first_name, last_name }, amenities: [{name}] }
 *
 * Rendu aligné sur le screenshot img_place :
 *   <h1>Beautiful Beach House</h1>  ← centré, en dehors de la card
 *   <div class="place-details">
 *     <div class="place-info">
 *       <p><strong>Host:</strong> John Doe</p>
 *       <p><strong>Price per night:</strong> $150</p>
 *       <p><strong>Description:</strong> ...</p>
 *       <p><strong>Amenities:</strong> WiFi, Pool, Air Conditioning</p>
 *     </div>
 *   </div>
 */
async function fetchPlaceDetails(token, placeId) {
    const container = document.getElementById('place-details');
    showLoader(container);

    const headers = {};
    if (token) { headers['Authorization'] = `Bearer ${token}`; }

    try {
        const res = await fetch(`${API_BASE}/places/${placeId}`, { headers });
        if (!res.ok) { throw new Error('Place not found'); }
        const place = await res.json();
        displayPlaceDetails(place);
    } catch (err) {
        showStateError(container, err.message);
    }
}

function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    document.title  = `HBnB \u2014 ${place.title}`;

    const ownerName = place.owner
        ? `${escapeHtml(place.owner.first_name)} ${escapeHtml(place.owner.last_name)}`
        : 'Unknown';

    const amenitiesStr = (place.amenities && place.amenities.length)
        ? place.amenities.map(a => escapeHtml(a.name)).join(', ')
        : 'None';

    // Structure exacte du screenshot :
    // h1 centré AU-DESSUS de la card blanche, puis card avec les infos
    container.innerHTML = `
        <h1>${escapeHtml(place.title)}</h1>
        <div class="place-details">
            <div class="place-info">
                <p><strong>Host:</strong> ${ownerName}</p>
                <p><strong>Price per night:</strong> $${escapeHtml(place.price)}</p>
                <p><strong>Description:</strong> ${escapeHtml(place.description || 'No description available.')}</p>
                <p><strong>Amenities:</strong> ${amenitiesStr}</p>
            </div>
        </div>
    `;
}

/**
 * GET /api/v1/places/<place_id>/reviews
 * Réponse : [{ id, text, rating, user: { first_name, last_name } }]
 *
 * Rendu aligné sur le screenshot img_place :
 *   Jane Smith:
 *   Great place to stay!
 *   Rating: ★★★★☆
 */
async function fetchPlaceReviews(token, placeId) {
    const section = document.getElementById('reviews');
    const loader  = document.createElement('div');
    loader.style.cssText = 'text-align:center; padding:1rem;';
    loader.innerHTML     = '<div class="loader"></div>';
    section.appendChild(loader);

    const headers = {};
    if (token) { headers['Authorization'] = `Bearer ${token}`; }

    try {
        const res = await fetch(`${API_BASE}/places/${placeId}/reviews`, { headers });
        if (!res.ok) { throw new Error('Could not load reviews'); }
        const reviews = await res.json();
        loader.remove();
        displayReviews(reviews, section);
    } catch (err) {
        loader.remove();
        const p = document.createElement('p');
        p.className   = 'error-msg';
        p.textContent = err.message;
        section.appendChild(p);
    }
}

function displayReviews(reviews, section) {
    if (!reviews.length) {
        const p = document.createElement('p');
        p.style.cssText = 'color:#666; padding:.5rem 20px;';
        p.textContent   = 'No reviews yet. Be the first!';
        section.appendChild(p);
        return;
    }

    reviews.forEach((review, index) => {
        const card = document.createElement('article');
        // CLASSE IMPOSÉE
        card.className          = 'review-card';
        card.style.animationDelay = `${index * 0.07}s`;

        const userName = review.user
            ? `${escapeHtml(review.user.first_name)} ${escapeHtml(review.user.last_name)}`
            : 'Anonymous';

        // Format exact du screenshot : "Jane Smith:" / texte / "Rating: ★★★★☆"
        card.innerHTML = `
            <p class="reviewer">${userName}:</p>
            <p class="review-text">${escapeHtml(review.text)}</p>
            <p class="rating-line">Rating: <span class="stars">${renderStars(review.rating)}</span></p>
        `;
        section.appendChild(card);
    });
}

/**
 * Formulaire de review inline sur place.html.
 * POST /api/v1/reviews/
 */
function initInlineReviewForm(token, placeId) {
    const form       = document.getElementById('review-form');
    const feedbackEl = document.getElementById('review-feedback');
    if (!form) { return; }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        hideFeedback(feedbackEl);

        const text   = document.getElementById('review-text').value.trim();
        const rating = parseInt(document.getElementById('rating').value, 10);

        if (!text) {
            showFeedback(feedbackEl, 'Please write your review.', 'error');
            return;
        }

        const btn = form.querySelector('button[type="submit"]');
        btn.disabled    = true;
        btn.textContent = 'Submitting\u2026';

        try {
            await submitReview(token, placeId, text, rating);
            showFeedback(feedbackEl, 'Review submitted! Refreshing\u2026', 'success');
            form.reset();
            // Rafraîchir la liste des reviews
            setTimeout(() => {
                const section = document.getElementById('reviews');
                [...section.children].forEach(child => {
                    if (child.tagName !== 'H2') { child.remove(); }
                });
                fetchPlaceReviews(token, placeId);
                hideFeedback(feedbackEl);
            }, 1500);
        } catch (err) {
            showFeedback(feedbackEl, err.message, 'error');
        } finally {
            btn.disabled    = false;
            btn.textContent = 'Submit Review';
        }
    });
}


/* ═════════════════════════════════════════════
   PAGE : add_review.html — TASK 4
   ─────────────────────────────────────────────
   - Redirige vers index.html si non authentifié
   - Affiche "Reviewing: [Place Title]" en h1
   - POST /api/v1/reviews/ + redirect place.html
   ═════════════════════════════════════════════ */

function initAddReview() {
    // Vérification auth : redirect si non connecté
    const token = getCookie('token');
    if (!token) { window.location.href = 'index.html'; return; }

    const placeId = getQueryParam('id');
    if (!placeId) { window.location.href = 'index.html'; return; }

    // Lien "back to place"
    const backLink = document.getElementById('back-to-place');
    if (backLink) { backLink.href = `place.html?id=${placeId}`; }

    // Charge le titre de la place pour le h1 "Reviewing: [Title]"
    loadPlaceTitle(token, placeId);

    const form       = document.getElementById('review-form');
    const feedbackEl = document.getElementById('review-feedback');
    if (!form) { return; }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        hideFeedback(feedbackEl);

        const text   = document.getElementById('review').value.trim();
        const rating = parseInt(document.getElementById('rating').value, 10);

        if (!text) {
            showFeedback(feedbackEl, 'Please write your review.', 'error');
            return;
        }

        const btn = form.querySelector('button[type="submit"]');
        btn.disabled    = true;
        btn.textContent = 'Submitting\u2026';

        try {
            await submitReview(token, placeId, text, rating);
            showFeedback(feedbackEl, 'Review submitted! Redirecting\u2026', 'success');
            form.reset();
            setTimeout(() => { window.location.href = `place.html?id=${placeId}`; }, 1800);
        } catch (err) {
            showFeedback(feedbackEl, err.message, 'error');
            btn.disabled    = false;
            btn.textContent = 'Submit Review';
        }
    });
}

/**
 * Charge le titre de la place et l'injecte dans #review-page-title.
 * Résultat : "Reviewing: Beautiful Beach House"
 */
async function loadPlaceTitle(token, placeId) {
    try {
        const res = await fetch(`${API_BASE}/places/${placeId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) { return; }
        const place = await res.json();

        const titleEl = document.getElementById('review-page-title');
        if (titleEl) { titleEl.textContent = `Reviewing: ${place.title}`; }
        document.title = `HBnB \u2014 Reviewing: ${place.title}`;
    } catch (_) { /* silencieux — formulaire reste fonctionnel */ }
}


/* ─────────────────────────────────────────────
   FONCTION PARTAGÉE — submitReview
   Utilisée par initInlineReviewForm + initAddReview
   ───────────────────────────────────────────── */

/**
 * POST /api/v1/reviews/
 * Header : Authorization: Bearer <token>
 * Body   : { text, rating, user_id, place_id }
 *
 * Note importante : le modèle Flask-RESTX a validate=True et requiert user_id.
 * Côté serveur, review_data['user_id'] = get_jwt_identity() écrase la valeur.
 * On envoie quand même user_id (extrait du JWT) pour passer la validation.
 *
 * @param {string} token
 * @param {string} placeId
 * @param {string} text
 * @param {number} rating
 * @throws {Error} avec le message d'erreur de l'API
 */
async function submitReview(token, placeId, text, rating) {
    const userId = getUserIdFromToken(token);

    // --- ON AJOUTE ÇA ICI POUR VOIR LE PROBLÈME DANS F12 ---
    console.log("DEBUG -> Token récupéré:", token);
    console.log("DEBUG -> UserID extrait:", userId);
    console.log("DEBUG -> PlaceID utilisé:", placeId);
    // -------------------------------------------------------

    let response;
    try {
        response = await fetch(`${API_BASE}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type':  'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text:     text,
                rating:   rating,
                user_id:  userId,
                place_id: placeId
            })
        });
    } catch (_) {
        throw new Error('Cannot reach the server. Is the API running?');
    }

    if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        // On affiche aussi l'erreur précise du serveur en console
        console.error("Erreur API détaillée:", data);
        throw new Error(data.error || `Error ${response.status}`);
    }

    return response.json();
}