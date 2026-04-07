const API = 'http://localhost:5000/api/v1';

function getCookie(name) {
    const match = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return match ? match.split('=')[1] : null;
}

function getQueryParam(key) {
    return new URLSearchParams(window.location.search).get(key);
}

function showLoader(container) {
    container.innerHTML = `
        <div class="state-container">
            <div class="loader"></div>
            <p>Loading…</p>
        </div>`;
}

function showError(container, message) {
    container.innerHTML = `
        <div class="state-container">
            <p class="error-msg">⚠ ${message}</p>
        </div>`;
}

function renderStars(rating) {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
}

document.addEventListener('DOMContentLoaded', () => {
    const page = document.body.dataset.page || detectPage();

    if (page === 'index')      initIndex();
    if (page === 'login')      initLogin();
    if (page === 'place')      initPlace();
    if (page === 'add_review') initAddReview();
});

function detectPage() {
    const path = window.location.pathname;
    if (path.includes('login'))      return 'login';
    if (path.includes('place.html')) return 'place';
    if (path.includes('add_review')) return 'add_review';
    return 'index';
}

function initLogin() {
    const form      = document.getElementById('login-form');
    const errorBox  = document.getElementById('login-error');

    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorBox.style.display = 'none';

        const email    = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        try {
            await loginUser(email, password);
        } catch (err) {
            errorBox.textContent = err.message;
            errorBox.style.display = 'block';
        }
    });
}

async function loginUser(email, password) {
    const response = await fetch(`${API}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.error || 'Invalid credentials. Please try again.');
    }

    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
}

let allPlaces = [];

function initIndex() {
    checkAuthIndex();
    initPriceFilter();
}

function checkAuthIndex() {
    const token     = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (token) {
        if (loginLink) loginLink.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'inline-block';
    }

    fetchPlaces(token);
}

async function fetchPlaces(token) {
    const list = document.getElementById('places-list');
    showLoader(list);

    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const res = await fetch(`${API}/places/`, { headers });
        if (!res.ok) throw new Error(`Server error ${res.status}`);
        allPlaces = await res.json();
        displayPlaces(allPlaces);
    } catch (err) {
        showError(list, `Could not load places: ${err.message}`);
    }
}

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

    places.forEach((place, i) => {
        const card = document.createElement('article');
        card.className = 'place-card';
        card.dataset.price = place.price;
        card.style.animationDelay = `${i * 0.06}s`;

        card.innerHTML = `
            <h3>${escapeHtml(place.title)}</h3>
            <p class="price">$${place.price} <span>/ night</span></p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        list.appendChild(card);
    });
}

