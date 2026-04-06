/* HBnB Evolution - Part 4 Scripts */
const API_URL = 'http://localhost:5000/api/v1';

// --- 1. UTILITAIRES (Cookies & Auth) ---

function getCookie(name) {
  const nameEQ = name + '=';
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const trimmed = cookie.trim();
    if (trimmed.indexOf(nameEQ) === 0) {
      return trimmed.substring(nameEQ.length);
    }
  }
  return null;
}

function setCookie(name, value, days = 7) {
  const date = new Date();
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value}; expires=${date.toUTCString()}; path=/`;
}

function getUserIdFromToken() {
  const token = getCookie('token');
  if (!token) return null;
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const payload = JSON.parse(window.atob(base64));
    return payload.sub; 
  } catch (e) {
    return null;
  }
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'inline-block';
  }
  return Boolean(token);
}

function showMessage(elementId, message, type = 'error') {
  const el = document.getElementById(elementId);
  if (!el) return;
  el.textContent = message;
  el.style.display = 'block';
  el.style.color = type === 'success' ? 'green' : '#c0392b';
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

// --- 2. GESTION DU LOGIN (Task 01) ---

async function setupLoginForm() {
  const loginForm = document.getElementById('login-form');
  if (!loginForm) return;

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (response.ok) {
        const data = await response.json();
        setCookie('token', data.access_token);
        window.location.href = 'index.html';
      } else {
        const errorData = await response.json().catch(() => ({}));
        showMessage('login-error', errorData.error || 'Login failed.');
      }
    } catch (error) {
      showMessage('login-error', 'Unable to connect to the server.');
    }
  });
}

// --- 3. LISTE DES PLACES & FILTRE (Task 02) ---

let placesData = [];

async function fetchPlaces() {
  try {
    const response = await fetch(`${API_URL}/places/`);
    if (!response.ok) throw new Error('Failed to fetch places');
    placesData = await response.json();
    displayPlaces(placesData);
  } catch (error) {
    const list = document.getElementById('places-list');
    if (list) list.innerHTML = '<p>Unable to load places.</p>';
  }
}

function displayPlaces(places) {
  const list = document.getElementById('places-list');
  if (!list) return;
  list.innerHTML = '';
  places.forEach((place) => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price per night: $${place.price ?? 'N/A'}</p>
      <a class="details-button" href="place.html?id=${place.id}">View Details</a>
    `;
    list.appendChild(card);
  });
}

function setupPriceFilter() {
  const filter = document.getElementById('price-filter');
  if (!filter) return;
  filter.addEventListener('change', () => {
    const maxPrice = filter.value;
    if (!maxPrice) return displayPlaces(placesData);
    displayPlaces(placesData.filter((p) => p.price <= parseFloat(maxPrice)));
  });
}

// --- 4. DETAILS DE LA PLACE (Task 03) ---

async function fetchPlaceDetails() {
  const placeId = getPlaceIdFromURL();
  if (!placeId) return;

  try {
    const response = await fetch(`${API_URL}/places/${placeId}`);
    if (!response.ok) throw new Error('Failed to load place');
    const place = await response.json();
    renderPlaceDetails(place);
    setupReviewButton(placeId);
    await fetchPlaceReviews(placeId);
  } catch (error) {
    const details = document.getElementById('place-details');
    if (details) details.innerHTML = '<p>Unable to load place details.</p>';
  }
}

function renderPlaceDetails(place) {
  const title = document.getElementById('place-title');
  if (title) title.textContent = place.title;

  const detailsSection = document.getElementById('place-details');
  if (!detailsSection) return;

  const amenities = place.amenities && place.amenities.length
    ? place.amenities.map((a) => a.name).join(', ')
    : 'None';

  const ownerName = place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : 'N/A';

  detailsSection.innerHTML = `
    <div class="place-info">
      <p><strong>Host:</strong> ${ownerName}</p>
      <p><strong>Price per night:</strong> $${place.price ?? 'N/A'}</p>
      <p><strong>Description:</strong> ${place.description || 'No description.'}</p>
      <p><strong>Amenities:</strong> ${amenities}</p>
    </div>
  `;
}

// --- 5. GESTION DES REVIEWS (Task 03 & 04) ---

async function fetchPlaceReviews(placeId) {
  try {
    const response = await fetch(`${API_URL}/places/${placeId}/reviews`);
    if (response.ok) {
      const reviews = await response.json();
      renderReviews(reviews);
    }
  } catch (error) {
    renderReviews([]);
  }
}

function renderReviews(reviews) {
  const reviewsSection = document.getElementById('reviews');
  if (!reviewsSection) return;

  let html = '<h2>Reviews</h2>';
  if (!reviews || reviews.length === 0) {
    html += '<p>No reviews yet.</p>';
  } else {
    reviews.forEach((review) => {
      const firstName = review.user ? review.user.first_name : 'Anonymous';
      const lastName = review.user ? review.user.last_name : '';
      const author = `${firstName} ${lastName}`.trim();
      const stars = '★'.repeat(Math.round(review.rating)) + '☆'.repeat(5 - Math.round(review.rating));
      
      html += `
        <div class="review-card">
          <p><strong>${author}</strong></p>
          <p>${review.text}</p>
          <p class="review-rating"><strong>Rating:</strong> ${review.rating}/5 ${stars}</p>
        </div>
      `;
    });
  }
  reviewsSection.innerHTML = html;
}

function setupReviewButton(placeId) {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review');
  const addReviewLink = document.getElementById('add-review-link');
  if (addReviewSection && token) {
    addReviewSection.classList.remove('hidden');
    addReviewLink.href = `add_review.html?id=${placeId}`;
  }
}

function setupAddReviewForm() {
  const reviewForm = document.getElementById('review-form');
  if (!reviewForm) return;

  reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();
    const userId = getUserIdFromToken();

    if (!token) {
      window.location.href = 'index.html';
      return;
    }

    const reviewData = {
      text: document.getElementById('review-text').value.trim(),
      rating: parseInt(document.getElementById('rating').value),
      place_id: placeId,
      user_id: userId
    };

    try {
      const response = await fetch(`${API_URL}/reviews/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(reviewData)
      });

      if (response.ok) {
        showMessage('review-message', 'Review submitted successfully!', 'success');
        setTimeout(() => window.location.href = `place.html?id=${placeId}`, 1500);
      } else {
        const err = await response.json();
        showMessage('review-message', err.error || 'Submission failed.');
      }
    } catch (error) {
      showMessage('review-message', 'Server error.');
    }
  });
}

async function fetchPlaceTitleForReview() {
  const placeId = getPlaceIdFromURL();
  if (!placeId) return;
  const response = await fetch(`${API_URL}/places/${placeId}`);
  if (response.ok) {
    const place = await response.json();
    document.getElementById('review-place-title').textContent = `Add Review for ${place.title}`;
  }
}

// --- INITIALISATION ---

document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  const path = window.location.pathname;
  const page = path.split('/').pop();

  if (page === 'login.html') {
    setupLoginForm();
  } else if (page === 'index.html' || page === '') {
    fetchPlaces();
    setupPriceFilter();
  } else if (page === 'place.html') {
    fetchPlaceDetails();
  } else if (page === 'add_review.html') {
    if (!getCookie('token')) {
      window.location.href = 'index.html'; // Redirection Task 04
    } else {
      fetchPlaceTitleForReview();
      setupAddReviewForm();
    }
  }
});