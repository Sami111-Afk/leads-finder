/* FLORSIMINTEX — generator pagini statice.
   O singură sursă de conținut + markup, 3 teme vizuale (industrial / clean / neon).
   Rulează:  node build.js   →  scrie index.html + industrial.html + clean.html + neon.html
   CSS/JS sunt fișiere separate, editabile manual (css/, js/). */

const fs = require('fs');
const path = require('path');

/* ----------------------------------------------------------------- DATE FIRMĂ */
const C = {
  brand: 'FLORSIMINTEX',
  legal: 'FLORSIMINTEX S.R.L.',
  tagline: 'Tractări · Vulcanizare · Utilaje · Spălătorie',
  city: 'Comarnic',
  county: 'jud. Prahova',
  address: 'Str. Republicii 1 Bis, Comarnic',
  cui: '1327508',
  tel: '0722 553 406',
  telRaw: '+40722553406',
  wa: '40722553406',
  fix: '0244 360 278',
  fixRaw: '+40244360278',
  maps: 'https://maps.app.goo.gl/q3RN5pKrEn8EoF1H6',
  mapsTractari: 'https://maps.app.goo.gl/4gYi3hnEfFh5eGaT8',
  areas: ['DN1', 'Comarnic', 'Posada', 'Sinaia', 'Breaza', 'Nistorești', 'Câmpina', 'Bănești'],
  waMsg: encodeURIComponent('Bună ziua! Am nevoie de ajutor — '),
};

/* ----------------------------------------------------------------- ICONIȚE SVG (line, stroke currentColor) */
const ico = {
  tow: '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M4 32h26V18h8l6 7v7h-4"/><path d="M30 18l-9-9-7 7"/><circle cx="13" cy="36" r="4"/><circle cx="38" cy="36" r="4"/><path d="M8 32V22h6"/></svg>',
  tire: '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="18"/><circle cx="24" cy="24" r="7"/><path d="M24 6v8M24 34v8M6 24h8M34 24h8M11 11l6 6M31 31l6 6M37 11l-6 6M17 31l-6 6"/></svg>',
  crane: '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M6 40h22V28h7l5 6v6h-3"/><path d="M14 28V14h5l16 5"/><path d="M19 14l9-6"/><circle cx="13" cy="44" r="3"/><circle cx="34" cy="44" r="3"/></svg>',
  excavator: '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M4 40h24v-9H8a4 4 0 0 0-4 4z"/><path d="M28 31v-7l9-10 4 3-7 9"/><path d="M38 24l5 6-4 6h-6"/><path d="M4 36h24"/></svg>',
  wash: '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 6c-6 8-10 13-10 18a10 10 0 0 0 20 0c0-5-4-10-10-18z"/><path d="M20 28a4 4 0 0 0 4 4"/></svg>',
  atv: '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="11" cy="34" r="6"/><circle cx="37" cy="34" r="6"/><path d="M11 34h14l4-10h8M17 24l4-6h8l3 6"/><path d="M29 24l-4 10"/></svg>',
  clock: '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="18"/><path d="M24 13v11l8 5"/></svg>',
  pin: '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 44s14-12 14-24a14 14 0 1 0-28 0c0 12 14 24 14 24z"/><circle cx="24" cy="20" r="5"/></svg>',
  phone: '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M14 6l6 1 2 9-5 4a24 24 0 0 0 11 11l4-5 9 2 1 6a4 4 0 0 1-4 4A34 34 0 0 1 10 10a4 4 0 0 1 4-4z"/></svg>',
  bolt: '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M26 4 10 28h10l-2 16 18-26H26z"/></svg>',
  shield: '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 4l16 6v12c0 11-7 17-16 22-9-5-16-11-16-22V10z"/><path d="M17 24l5 5 9-11"/></svg>',
  wa: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11 19.6L3 29l6.6-2a13 13 0 1 0 6.4-24zm0 23.6a10.6 10.6 0 0 1-5.4-1.5l-.4-.2-4 1 1-3.9-.3-.4A10.6 10.6 0 1 1 16 26.6zm6-7.9c-.3-.2-2-1-2.3-1.1-.3-.1-.5-.2-.8.2s-.9 1.1-1.1 1.3-.4.2-.8 0a8.6 8.6 0 0 1-4.3-3.7c-.3-.6.3-.5.9-1.8.1-.2 0-.4 0-.6s-.8-1.9-1-2.6c-.3-.7-.6-.6-.8-.6h-.7a1.3 1.3 0 0 0-1 .4 4 4 0 0 0-1.2 2.9 6.9 6.9 0 0 0 1.4 3.6 15.7 15.7 0 0 0 6 5.3c2.2 1 3 1 4.1.9a3.5 3.5 0 0 0 2.3-1.6 2.9 2.9 0 0 0 .2-1.6c0-.2-.3-.3-.6-.5z"/></svg>',
  arrow: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
  star: '<svg viewBox="0 0 24 24" class="star" aria-hidden="true"><path d="M12 2l3 6.5 7 .8-5.2 4.7L18.5 22 12 18.3 5.5 22l1.7-8L2 9.3l7-.8z"/></svg>',
  check: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 13l4 4 10-12"/></svg>',
};

