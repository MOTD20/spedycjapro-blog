document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle for navigation
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.getElementById('nav-links');

    if (menuToggle && navLinks) {
      menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('open');
      });
      // Close menu when clicking outside (mobile UX)
      document.addEventListener('click', (e) => {
        if (!menuToggle.contains(e.target) && !navLinks.contains(e.target)) {
          navLinks.classList.remove('open');
        }
      });
    }
  });
  
// WOW EFFECTS & INTERACTIVITY

document.addEventListener('DOMContentLoaded', () => {
  // Scroll to Top Button
  const scrollTopBtn = document.getElementById('scrollTopBtn');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      scrollTopBtn.style.display = 'block';
    } else {
      scrollTopBtn.style.display = 'none';
    }
  });
  scrollTopBtn && scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Animated Counters
  function animateCounter(counter) {
    const target = +counter.getAttribute('data-target');
    const duration = 1200;
    const start = 0;
    const step = Math.ceil(target / (duration / 16));
    let current = start;
    function update() {
      current += step;
      if (current >= target) {
        counter.textContent = target;
      } else {
        counter.textContent = current;
        requestAnimationFrame(update);
      }
    }
    update();
  }
  function handleCounters() {
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
      if (!counter.classList.contains('counted')) {
        const rect = counter.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
          animateCounter(counter);
          counter.classList.add('counted');
        }
      }
    });
  }
  window.addEventListener('scroll', handleCounters);
  handleCounters();

  // Newsletter Modal (show after 10s)
  setTimeout(() => {
    if (!localStorage.getItem('newsletter_shown')) {
      const modal = new bootstrap.Modal(document.getElementById('newsletterModal'));
      modal.show();
      localStorage.setItem('newsletter_shown', '1');
    }
  }, 10000);

  // Newsletter Form Validation
  const newsletterForm = document.getElementById('newsletterForm');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const email = document.getElementById('newsletterEmail').value;
      const success = document.getElementById('newsletterSuccess');
      if (/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
        success.classList.remove('d-none');
        newsletterForm.classList.add('d-none');
      } else {
        alert('Podaj poprawny adres e-mail!');
      }
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});
  
// Random Fact Section
const facts = [
  'Ładunki morskie stanowią ponad 80% światowego handlu!',
  'Pierwsza ciężarówka została wyprodukowana w 1896 roku przez Gottlieba Daimlera.',
  'Najdłuższy pociąg towarowy miał ponad 7 km długości!',
  'Transport lotniczy to najszybsza forma przewozu towarów na duże odległości.',
  'W logistyce coraz częściej wykorzystuje się roboty i sztuczną inteligencję.',
  'Ekologiczna spedycja to przyszłość branży transportowej.',
  'Największy port kontenerowy na świecie to Szanghaj w Chinach.',
  'W Polsce działa ponad 36 tysięcy firm transportowych.'
];
const randomFact = document.getElementById('randomFact');
const newFactBtn = document.getElementById('newFactBtn');
if (randomFact && newFactBtn) {
  let lastIdx = 0;
  newFactBtn.addEventListener('click', () => {
    let idx;
    do {
      idx = Math.floor(Math.random() * facts.length);
    } while (facts.length > 1 && idx === lastIdx);
    lastIdx = idx;
    randomFact.style.opacity = 0;
    randomFact.style.transform = 'scale(0.95)';
    newFactBtn.classList.add('animate__animated', 'animate__tada');
    setTimeout(() => {
      randomFact.textContent = facts[idx];
      randomFact.style.opacity = 1;
      randomFact.style.transform = 'scale(1)';
      newFactBtn.classList.remove('animate__animated', 'animate__tada');
    }, 300);
  });
}
// Force newsletter modal to show every time for demo
setTimeout(() => {
  const modal = new bootstrap.Modal(document.getElementById('newsletterModal'));
  modal.show();
}, 3000);
// Confetti on newsletter submit
function confetti() {
  for (let i = 0; i < 80; i++) {
    const conf = document.createElement('div');
    conf.className = 'confetti';
    conf.style.left = Math.random() * 100 + 'vw';
    conf.style.background = `hsl(${Math.random()*360},80%,60%)`;
    conf.style.animationDuration = (Math.random()*1+1.5) + 's';
    document.body.appendChild(conf);
    setTimeout(() => conf.remove(), 2000);
  }
}

