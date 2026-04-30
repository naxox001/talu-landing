/* ============================================================
   TÄLU · PREMIUM FX
   GSAP-powered animations: magnetic buttons, ripple, letter stagger,
   counter, parallax, scroll reveals.
   Carga GSAP + Lucide vía CDN. Aplica a CUALQUIER página landing.
   ============================================================ */

(function() {
  'use strict';

  // ============ Helper: load script ============
  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = src;
      s.async = true;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  async function bootstrap() {
    // Cargar Lucide + GSAP en paralelo
    await Promise.all([
      loadScript('https://unpkg.com/lucide@latest/dist/umd/lucide.js'),
      loadScript('https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js'),
    ]);
    // ScrollTrigger plugin
    await loadScript('https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js');

    if (window.gsap && window.ScrollTrigger) {
      gsap.registerPlugin(ScrollTrigger);
    }
    if (window.lucide) {
      lucide.createIcons();
    }

    initButtons();
    initLetterReveal();
    initCounters();
    initParallax();
    initSealEntrance();
    initRippleEffect();
    initMagneticButtons();
  }

  // ============ Magnetic Buttons (cursor follow) ============
  function initMagneticButtons() {
    if (!window.gsap) return;
    document.querySelectorAll('.btn-primary, .btn-secondary, [data-magnetic]').forEach(btn => {
      const strength = parseFloat(btn.dataset.magnetic) || 0.35;
      btn.addEventListener('mousemove', e => {
        const r = btn.getBoundingClientRect();
        const x = e.clientX - r.left - r.width / 2;
        const y = e.clientY - r.top - r.height / 2;
        gsap.to(btn, {
          x: x * strength,
          y: y * strength,
          duration: 0.4,
          ease: 'power2.out'
        });
      });
      btn.addEventListener('mouseleave', () => {
        gsap.to(btn, { x: 0, y: 0, duration: 0.6, ease: 'elastic.out(1, 0.4)' });
      });
    });
  }

  // ============ Ripple effect on click ============
  function initRippleEffect() {
    document.querySelectorAll('.btn-primary, .btn-secondary, .v-pill, .amount-pill').forEach(btn => {
      btn.style.position = btn.style.position || 'relative';
      btn.style.overflow = 'hidden';
      btn.addEventListener('click', e => {
        const ripple = document.createElement('span');
        ripple.className = 'ripple-fx';
        const r = btn.getBoundingClientRect();
        const size = Math.max(r.width, r.height) * 1.5;
        ripple.style.cssText = `
          position: absolute;
          left: ${e.clientX - r.left - size/2}px;
          top: ${e.clientY - r.top - size/2}px;
          width: ${size}px;
          height: ${size}px;
          border-radius: 999px;
          background: radial-gradient(circle, rgba(255,255,255,.55), transparent 70%);
          pointer-events: none;
          transform: scale(0);
          animation: ripple-expand .7s ease-out;
          z-index: 10;
        `;
        btn.appendChild(ripple);
        setTimeout(() => ripple.remove(), 700);
      });
    });
  }

  // ============ Letter-by-letter reveal en H1 hero ============
  function initLetterReveal() {
    if (!window.gsap) return;
    document.querySelectorAll('.hero-text h1, .hero-ternero h1, .contact-wrap h1').forEach(h1 => {
      // Solo si no tiene <em> dentro (evitar romper estructura) → split por letras conservando spans
      const original = h1.innerHTML;
      // Si tiene em, preservarlo
      const hasEm = h1.querySelector('em');
      if (hasEm) {
        // Splitear texto principal y em por separado
        const text = h1.childNodes[0]?.textContent?.trim() || '';
        const emText = hasEm.textContent.trim();
        if (text) {
          h1.innerHTML = wrapChars(text) + '<em class="hero-em">' + wrapChars(emText) + '</em>';
        }
      } else {
        h1.innerHTML = wrapChars(h1.textContent.trim());
      }

      const chars = h1.querySelectorAll('.char');
      gsap.from(chars, {
        opacity: 0,
        y: 28,
        rotateX: -45,
        filter: 'blur(8px)',
        stagger: 0.025,
        duration: 0.9,
        ease: 'power3.out',
        delay: 0.2,
      });
    });
  }

  function wrapChars(text) {
    return text.split('').map(c => {
      if (c === ' ') return '<span class="char">&nbsp;</span>';
      return `<span class="char">${c}</span>`;
    }).join('');
  }

  // ============ Counter animation en precios ============
  function initCounters() {
    if (!window.gsap || !window.ScrollTrigger) return;
    document.querySelectorAll('[data-counter], .price-now, .gc-amount-display').forEach(el => {
      const text = el.textContent;
      const match = text.match(/[\d.]+/);
      if (!match) return;
      const finalValue = parseFloat(match[0].replace(/\./g, ''));
      if (!finalValue || finalValue < 100) return;

      const prefix = text.split(match[0])[0];
      const suffix = text.split(match[0])[1] || '';
      const obj = { v: 0 };

      ScrollTrigger.create({
        trigger: el,
        start: 'top 85%',
        once: true,
        onEnter: () => {
          gsap.to(obj, {
            v: finalValue,
            duration: 1.6,
            ease: 'power2.out',
            onUpdate: () => {
              el.textContent = prefix + Math.round(obj.v).toLocaleString('es-CL') + suffix;
            }
          });
        }
      });
    });
  }

  // ============ Parallax sutil en hero product / imágenes ============
  function initParallax() {
    if (!window.gsap || !window.ScrollTrigger) return;
    document.querySelectorAll('.hero-product-frame img, .hero-img-wrap img, .hero-bottles-frame img').forEach(img => {
      gsap.to(img, {
        yPercent: -10,
        ease: 'none',
        scrollTrigger: {
          trigger: img,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true,
        }
      });
    });
  }

  // ============ Sello entrance (selladura dramática) ============
  function initSealEntrance() {
    if (!window.gsap) return;
    document.querySelectorAll('.hero-seal, .hero-seal-massive, .seal-center').forEach(seal => {
      gsap.from(seal, {
        scale: 0,
        rotation: -180,
        opacity: 0,
        duration: 1.2,
        ease: 'back.out(1.4)',
        delay: 0.4,
      });
    });
  }

  // ============ Buttons - glow pulse idle (CSS-driven, JS solo enhance) ============
  function initButtons() {
    document.querySelectorAll('.btn-primary').forEach(btn => {
      btn.classList.add('btn-fx');
    });
  }

  // Boot when DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootstrap);
  } else {
    bootstrap();
  }

  // Re-render Lucide icons after dynamic content
  window.taluRefreshIcons = function() {
    if (window.lucide) lucide.createIcons();
  };
})();