/* ----------------------------------------------------------------- SERVICII */
const services = [
  { ico: 'tow', tag: 'NON-STOP 24/7', t: 'Tractări & asistență rutieră', d: 'Intervenim non-stop pe DN1 și Valea Prahovei. Autoplatforme moderne, trolii electrice și hidraulice pentru orice situație — pană, accident sau defecțiune.', img: 'asistenta-rutiera.jpg' },
  { ico: 'tire', tag: 'Luni–Sâm 08–18', t: 'Vulcanizare auto', d: 'Anvelope autoturisme, camioane și utilaje. Dejantare, echilibrare și service roți, rapid și corect. Reparăm și pe loc dacă te-a prins pana în drum.', img: 'vulcanizare-atelier.jpg' },
  { ico: 'crane', tag: 'Agabaritic', t: 'Transport utilaje & agabaritic', d: 'Mutăm excavatoare, buldoexcavatoare, tractoare și utilaje grele cu trailer dedicat. Transport mașini noi sau avariate, dube, remorci, bărci și rulote.', img: 'transport-utilaje.jpg' },
  { ico: 'excavator', tag: 'Cu sau fără operator', t: 'Închiriere utilaje', d: 'Excavatoare și utilaje de construcții disponibile pentru închiriere în zona Comarnic. Punem la dispoziție și transportul la punctul de lucru.', img: 'inchiriere-utilaje.jpg' },
  { ico: 'wash', tag: 'Interior & exterior', t: 'Spălătorie auto', d: 'Spălare completă pentru autoturisme și SUV-uri, exterior și interior. Mașina ta arată ca nouă cât rezolvi restul treburilor.', img: '' },
  { ico: 'atv', tag: 'ATV · Moto', t: 'Transport ATV & moto', d: 'Transportăm în siguranță ATV-uri, motociclete și jet-ski. Tot de aici poți închiria ATV-uri pentru ture pe munte.', img: '' },
];

const whyUs = [
  ['bolt', 'Ajungem repede', 'Echipe permanente în zonă, pe DN1. Suni, spui unde ești, plecăm spre tine.'],
  ['shield', 'Autoplatforme moderne', 'Mașina ta urcă pe platformă, nu e trasă pe asfalt. Trolii electrice, hidraulice și manuale.'],
  ['clock', 'Non-stop, chiar și noaptea', 'Asistența rutieră nu se închide. Suntem la telefon 24/7, inclusiv în weekend și de sărbători.'],
  ['check', 'O firmă, toate serviciile', 'De la tractare la vulcanizare, utilaje și spălătorie — rezolvi totul într-un singur loc, cu oameni pe care îi cunoști.'],
];

