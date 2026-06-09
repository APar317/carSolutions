import http.server
import socketserver
import os
import mimetypes

PORT = 8005

ABOUT_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>About Us – Car Solution | Premium Automotive Care</title>
  <meta name="description" content="Meet Nirmal Hans and the Car Solution team. 7+ years of automotive expertise with trained mechanical & electrical engineers." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <style>
    :root {
      --bg-base: #030712;
      --bg-surface: #0b0f19;
      --bg-card: rgba(15, 23, 42, 0.6);
      --border-glass: rgba(255, 255, 255, 0.08);
      --color-primary: #0ea5e9;
      --color-primary-glow: rgba(14, 165, 233, 0.25);
      --color-secondary: #6366f1;
      --color-accent: #f59e0b;
      --gradient-primary: linear-gradient(135deg, #0ea5e9, #6366f1);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --font-display: 'Outfit', sans-serif;
      --font-body: 'Inter', sans-serif;
      --radius: 16px;
      --shadow-card: 0 8px 32px rgba(0,0,0,0.3);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      background: var(--bg-base);
      color: var(--text-main);
      font-family: var(--font-body);
      line-height: 1.7;
      overflow-x: hidden;
    }

    .nav {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      z-index: 100;
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      background: rgba(3, 7, 18, 0.8);
      border-bottom: 1px solid var(--border-glass);
      padding: 16px 0;
      transition: background 0.3s;
    }
    .nav-inner {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .nav-logo {
      font-family: var(--font-display);
      font-size: 1.5rem;
      font-weight: 700;
      background: var(--gradient-primary);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-decoration: none;
    }
    .nav-links { display: flex; gap: 32px; list-style: none; }
    .nav-links a {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.95rem;
      font-weight: 500;
      transition: color 0.3s;
      position: relative;
    }
    .nav-links a:hover, .nav-links a.active {
      color: var(--color-primary);
    }
    .nav-links a.active::after {
      content: '';
      position: absolute;
      bottom: -6px;
      left: 0;
      right: 0;
      height: 2px;
      background: var(--gradient-primary);
      border-radius: 2px;
    }

    .hero {
      position: relative;
      padding: 160px 24px 100px;
      text-align: center;
      overflow: hidden;
    }
    .hero::before {
      content: '';
      position: absolute;
      top: -200px;
      left: 50%;
      transform: translateX(-50%);
      width: 800px;
      height: 800px;
      background: radial-gradient(circle, rgba(14,165,233,0.12) 0%, rgba(99,102,241,0.06) 40%, transparent 70%);
      pointer-events: none;
    }
    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 20px;
      background: rgba(14, 165, 233, 0.1);
      border: 1px solid rgba(14, 165, 233, 0.2);
      border-radius: 100px;
      font-size: 0.85rem;
      color: var(--color-primary);
      font-weight: 500;
      margin-bottom: 24px;
      animation: fadeInDown 0.8s ease-out;
    }
    .hero-badge .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--color-primary);
      animation: pulse 2s infinite;
    }
    .hero h1 {
      font-family: var(--font-display);
      font-size: clamp(2.5rem, 5vw, 4rem);
      font-weight: 800;
      line-height: 1.15;
      margin-bottom: 20px;
      animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    .hero h1 span {
      background: var(--gradient-primary);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero-sub {
      color: var(--text-muted);
      font-size: 1.2rem;
      max-width: 600px;
      margin: 0 auto;
      animation: fadeInUp 0.8s ease-out 0.4s both;
    }

    .founder-section {
      max-width: 1200px;
      margin: 0 auto;
      padding: 80px 24px;
    }
    .founder-card {
      display: grid;
      grid-template-columns: 1fr 1.4fr;
      gap: 60px;
      align-items: center;
      background: var(--bg-card);
      border: 1px solid var(--border-glass);
      border-radius: var(--radius);
      padding: 48px;
      backdrop-filter: blur(12px);
      box-shadow: var(--shadow-card);
      animation: fadeInUp 0.8s ease-out 0.6s both;
    }
    .founder-photo-wrapper {
      position: relative;
    }
    .founder-photo-wrapper::before {
      content: '';
      position: absolute;
      inset: -4px;
      background: var(--gradient-primary);
      border-radius: 20px;
      opacity: 0.6;
      z-index: 0;
      filter: blur(8px);
    }
    .founder-photo {
      position: relative;
      z-index: 1;
      width: 100%;
      aspect-ratio: 3/4;
      object-fit: cover;
      border-radius: 16px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    }
    .founder-info { position: relative; }
    .founder-name {
      font-family: var(--font-display);
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 4px;
    }
    .founder-title {
      color: var(--color-primary);
      font-size: 1rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 24px;
    }
    .founder-bio {
      color: var(--text-muted);
      font-size: 1.05rem;
      margin-bottom: 16px;
    }
    .founder-stats {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-top: 32px;
      padding-top: 32px;
      border-top: 1px solid var(--border-glass);
    }
    .stat { text-align: center; }
    .stat-value {
      font-family: var(--font-display);
      font-size: 2rem;
      font-weight: 700;
      background: var(--gradient-primary);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .stat-label {
      color: var(--text-dim);
      font-size: 0.85rem;
      margin-top: 4px;
    }

    .why-section {
      max-width: 1200px;
      margin: 0 auto;
      padding: 80px 24px 100px;
    }
    .section-header {
      text-align: center;
      margin-bottom: 60px;
    }
    .section-header h2 {
      font-family: var(--font-display);
      font-size: clamp(2rem, 4vw, 3rem);
      font-weight: 700;
      margin-bottom: 16px;
    }
    .section-header h2 span {
      background: var(--gradient-primary);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .section-header p {
      color: var(--text-muted);
      font-size: 1.1rem;
      max-width: 600px;
      margin: 0 auto;
    }

    .why-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 24px;
    }
    .why-card {
      background: var(--bg-card);
      border: 1px solid var(--border-glass);
      border-radius: var(--radius);
      padding: 36px 32px;
      transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s, border-color 0.4s;
      position: relative;
      overflow: hidden;
    }
    .why-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: var(--gradient-primary);
      opacity: 0;
      transition: opacity 0.4s;
    }
    .why-card:hover {
      transform: translateY(-6px);
      box-shadow: 0 20px 40px rgba(14, 165, 233, 0.1);
      border-color: rgba(14, 165, 233, 0.2);
    }
    .why-card:hover::before { opacity: 1; }
    .why-icon {
      width: 56px;
      height: 56px;
      border-radius: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      margin-bottom: 20px;
      background: rgba(14, 165, 233, 0.1);
      border: 1px solid rgba(14, 165, 233, 0.15);
    }
    .why-card:nth-child(2) .why-icon { background: rgba(99, 102, 241, 0.1); border-color: rgba(99, 102, 241, 0.15); }
    .why-card:nth-child(3) .why-icon { background: rgba(245, 158, 11, 0.1); border-color: rgba(245, 158, 11, 0.15); }
    .why-card:nth-child(4) .why-icon { background: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.15); }
    .why-card:nth-child(5) .why-icon { background: rgba(236, 72, 153, 0.1); border-color: rgba(236, 72, 153, 0.15); }
    .why-card:nth-child(6) .why-icon { background: rgba(168, 85, 247, 0.1); border-color: rgba(168, 85, 247, 0.15); }
    .why-card h3 {
      font-family: var(--font-display);
      font-size: 1.25rem;
      font-weight: 600;
      margin-bottom: 10px;
    }
    .why-card p {
      color: var(--text-muted);
      font-size: 0.95rem;
      line-height: 1.7;
    }

    .team-section {
      background: linear-gradient(180deg, transparent 0%, rgba(14,165,233,0.04) 50%, transparent 100%);
      padding: 100px 24px;
    }
    .team-inner {
      max-width: 1200px;
      margin: 0 auto;
    }
    .expertise-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 20px;
      margin-top: 50px;
    }
    .expertise-card {
      background: rgba(15, 23, 42, 0.5);
      border: 1px solid var(--border-glass);
      border-radius: 12px;
      padding: 28px 24px;
      text-align: center;
      transition: transform 0.3s, border-color 0.3s;
    }
    .expertise-card:hover { transform: translateY(-4px); border-color: rgba(14, 165, 233, 0.3); }
    .expertise-emoji {
      font-size: 2.5rem;
      margin-bottom: 14px;
      display: block;
    }
    .expertise-card h4 {
      font-family: var(--font-display);
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 8px;
    }
    .expertise-card p { color: var(--text-dim); font-size: 0.88rem; }

    .cta-section {
      max-width: 800px;
      margin: 0 auto;
      padding: 80px 24px 120px;
      text-align: center;
    }
    .cta-box {
      background: var(--bg-card);
      border: 1px solid var(--border-glass);
      border-radius: var(--radius);
      padding: 60px 48px;
      position: relative;
      overflow: hidden;
    }
    .cta-box::before {
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle at 30% 40%, rgba(14,165,233,0.06) 0%, transparent 50%);
      pointer-events: none;
    }
    .cta-box h2 {
      font-family: var(--font-display);
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 16px;
      position: relative;
    }
    .cta-box p {
      color: var(--text-muted);
      font-size: 1.05rem;
      margin-bottom: 32px;
      position: relative;
    }
    .cta-btn {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 14px 36px;
      background: var(--gradient-primary);
      color: white;
      font-family: var(--font-display);
      font-size: 1rem;
      font-weight: 600;
      border: none;
      border-radius: 12px;
      cursor: pointer;
      text-decoration: none;
      transition: transform 0.3s, box-shadow 0.3s;
      position: relative;
    }
    .cta-btn:hover { transform: translateY(-2px); box-shadow: 0 12px 32px var(--color-primary-glow); }

    .footer {
      border-top: 1px solid var(--border-glass);
      padding: 24px;
      text-align: center;
      color: var(--text-dim);
      font-size: 0.85rem;
    }

    @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(1.4); } }

    .reveal { opacity: 0; transform: translateY(40px); transition: opacity 0.8s ease-out, transform 0.8s ease-out; }
    .reveal.visible { opacity: 1; transform: translateY(0); }

    @media (max-width: 768px) {
      .founder-card { grid-template-columns: 1fr; padding: 28px; gap: 32px; }
      .founder-photo { max-width: 280px; margin: 0 auto; }
      .founder-stats { grid-template-columns: repeat(3, 1fr); gap: 12px; }
      .nav-links { gap: 20px; }
      .nav-links a { font-size: 0.85rem; }
      .cta-box { padding: 40px 24px; }
    }
  </style>
