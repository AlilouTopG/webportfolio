// OLED Cyberpunk — Interactions
const nav = document.getElementById('nav');
const toggle = document.getElementById('navToggle');
const links = document.getElementById('navLinks');

toggle?.addEventListener('click', () => links.classList.toggle('open'));
document.querySelectorAll('.nav-link').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));

// Sticky nav shadow
let lastY = 0;
window.addEventListener('scroll', () => {
  const y = window.scrollY;
  nav.style.background = y > 12 ? 'rgba(10,10,10,0.85)' : 'rgba(10,10,10,0.65)';
  nav.style.borderBottomColor = y > 12 ? 'rgba(0,229,255,0.14)' : 'rgba(255,255,255,0.08)';
  lastY = y;
}, { passive: true });

// Reveal on scroll
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('in'); });
}, { threshold: 0.12 });

document.querySelectorAll('.section, .project-card, .about-card, .stack-card, .contact-card').forEach(el => {
  el.classList.add('reveal');
  io.observe(el);
});

// Smooth parallax for glows
window.addEventListener('mousemove', (e) => {
  const x = (e.clientX / window.innerWidth - 0.5) * 20;
  const y = (e.clientY / window.innerHeight - 0.5) * 20;
  document.querySelectorAll('.bg-glow').forEach((glow, i) => {
    const factor = i === 0 ? 1 : -0.6;
    glow.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
  });
});

// Contact form demo
function handleContact(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button[type="submit"]');
  const orig = btn.textContent;
  btn.textContent = '✓ Transmission Queued — Check Email';
  btn.style.background = '#00E5FF';
  btn.style.color = '#001114';
  setTimeout(() => {
    btn.textContent = orig;
    btn.style.background = '';
    btn.style.color = '';
    e.target.reset();
  }, 2600);
  return false;
}
window.handleContact = handleContact;

// Konami: cyan flash
let seq = [];
const konami = ['ArrowUp','ArrowUp','ArrowDown','ArrowDown','ArrowLeft','ArrowRight','ArrowLeft','ArrowRight'];
window.addEventListener('keydown', (e) => {
  seq.push(e.key);
  seq = seq.slice(-8);
  if (seq.join(',') === konami.join(',')) {
    document.body.style.transition = 'box-shadow .4s';
    document.body.style.boxShadow = 'inset 0 0 120px rgba(0,229,255,0.2)';
    setTimeout(() => document.body.style.boxShadow = '', 1200);
  }
});