const stats = [
  ['24/7', 'asistență rutieră non-stop'],
  ['8', 'localități acoperite pe DN1'],
  ['12+', 'oameni în echipă'],
  ['100%', 'autoplatforme moderne'],
];

const reviews = [
  { n: 'Radu Coman', meta: 'Local Guide · Google', s: 5, t: 'Servicii rapide și de calitate. Recomand cu încredere.' },
  { n: 'Mihaela Nedelcu', meta: 'Google', s: 5, t: 'Oameni serioși, te ajută imediat. Mulțumesc!' },
  { n: 'Noemi Moise', meta: 'Google', s: 5, t: 'Au venit repede și au rezolvat fără bătăi de cap. Profesioniști.' },
];

/* ----------------------------------------------------------------- HELPERE */
const waLink = (txt) => `https://wa.me/${C.wa}?text=${txt || C.waMsg}`;
const stars = (n) => Array.from({ length: 5 }, (_, i) => ico.star.replace('class="star"', `class="star${i < n ? '' : ' off'}"`)).join('');

/* ----------------------------------------------------------------- MARKUP (comun tuturor temelor) */
function body() {
  return `
<a class="skip" href="#main">Sari la conținut</a>

<header class="site-head" id="top">
  <div class="wrap head-inner">
    <a class="brand" href="#top" aria-label="${C.brand} — acasă">
      <span class="brand-mark">${ico.tow}</span>
      <span class="brand-txt"><b>${C.brand}</b><i>${C.city} · DN1</i></span>
    </a>
    <nav class="nav" aria-label="Principal">
      <a href="#servicii">Servicii</a>
      <a href="#dece">De ce noi</a>
      <a href="#acoperire">Acoperire</a>
      <a href="#recenzii">Recenzii</a>
      <a href="#contact">Contact</a>
    </nav>
    <div class="head-cta">
      <a class="btn btn-ghost" href="tel:${C.telRaw}">${ico.phone}<span>${C.tel}</span></a>
      <button class="burger" aria-label="Meniu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div class="chevron-bar" aria-hidden="true"></div>
</header>

<main id="main">

  <!-- HERO -->
  <section class="hero">
    <div class="hero-media"><img src="assets/images/hero-tractare.jpg" alt="Autospeciala FLORSIMINTEX tractând un autoturism pe DN1" width="1600" height="1200" fetchpriority="high"></div>
    <div class="hero-overlay"></div>
    <div class="wrap hero-inner">
      <p class="eyebrow reveal"><span class="ping"></span> Non-stop pe DN1 · Valea Prahovei</p>
      <h1 class="reveal">Ai rămas în pană<br>pe drum? <em>Te scoatem noi.</em></h1>
      <p class="lead reveal">Tractări și asistență rutieră 24/7 în ${C.city} și pe toată Valea Prahovei. Plus vulcanizare, transport utilaje și spălătorie — toate la aceeași echipă.</p>
      <div class="hero-actions reveal">
        <a class="btn btn-call" href="tel:${C.telRaw}">${ico.phone}<span>Sună acum · ${C.tel}</span></a>
        <a class="btn btn-wa" href="${waLink()}" target="_blank" rel="noopener">${ico.wa}<span>Scrie pe WhatsApp</span></a>
      </div>
      <ul class="hero-chips reveal">
        <li>${ico.check} Ajungem rapid</li>
        <li>${ico.check} Autoplatforme moderne</li>
        <li>${ico.check} Plata pe loc / card</li>
      </ul>
    </div>
  </section>

  <!-- TICKER ZONE -->
  <div class="ticker" aria-label="Zone acoperite">
    <div class="ticker-track">
      ${C.areas.concat(C.areas, C.areas).map(a => `<span>${ico.pin}${a}</span>`).join('')}
    </div>
  </div>

  <!-- STATS -->
  <section class="stats wrap">
    ${stats.map(([n, l]) => `<div class="stat reveal"><b data-count="${n}">${n}</b><span>${l}</span></div>`).join('')}
  </section>

  <!-- SERVICII -->
  <section class="section" id="servicii">
    <div class="wrap">
      <header class="sec-head reveal">
        <p class="kicker">Ce facem</p>
        <h2>Servicii pentru drum, atelier și șantier</h2>
        <p class="sub">O singură firmă din ${C.city} care îți rezolvă mașina, anvelopele și utilajele. Suni, te ajutăm.</p>
      </header>
      <div class="services">
        ${services.map((s, i) => `
        <article class="card reveal${s.img ? ' has-img' : ''}" style="--i:${i}">
          ${s.img ? `<div class="card-media"><img src="assets/images/${s.img}" alt="${s.t} — FLORSIMINTEX ${C.city}" width="1400" height="1050" loading="lazy"></div>` : ''}
          <div class="card-body">
            <span class="card-ico">${ico[s.ico]}</span>
            <span class="card-tag">${s.tag}</span>
            <h3>${s.t}</h3>
            <p>${s.d}</p>
            <a class="card-link" href="${waLink(encodeURIComponent('Bună ziua! Vreau detalii despre: ' + s.t))}" target="_blank" rel="noopener">Cere o ofertă ${ico.arrow}</a>
          </div>
        </article>`).join('')}
      </div>
    </div>
  </section>

  <!-- DE CE NOI -->
  <section class="section section-alt" id="dece">
    <div class="wrap feature">
      <div class="feature-media reveal">
        <img src="assets/images/asistenta-rutiera.jpg" alt="Platformă de asistență rutieră non-stop FLORSIMINTEX" width="1000" height="1333" loading="lazy">
        <div class="feature-badge">${ico.clock}<div><b>NON-STOP</b><span>și de sărbători</span></div></div>
      </div>
      <div class="feature-text">
        <p class="kicker reveal">De ce FLORSIMINTEX</p>
        <h2 class="reveal">Pe noi ne găsești când chiar ai nevoie</h2>
        <ul class="why">
          ${whyUs.map(([k, t, d]) => `<li class="reveal"><span class="why-ico">${ico[k]}</span><div><b>${t}</b><p>${d}</p></div></li>`).join('')}
        </ul>
        <a class="btn btn-call reveal" href="tel:${C.telRaw}">${ico.phone}<span>${C.tel}</span></a>
      </div>
    </div>
  </section>

  <!-- ACOPERIRE -->
  <section class="section" id="acoperire">
    <div class="wrap">
      <header class="sec-head reveal">
        <p class="kicker">Unde ajungem</p>
        <h2>Acoperim toată Valea Prahovei</h2>
        <p class="sub">Echipe permanente pe DN1, gata de plecare. Dacă ești în zonă, suntem la tine în cel mai scurt timp.</p>
      </header>
      <div class="areas reveal">
        ${C.areas.map(a => `<span class="area-pill">${ico.pin}${a}</span>`).join('')}
      </div>
      <div class="map-cta reveal">
        <div>
          <b>${C.address}</b>
          <span>${C.city}, ${C.county}</span>
        </div>
        <a class="btn btn-ghost" href="${C.maps}" target="_blank" rel="noopener">${ico.pin}<span>Deschide în Google Maps</span></a>
      </div>
    </div>
  </section>

  <!-- RECENZII -->
  <section class="section section-alt" id="recenzii">
    <div class="wrap">
      <header class="sec-head reveal">
        <p class="kicker">Ce spun clienții</p>
        <h2>Oameni pe care i-am scos din drum</h2>
        <div class="rating-line reveal"><span class="stars">${stars(5)}</span> <b>5,0</b> pe Google pentru asistență rutieră</div>
      </header>
      <div class="reviews">
        ${reviews.map(r => `
        <figure class="review reveal">
          <span class="stars">${stars(r.s)}</span>
          <blockquote>${r.t}</blockquote>
          <figcaption><span class="avatar">${r.n[0]}</span><span><b>${r.n}</b><i>${r.meta}</i></span></figcaption>
        </figure>`).join('')}
      </div>
    </div>
  </section>

  <!-- CONTACT / CTA -->
  <section class="section contact" id="contact">
    <div class="wrap contact-inner">
      <div class="contact-text">
        <p class="kicker reveal">Contact</p>
        <h2 class="reveal">Sună-ne. Restul rezolvăm noi.</h2>
        <p class="sub reveal">Asistență rutieră non-stop. Pentru vulcanizare, utilaje sau spălătorie, dă-ne un semn pe WhatsApp.</p>
        <div class="contact-actions reveal">
          <a class="btn btn-call" href="tel:${C.telRaw}">${ico.phone}<span>${C.tel}</span></a>
          <a class="btn btn-wa" href="${waLink()}" target="_blank" rel="noopener">${ico.wa}<span>WhatsApp</span></a>
        </div>
        <ul class="contact-list reveal">
          <li>${ico.pin}<span>${C.address}, ${C.county}</span></li>
          <li>${ico.phone}<span>${C.tel} · ${C.fix}</span></li>
        </ul>
      </div>
      <div class="hours reveal">
        <h3>Program</h3>
        <table>
          <tr><td>Tractări & asistență rutieră</td><td class="hl">NON-STOP</td></tr>
          <tr><td>Închiriere & transport utilaje</td><td class="hl">NON-STOP</td></tr>
          <tr><td>Vulcanizare</td><td>Luni–Sâmbătă · 08–18</td></tr>
          <tr><td>Spălătorie auto</td><td>Luni–Sâmbătă · 08–18</td></tr>
        </table>
        <p class="hours-note">${ico.clock} Pe drum, la orice oră — asistența rutieră răspunde mereu.</p>
      </div>
    </div>
  </section>
</main>

<footer class="site-foot">
  <div class="wrap foot-inner">
    <div class="foot-brand">
      <span class="brand-mark">${ico.tow}</span>
      <div><b>${C.brand}</b><span>${C.tagline} · ${C.city}</span></div>
    </div>
    <nav class="foot-nav" aria-label="Footer">
      <a href="#servicii">Servicii</a><a href="#acoperire">Acoperire</a><a href="#recenzii">Recenzii</a><a href="#contact">Contact</a>
    </nav>
    <p class="foot-legal">© <span id="y"></span> ${C.legal} · CUI ${C.cui} · ${C.address}, ${C.county}<br>Tractări · Vulcanizare · Închiriere utilaje · Spălătorie auto — non-stop pe DN1.</p>
  </div>
</footer>

<!-- BUTOANE FLOTANTE -->
<div class="dock">
  <a class="dock-btn dock-call" href="tel:${C.telRaw}" aria-label="Sună acum">${ico.phone}</a>
  <a class="dock-btn dock-wa" href="${waLink()}" target="_blank" rel="noopener" aria-label="Scrie pe WhatsApp">${ico.wa}</a>
</div>
`;
}