function initPriceFilter() {
    const select = document.getElementById('price-filter');
    if (!select) return;

    select.addEventListener('change', () => {
        const value = select.value;
        const cards = document.querySelectorAll('.place-card');

        cards.forEach(card => {
            const price = parseFloat(card.dataset.price);
            if (value === 'all' || price <= parseFloat(value)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

function initPlace() {
    const placeId = getQueryParam('id');
    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    const token     = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (token && loginLink) loginLink.style.display = 'none';

    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    fetchPlaceDetails(token, placeId);
    fetchPlaceReviews(token, placeId);

    initInlineReviewForm(token, placeId);
}

async function fetchPlaceDetails(token, placeId) {
    const section = document.getElementById('place-details');
    showLoader(section);

    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const res = await fetch(`${API}/places/${placeId}`, { headers });
        if (!res.ok) throw new Error('Place not found');
        const place = await res.json();
        displayPlaceDetails(place);
    } catch (err) {
        showError(section, err.message);
    }
}

function displayPlaceDetails(place) {
    const section = document.getElementById('place-details');

    document.title = `HBnB — ${place.title}`;

    const amenitiesHtml = place.amenities && place.amenities.length
        ? `<div class="amenities-list">
               ${place.amenities.map(a =>
                   `<span class="amenity-tag">${escapeHtml(a.name)}</span>`
               ).join('')}
           </div>`
        : '<p style="color:var(--text-muted); font-size:.9rem;">No amenities listed.</p>';

    const ownerName = place.owner
        ? `${escapeHtml(place.owner.first_name)} ${escapeHtml(place.owner.last_name)}`
        : 'Unknown host';

    section.innerHTML = `
        <div class="place-details">
            <h1>${escapeHtml(place.title)}</h1>

            <div class="place-info">
                <span class="badge price-badge">$${place.price} / night</span>
                <span class="badge">🧑 Host: ${ownerName}</span>
                ${place.latitude ? `<span class="badge">📍 ${place.latitude.toFixed(4)}, ${place.longitude.toFixed(4)}</span>` : ''}
            </div>

            <p style="margin: 1rem 0; line-height:1.7; color:var(--text);">
                ${escapeHtml(place.description || 'No description available.')}
            </p>

            <h3 style="margin-bottom:.6rem; font-family:'Playfair Display',serif;">Amenities</h3>
            ${amenitiesHtml}
        </div>
    `;
}

async function fetchPlaceReviews(token, placeId) {
    const section = document.getElementById('reviews');
    const loader = document.createElement('div');
    loader.className = 'state-container';
    loader.innerHTML = '<div class="loader"></div>';
    section.appendChild(loader);

    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const res = await fetch(`${API}/places/${placeId}/reviews`, { headers });
        if (!res.ok) throw new Error('Could not load reviews');
        const reviews = await res.json();
        displayReviews(reviews);
    } catch (err) {
        loader.remove();
        const errEl = document.createElement('p');
        errEl.className = 'error-msg';
        errEl.textContent = err.message;
        section.appendChild(errEl);
    }
}

function displayReviews(reviews) {
    const section = document.getElementById('reviews');
    [...section.children].forEach(child => {
        if (child.tagName !== 'H2') child.remove();
    });

    if (!reviews.length) {
        const empty = document.createElement('p');
        empty.style.cssText = 'color:var(--text-muted); padding:1rem 0;';
        empty.textContent = 'No reviews yet. Be the first!';
        section.appendChild(empty);
        return;
    }

    reviews.forEach((review, i) => {
        const card = document.createElement('article');
        card.className = 'review-card';
        card.style.animationDelay = `${i * 0.07}s`;

        const userName = review.user
            ? `${escapeHtml(review.user.first_name)} ${escapeHtml(review.user.last_name)}`
            : 'Anonymous';

        card.innerHTML = `
            <p class="reviewer">${userName}</p>
            <p class="rating">${renderStars(review.rating)}</p>
            <p class="review-text">${escapeHtml(review.text)}</p>
        `;
        section.appendChild(card);
    });
}

function initInlineReviewForm(token, placeId) {
    const form = document.getElementById('review-form');
    if (!form || !token) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const errorBox = document.getElementById('review-error');
        if (errorBox) errorBox.style.display = 'none';

        const text   = document.getElementById('review-text').value.trim();
        const rating = parseInt(document.getElementById('rating').value);

        if (!text || !rating) {
            if (errorBox) {
                errorBox.textContent = 'Please fill in all fields.';
                errorBox.style.display = 'block';
            }
            return;
        }

        try {
            await submitReviewFromPlace(token, placeId, text, rating);
            form.reset();
            fetchPlaceReviews(token, placeId);
        } catch (err) {
            if (errorBox) {
                errorBox.textContent = err.message;
                errorBox.style.display = 'block';
            }
        }
    });
}

async function submitReviewFromPlace(token, placeId, text, rating) {
    const res = await fetch(`${API}/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            text,
            rating,
            place_id: placeId,
            user_id: getUserIdFromToken(token)
        })
    });

    if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || `Error ${res.status}`);
    }
    return res.json();
}

function initAddReview() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    const placeId = getQueryParam('id');
    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    const backLink = document.getElementById('back-to-place');
    if (backLink) backLink.href = `place.html?id=${placeId}`;

    loadPlaceName(token, placeId);

    const form = document.getElementById('review-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const errorBox = document.getElementById('review-error');
        if (errorBox) errorBox.style.display = 'none';

        const text   = document.getElementById('review').value.trim();
        const rating = parseInt(document.getElementById('rating').value);

        if (!text || !rating) {
            if (errorBox) {
                errorBox.textContent = 'Please fill in all fields.';
                errorBox.style.display = 'block';
            }
            return;
        }

        try {
            await submitReview(token, placeId, text, rating);
            alert('Review submitted successfully! Redirecting…');
            window.location.href = `place.html?id=${placeId}`;
        } catch (err) {
            if (errorBox) {
                errorBox.textContent = err.message;
                errorBox.style.display = 'block';
            }
        }
    });
}

async function loadPlaceName(token, placeId) {
    try {
        const res = await fetch(`${API}/places/${placeId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) return;
        const place = await res.json();
        const label = document.getElementById('place-name-label');
        if (label) label.textContent = `for "${place.title}"`;
        document.title = `HBnB — Review: ${place.title}`;
    } catch (_) {}
}

async function submitReview(token, placeId, text, rating) {
    const res = await fetch(`${API}/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            text,
            rating,
            place_id: placeId,
            user_id: getUserIdFromToken(token)
        })
    });

    if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || `Submission failed (${res.status})`);
    }
    return res.json();
}

function getUserIdFromToken(token) {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.sub || payload.identity || '';
    } catch (_) {
        return '';
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}