</head>
<body>
  <nav class="nav">
    <div class="nav-inner">
      <a href="http://localhost:8000" class="nav-logo">Car Solution</a>
      <ul class="nav-links">
        <li><a href="http://localhost:8000">Home</a></li>
        <li><a href="http://localhost:8005" class="active">About</a></li>
        <li><a href="http://localhost:8001" target="_blank">Services</a></li>
        <li><a href="http://localhost:8004" target="_blank">Appointment</a></li>
      </ul>
    </div>
  </nav>

  <section class="hero">
    <div class="hero-badge"><span class="dot"></span> Trusted Since 2019</div>
    <h1>About<br /><span>Nirmal Hans Car Care & Service Center</span></h1>
    <p class="hero-sub">Reliable, affordable, and high-quality vehicle care delivered by a diploma-qualified automotive specialist and a skilled mechanical & electrical team.</p>
  </section>

  <section class="founder-section">
    <div class="founder-card reveal">
      <div class="founder-photo-wrapper">
        <img class="founder-photo" src="nirmal_hans.jpg" alt="Nirmal Hans – Founder of Car Solution" />
      </div>
      <div class="founder-info">
        <h2 class="founder-name">Nirmal Hans</h2>
        <div class="founder-title">Founder &amp; Lead Specialist</div>
        <p class="founder-bio">Founded by <strong>Mr. Nirmal Hans</strong>, a passionate automobile professional with a <strong>3-Year Diploma in Automobile Engineering</strong> and over <strong>7 years of hands-on experience</strong> in the automotive service industry.</p>
        <p class="founder-bio">With a strong interest in automobiles and extensive practical expertise, our mission is to provide reliable, affordable, and high-quality vehicle care solutions. We specialize in car washing, detailing, maintenance, diagnostics, and repair services.</p>
        <p class="founder-bio">Our strength lies in our highly skilled team, carefully curated from mechanical and electrical engineering backgrounds, enabling us to handle a wide range of automotive services efficiently and professionally.</p>
        <div class="founder-stats">
          <div class="stat"><div class="stat-value">7+</div><div class="stat-label">Years Experience</div></div>
          <div class="stat"><div class="stat-value">3</div><div class="stat-label">Year Diploma</div></div>
          <div class="stat"><div class="stat-value">ME/EE</div><div class="stat-label">Mechanical & Electrical</div></div>
        </div>
      </div>
    </div>
  </section>

  <section class="why-section">
    <div class="section-header reveal">
      <h2>Why <span>Choose Us</span></h2>
      <p>We don't just service cars — we build trust. Here's what sets Car Solution apart.</p>
    </div>
    <div class="why-grid">
      <div class="why-card reveal"><div class="why-icon">🏁</div><h3>7+ Years Experience</h3><p>Decades of combined industry experience delivering dependable automotive care and long-term performance.</p></div>
      <div class="why-card reveal"><div class="why-icon">🎓</div><h3>Diploma-Qualified Specialist</h3><p>Founded by a diploma-qualified automobile professional with a deep understanding of vehicle systems.</p></div>
      <div class="why-card reveal"><div class="why-icon">🧑‍🔧</div><h3>Skilled Technician Team</h3><p>Our technicians are trained in both mechanical and electrical services to handle every repair and maintenance need.</p></div>
      <div class="why-card reveal"><div class="why-icon">✨</div><h3>Advanced Techniques</h3><p>We use modern cleaning, detailing, and servicing methods to deliver premium results for every vehicle.</p></div>
      <div class="why-card reveal"><div class="why-icon">🤝</div><h3>Customer-Focused Approach</h3><p>Transparent pricing, clear communication, and service that prioritizes your convenience and satisfaction.</p></div>
      <div class="why-card reveal"><div class="why-icon">⏱️</div><h3>Timely Delivery</h3><p>Fast, reliable service with attention to detail so your vehicle returns to the road on schedule.</p></div>
    </div>
  </section>

  <section class="why-section">
    <div class="section-header reveal">
      <h2>Our <span>Services</span></h2>
      <p>Comprehensive automotive care designed to keep your vehicle looking great and running safely.</p>
    </div>
    <div class="why-grid">
      <div class="why-card reveal"><div class="why-icon">🚿</div><h3>Premium Car Washing</h3><p>Professional exterior cleaning with gentle care for paint and trim.</p></div>
      <div class="why-card reveal"><div class="why-icon">🧽</div><h3>Interior & Exterior Detailing</h3><p>Complete detailing for cabin refresh, paint enhancement, and overall finish.</p></div>
      <div class="why-card reveal"><div class="why-icon">🛡️</div><h3>Ceramic & Protective Coatings</h3><p>Long-lasting protection to preserve shine and shield against wear.</p></div>
      <div class="why-card reveal"><div class="why-icon">🧼</div><h3>Engine Cleaning</h3><p>Safe, thorough engine bay cleaning to keep performance reliable.</p></div>
      <div class="why-card reveal"><div class="why-icon">⚙️</div><h3>Oil & Filter Changes</h3><p>Routine maintenance to protect your engine and maintain smooth operation.</p></div>
      <div class="why-card reveal"><div class="why-icon">🛑</div><h3>Brake Inspection & Repair</h3><p>Comprehensive brake checks and repairs for safety you can trust.</p></div>
      <div class="why-card reveal"><div class="why-icon">🔌</div><h3>Electrical Diagnostics</h3><p>Expert diagnosis of wiring, sensors, batteries, and charging systems.</p></div>
      <div class="why-card reveal"><div class="why-icon">🔋</div><h3>Battery & Charging System</h3><p>Testing, replacement, and service for reliable starting and electrical health.</p></div>
      <div class="why-card reveal"><div class="why-icon">❄️</div><h3>AC Service & Maintenance</h3><p>Complete air conditioning care for a cooler, more comfortable ride.</p></div>
      <div class="why-card reveal"><div class="why-icon">🚗</div><h3>General Vehicle Servicing</h3><p>Broad maintenance services that keep your vehicle safe and dependable.</p></div>
      <div class="why-card reveal"><div class="why-icon">📦</div><h3>Pickup & Drop Facility</h3><p>Convenient vehicle collection and delivery for a hassle-free service experience.</p></div>
    </div>
  </section>

  <section class="team-section">
    <div class="team-inner">
      <div class="section-header reveal">
        <h2>Our <span>Vision &amp; Mission</span></h2>
        <p>Guided by a commitment to quality, trust, and customer-first automotive care.</p>
      </div>
      <div class="expertise-grid">
        <div class="expertise-card reveal"><span class="expertise-emoji">🌟</span><h4>Our Vision</h4><p>To become the most trusted and customer-centric automobile care and servicing center by delivering exceptional quality, professionalism, and value in every service we provide.</p></div>
        <div class="expertise-card reveal"><span class="expertise-emoji">🎯</span><h4>Our Mission</h4><p>To provide comprehensive automotive care solutions that enhance vehicle performance, safety, appearance, and longevity while maintaining the highest standards of customer satisfaction.</p></div>
      </div>
    </div>
  </section>

  <section class="cta-section">
    <div class="cta-box reveal">
      <h2>Ready to Experience the Difference?</h2>
      <p>Book an appointment today and let our team give your car the care it deserves.</p>
      <a href="http://localhost:8004" class="cta-btn" target="_blank">Book Appointment →</a>
    </div>
  </section>

  <footer class="footer">
    <p>© 2026 Car Solution. All rights reserved. | Built with ❤️ by Nirmal Hans</p>
  </footer>

  <script>
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  </script>
</body>
</html>"""

class AboutHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/about", "/about.html", "/about/", "/about/index.html"):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(ABOUT_PAGE.encode("utf-8"))
        elif self.path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico')):
            file_name = self.path.lstrip('/')
            file_path = os.path.join(os.path.dirname(__file__), file_name)
            if os.path.isfile(file_path):
                mime_type, _ = mimetypes.guess_type(file_path)
                if not mime_type:
                    mime_type = 'application/octet-stream'
                self.send_response(200)
                self.send_header("Content-type", mime_type)
                self.send_header("Cache-Control", "public, max-age=86400")
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")
        else:
            self.send_error(404, "Page not found")

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), AboutHandler) as httpd:
        print(f"Serving Car Solution about page at http://localhost:{PORT}")
        httpd.serve_forever()