/* ----------------------------------------------------------------- ȘABLON PAGINĂ */
function page(theme) {
  const title = `${C.brand} ${C.city} — Tractări non-stop, Vulcanizare, Utilaje & Spălătorie`;
  const desc = `Tractări auto și asistență rutieră non-stop pe DN1 și Valea Prahovei. Vulcanizare, transport și închiriere utilaje, spălătorie auto în ${C.city}, Prahova. Sună ${C.tel}.`;
  return `<!doctype html>
<html lang="ro" class="theme-${theme}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<meta name="description" content="${desc}">
<meta name="theme-color" content="#0d0f12">
<meta property="og:title" content="${title}">
<meta property="og:description" content="${desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/images/hero-tractare.jpg">
<link rel="preload" as="image" href="assets/images/hero-tractare.jpg" fetchpriority="high">
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="css/components.css">
<link rel="stylesheet" href="css/theme-${theme}.css">
<script type="application/ld+json">${JSON.stringify({
    '@context': 'https://schema.org', '@type': 'AutoRepair', name: C.legal,
    image: 'assets/images/hero-tractare.jpg', telephone: C.telRaw,
    address: { '@type': 'PostalAddress', streetAddress: 'Str. Republicii 1 Bis', addressLocality: C.city, addressRegion: 'Prahova', addressCountry: 'RO' },
    areaServed: C.areas, openingHours: 'Mo-Su 00:00-24:00',
    makesOffer: services.map(s => ({ '@type': 'Offer', name: s.t })),
    aggregateRating: { '@type': 'AggregateRating', ratingValue: '5.0', reviewCount: '3' }
  })}</script>
</head>
<body>
${body()}
<script src="js/app.js" defer></script>
</body>
</html>`;
}