// Floating notification system
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `floating-notification ${type}`;
  notification.innerHTML = `
    <div class="notification-content">
      <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
      <span>${message}</span>
    </div>
  `;
  
  document.body.appendChild(notification);
  
  // Animate in
  setTimeout(() => {
    notification.classList.add('show');
  }, 100);
  
  // Remove after 5 seconds
  setTimeout(() => {
    notification.classList.remove('show');
    setTimeout(() => {
      notification.remove();
    }, 300);
  }, 5000);
}

// Enhanced scroll animations
function animateOnScroll() {
  const elements = document.querySelectorAll('.animate-on-scroll');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animated');
      }
    });
  }, { threshold: 0.1 });
  
  elements.forEach(el => observer.observe(el));
}

// Initialize enhanced features
document.addEventListener('DOMContentLoaded', function() {
  animateOnScroll();
  
  // Show welcome notification
  setTimeout(() => {
    showNotification('Witamy w SpedycjaPro! 🚛', 'success');
  }, 2000);
});
if (newsletterForm) {
  newsletterForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const email = document.getElementById('newsletterEmail').value;
    const success = document.getElementById('newsletterSuccess');
    if (/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      success.classList.remove('d-none');
      newsletterForm.classList.add('d-none');
      confetti();
    } else {
      alert('Podaj poprawny adres e-mail!');
    }
  });
}
  
// Quiz o Spedycji
const quizQuestions = [
  {
    question: 'Jaki jest najczęściej wykorzystywany środek transportu w Polsce?',
    answer: 'Transport drogowy (ciężarówki)'
  },
  {
    question: 'Który port jest największym portem morskim w Polsce?',
    answer: 'Port Gdańsk'
  },
  {
    question: 'Ile wynosi maksymalna waga ładunku dla samochodu ciężarowego w UE?',
    answer: '40 ton'
  },
  {
    question: 'Która firma jest największym przewoźnikiem lotniczym cargo na świecie?',
    answer: 'FedEx'
  },
  {
    question: 'W którym roku powstała pierwsza linia kolejowa w Polsce?',
    answer: '1842 rok'
  },
  {
    question: 'Jaki procent światowego handlu odbywa się drogą morską?',
    answer: 'Ponad 80%'
  }
];

let currentQuizIndex = 0;
const showAnswerBtn = document.getElementById('showAnswerBtn');
const quizAnswer = document.getElementById('quizAnswer');
const quizQuestion = document.getElementById('quizQuestion');
const quizAnswerText = document.getElementById('quizAnswerText');
const nextQuestionBtn = document.getElementById('nextQuestionBtn');
const currentQuestionSpan = document.getElementById('currentQuestion');
const totalQuestionsSpan = document.getElementById('totalQuestions');
const quizProgress = document.getElementById('quizProgress');

if (showAnswerBtn && quizAnswer && quizQuestion && nextQuestionBtn) {
  // Initialize quiz
  totalQuestionsSpan.textContent = quizQuestions.length;
  updateQuizProgress();
  
  showAnswerBtn.addEventListener('click', () => {
    quizAnswer.style.display = 'block';
    showAnswerBtn.disabled = true;
    showAnswerBtn.innerHTML = '<i class="fas fa-check me-2"></i>Odpowiedź pokazana';
  });

  nextQuestionBtn.addEventListener('click', () => {
    currentQuizIndex = (currentQuizIndex + 1) % quizQuestions.length;
    updateQuiz();
  });

  function updateQuiz() {
    quizQuestion.textContent = quizQuestions[currentQuizIndex].question;
    quizAnswerText.textContent = quizQuestions[currentQuizIndex].answer;
    quizAnswer.style.display = 'none';
    showAnswerBtn.disabled = false;
    showAnswerBtn.innerHTML = '<i class="fas fa-eye me-2"></i>Pokaż odpowiedź';
    currentQuestionSpan.textContent = currentQuizIndex + 1;
    updateQuizProgress();
  }

  function updateQuizProgress() {
    const progress = ((currentQuizIndex + 1) / quizQuestions.length) * 100;
    quizProgress.style.width = progress + '%';
  }
}
// Galeria Lightbox
const galleryImgs = document.querySelectorAll('.gallery-img');
if (galleryImgs.length) {
  galleryImgs.forEach(img => {
    img.addEventListener('click', () => {
      const overlay = document.createElement('div');
      overlay.id = 'lightboxOverlay';
      const bigImg = document.createElement('img');
      bigImg.src = img.src;
      bigImg.alt = img.alt;
      overlay.appendChild(bigImg);
      document.body.appendChild(overlay);
      overlay.addEventListener('click', () => overlay.remove());
    });
  });
}
  