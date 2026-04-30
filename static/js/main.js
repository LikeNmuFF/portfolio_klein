// ==================== UTILITIES ====================

function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  if (type === 'error') {
    toast.style.borderLeftColor = 'var(--accent3)';
  }
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease-out forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
}

function renderStars(rating) {
  const stars = [];
  for (let i = 1; i <= 5; i++) {
    stars.push(i <= rating ? '⭐' : '☆');
  }
  return stars.join('');
}

// ==================== NAVIGATION ====================

document.addEventListener('DOMContentLoaded', function() {
  // Hamburger menu
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');
  
  if (hamburger) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });

    navLinks.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => navLinks.classList.remove('open'));
    });
  }

  // Reveal on scroll
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => entry.target.classList.add('visible'), 60);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    
    reveals.forEach(el => observer.observe(el));
  }

  // Stagger project cards
  document.querySelectorAll('.project-card.reveal').forEach((card, i) => {
    card.style.transitionDelay = (i * 80) + 'ms';
  });
});

// ==================== RATING SUBMISSION ====================

const ratingForm = document.getElementById('ratingForm');
if (ratingForm) {
  ratingForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
      name: document.getElementById('ratingName').value,
      email: document.getElementById('ratingEmail').value,
      rating: parseInt(document.getElementById('ratingStars').value),
      review: document.getElementById('ratingReview').value
    };

    try {
      const response = await fetch('/api/submit-rating', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        ratingForm.reset();
        showToast('Thank you! Your rating has been submitted.');
        
        // Optionally reload ratings display
        setTimeout(() => {
          location.reload();
        }, 1500);
      } else {
        showToast(data.error || 'Error submitting rating', 'error');
      }
    } catch (error) {
      showToast('Error submitting rating: ' + error.message, 'error');
    }
  });
}

// ==================== FORM SUBMISSION ====================

function handleSubmit(e) {
  e.preventDefault();
  const btn = document.getElementById('submitBtn');
  const msg = document.getElementById('formMsg');
  
  if (!btn) return;
  
  btn.textContent = 'sending...';
  btn.disabled = true;
  
  setTimeout(() => {
    btn.textContent = 'sent ✓';
    if (msg) {
      msg.style.display = 'block';
      msg.textContent = 'Thanks! I\'ll get back to you soon.';
    }
    e.target.reset();
    
    setTimeout(() => {
      btn.textContent = 'send message →';
      btn.disabled = false;
      if (msg) msg.style.display = 'none';
    }, 4000);
  }, 1200);
}

// ==================== DYNAMIC RATINGS LOADING ====================

async function loadAndDisplayRatings() {
  const ratingsContainer = document.getElementById('ratingsList');
  if (!ratingsContainer) return;

  try {
    const response = await fetch('/api/ratings');
    const data = await response.json();
    
    if (data.ratings && data.ratings.length > 0) {
      ratingsContainer.innerHTML = data.ratings.map(rating => `
        <div class="rating-item">
          <div class="rating-name">${rating.name}</div>
          <div class="rating-email">${rating.email_masked}</div>
          <div class="rating-stars">${renderStars(rating.rating)}</div>
          <div class="rating-text">"${rating.review}"</div>
          <div class="rating-date">${formatDate(rating.created_at)}</div>
        </div>
      `).join('');
    }
  } catch (error) {
    console.error('Error loading ratings:', error);
  }
}

// Load ratings on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadAndDisplayRatings);
} else {
  loadAndDisplayRatings();
}

// ==================== SMOOTH SCROLL ANIMATIONS ── */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href !== '#' && document.querySelector(href)) {
      e.preventDefault();
      document.querySelector(href).scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});

// Add CSS keyframes for slideOut animation
const style = document.createElement('style');
style.textContent = `
  @keyframes slideOut {
    to {
      transform: translateX(400px);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);

// ==================== MODAL HANDLING ====================

// Close modal when clicking outside
const ratingModal = document.getElementById('ratingModal');
if (ratingModal) {
  window.addEventListener('click', function(event) {
    if (event.target === ratingModal) {
      ratingModal.style.display = 'none';
    }
  });

  // Close modal on Escape key
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && ratingModal.style.display === 'flex') {
      ratingModal.style.display = 'none';
    }
  });
}