/* ----------------------------------------------------------------- SELECTOR (index.html) */
function chooser() {
  const variants = [
    ['industrial', 'Industrial / Garaj', 'Asfalt închis, roșu & alb cu chevroni hazard. Rugged, autentic — exact ca pe autospecialele lor.'],
    ['clean', 'Modern / Clean', 'Luminos, mult spațiu, fotografii mari. Curat și de încredere.'],
    ['neon', 'Dark / Neon', 'Negru profund cu accente luminoase. Modern, tech, cu glow subtil.'],
  ];
  return `<!doctype html>
<html lang="ro" class="theme-industrial">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>FLORSIMINTEX — alege varianta de design</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="css/theme-industrial.css">
<style>
  body{display:grid;place-items:center;min-height:100vh;padding:40px 20px}
  .pick{max-width:980px;width:100%}
  .pick h1{font-family:var(--font-display);font-size:clamp(2.4rem,7vw,4.5rem);line-height:.95;letter-spacing:.01em;margin:0 0 .2em}
  .pick .sub{color:var(--muted);max-width:54ch;margin:0 0 2.4rem;font-size:1.05rem}
  .pick-grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
  .pick-card{display:block;padding:26px;border:1px solid var(--line);border-radius:var(--r);background:var(--surface);text-decoration:none;color:inherit;transition:.25s}
  .pick-card:hover{transform:translateY(-6px);border-color:var(--accent);box-shadow:0 20px 50px rgba(0,0,0,.4)}
  .pick-card b{font-family:var(--font-display);font-size:1.5rem;display:block;margin-bottom:.4rem;letter-spacing:.02em}
  .pick-card span{color:var(--muted);font-size:.95rem;line-height:1.5}
  .pick-card .go{margin-top:1.2rem;display:inline-flex;gap:.4rem;align-items:center;color:var(--accent);font-weight:700}
  .pick-card .go svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2.4}
  .pick-note{margin-top:2rem;color:var(--muted);font-size:.85rem}
</style>
</head>
<body>
<div class="pick">
  <p class="kicker">FLORSIMINTEX · ${C.city}</p>
  <h1>Alege varianta<br>care îți place</h1>
  <p class="sub">Același conținut, trei atmosfere diferite. Deschide-le și spune-mi care merge mai departe — pe aceea o finisăm și o punem live.</p>
  <div class="pick-grid">
    ${variants.map(([k, t, d]) => `<a class="pick-card" href="${k}.html"><b>${t}</b><span>${d}</span><span class="go">Vezi varianta ${ico.arrow}</span></a>`).join('')}
  </div>
  <p class="pick-note">Date reale din profilurile Google · poze reale ale firmei · ${C.tel}</p>
</div>
</body>
</html>`;
}

/* ----------------------------------------------------------------- SCRIE FIȘIERE */
const out = (f, c) => { fs.writeFileSync(path.join(__dirname, f), c); console.log('✓', f, (c.length / 1024).toFixed(1) + 'kb'); };
['industrial', 'clean', 'neon'].forEach(t => out(`${t}.html`, page(t)));
out('index.html', chooser());
console.log('Build gata.');
