import http.server
import socketserver

PORT = 8003

PACKAGES_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Car Solution | Detailing Service Packages</title>
  
  <!-- Modern Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    /* Premium Design Tokens */
    :root {
      --bg-base: #030712;
      --bg-surface: #0b0f19;
      --bg-surface-glass: rgba(11, 15, 25, 0.65);
      --border-glass: rgba(255, 255, 255, 0.06);
      --border-glass-hover: rgba(255, 255, 255, 0.12);
      
      --color-primary: #0ea5e9;       /* Cyan */
      --color-primary-rgb: 14, 165, 233;
      --color-secondary: #6366f1;     /* Indigo */
      --color-secondary-rgb: 99, 102, 241;
      --color-accent: #f43f5e;        /* Rose */
      
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dark: #64748b;
      
      --font-display: 'Outfit', sans-serif;
      --font-body: 'Inter', sans-serif;
      
      --glow-cyan: 0 0 25px rgba(14, 165, 233, 0.25);
      --glow-indigo: 0 0 25px rgba(99, 102, 241, 0.25);
    }

    /* Reset & Core Styling */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: var(--font-body);
      overflow-x: hidden;
      min-height: 100vh;
      line-height: 1.6;
      /* Ambient glow spots */
      background-image: 
        radial-gradient(circle at 10% 90%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 10%, rgba(14, 165, 233, 0.1) 0%, transparent 45%);
      background-attachment: fixed;
    }

    a {
      color: inherit;
      text-decoration: none;
    }

    button, input, select {
      font-family: inherit;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
      width: 10px;
    }
    ::-webkit-scrollbar-track {
      background: var(--bg-base);
    }
    ::-webkit-scrollbar-thumb {
      background: #1e293b;
      border-radius: 5px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #334155;
    }

    /* Container */
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 24px;
    }

    /* Glassmorphic Navbar */
    .header {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      z-index: 100;
      background: var(--bg-surface-glass);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-glass);
      transition: all 0.3s ease;
    }

    .nav-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      height: 80px;
    }

    .logo {
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: var(--font-display);
      font-weight: 800;
      font-size: 1.5rem;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #f8fafc 40%, var(--color-primary) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .logo-icon {
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--glow-cyan);
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 32px;
    }

    .nav-link {
      font-size: 0.95rem;
      font-weight: 500;
      color: var(--text-muted);
      transition: color 0.25s ease;
      position: relative;
    }

    .nav-link::after {
      content: '';
      position: absolute;
      bottom: -6px;
      left: 0;
      width: 0;
      height: 2px;
      background-color: var(--color-primary);
      transition: width 0.25s ease;
    }

    .nav-link:hover {
      color: var(--text-main);
    }

    .nav-link:hover::after {
      width: 100%;
    }

    /* Buttons Component */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      padding: 14px 28px;
      font-weight: 600;
      font-size: 0.95rem;
      border-radius: 12px;
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      border: none;
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
      color: #020617;
      font-weight: 700;
      box-shadow: 0 10px 25px -5px rgba(14, 165, 233, 0.35);
    }

    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 15px 30px -5px rgba(14, 165, 233, 0.5);
    }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border-glass);
      color: var(--text-main);
    }

    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: var(--border-glass-hover);
      transform: translateY(-2px);
    }

    .btn-sm {
      padding: 10px 20px;
      font-size: 0.85rem;
      border-radius: 8px;
    }

    /* Page Intro */
    .intro-section {
      padding-top: 160px;
      padding-bottom: 50px;
      text-align: center;
    }

    .intro-title {
      font-family: var(--font-display);
      font-weight: 800;
      font-size: 3rem;
      letter-spacing: -0.02em;
      margin-bottom: 16px;
    }

    .intro-title span {
      background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .intro-desc {
      font-size: 1.1rem;
      color: var(--text-muted);
      max-width: 600px;
      margin: 0 auto;
    }

    /* Packages Layout */
    .packages-section {
      padding-bottom: 100px;
    }

    .packages-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 32px;
    }

    @media (min-width: 992px) {
      .packages-grid {
        grid-template-columns: repeat(3, 1fr);
      }
    }

    /* Package Box Card */
    .package-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-glass);
      border-radius: 24px;
      padding: 40px;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
      transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .package-card:hover {
      transform: translateY(-8px);
      border-color: rgba(14, 165, 233, 0.3);
      box-shadow: 0 25px 50px -15px rgba(2, 6, 23, 0.8);
    }

    .package-tag {
      position: absolute;
      top: 24px;
      right: 24px;
      background: rgba(244, 63, 94, 0.1);
      border: 1px solid rgba(244, 63, 94, 0.2);
      color: var(--color-accent);
      font-size: 0.75rem;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: 99px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .package-icon-wrap {
      width: 50px;
      height: 50px;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border-glass);
      border-radius: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--color-primary);
      margin-bottom: 28px;
    }

    .package-name {
      font-family: var(--font-display);
      font-size: 1.6rem;
      font-weight: 700;
      margin-bottom: 12px;
      color: var(--text-main);
    }

    .package-desc {
      font-size: 0.92rem;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 32px;
      min-height: 72px;
    }

    .package-contains-title {
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-dark);
      margin-bottom: 14px;
    }

    .package-services-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 40px;
      flex-grow: 1;
    }

    .service-item {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 0.95rem;
      color: var(--text-main);
      font-weight: 500;
    }

    .service-dot {
      width: 6px;
      height: 6px;
      background: var(--color-primary);
      border-radius: 50%;
    }

    .package-footer {
      border-top: 1px solid var(--border-glass);
      padding-top: 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .package-price-box {
      display: flex;
      flex-direction: column;
    }

    .package-price-val {
      font-family: var(--font-display);
      font-size: 1.6rem;
      font-weight: 800;
      color: var(--text-main);
    }

    .package-price-val span {
      font-size: 0.9rem;
      color: var(--color-primary);
      font-weight: 600;
      margin-right: 4px;
    }
  </style>
</head>
<body>

  <!-- Navigation Bar -->
  <header class="header">
    <div class="container nav-container">
      <a href="http://localhost:8000" class="logo">
        <div class="logo-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#020617" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
          </svg>
        </div>
        Car Solution
      </a>
      
      <nav class="nav-links">
        <a href="http://localhost:8000" class="nav-link">Home</a>
        <a href="http://localhost:8001" class="nav-link">Services</a>
        <a href="http://localhost:8002" class="nav-link">Pricing</a>
        <a href="#" class="nav-link">Packages</a>
        <a href="http://localhost:8004" class="btn btn-primary btn-sm">Book Appointment</a>
      </nav>
    </div>
  </header>

  <!-- Page Intro -->
  <section class="intro-section">
    <div class="container">
      <h1 class="intro-title">Service <span>Packages</span></h1>
      <p class="intro-desc">Choose from our discounted multi-service bundles, carefully grouped for absolute automotive hygiene.</p>
    </div>
  </section>

  <!-- Packages Section -->
  <section class="packages-section">
    <div class="container">
      <div class="packages-grid">
        
        <!-- Package 1: Express Shine -->
        <div class="package-card">
          <div class="package-tag">Save ₹198</div>
          <div class="package-icon-wrap">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
          </div>
          <h3 class="package-name">Express Shine</h3>
          <p class="package-desc">Perfect for routine exterior maintenance. Focuses on overall outer brightness and crystal clear visibility.</p>
          
          <p class="package-contains-title">Includes 3 Services</p>
          <ul class="package-services-list">
            <li class="service-item"><div class="service-dot"></div> Exterior Car Wash</li>
            <li class="service-item"><div class="service-dot"></div> Glass & Mirror Cleaning</li>
            <li class="service-item"><div class="service-dot"></div> Tire & Wheel Cleaning</li>
          </ul>

          <div class="package-footer">
            <div class="package-price-box">
              <span class="package-price-val"><span>RS</span> 749</span>
            </div>
            <a href="http://localhost:8004/?type=package&id=express" class="btn btn-primary btn-sm">Book Now</a>
          </div>
        </div>

        <!-- Package 2: Interior Revival -->
        <div class="package-card" style="border-color: rgba(99, 102, 241, 0.25);">
          <div class="package-tag">Save ₹348</div>
          <div class="package-icon-wrap" style="color: var(--color-secondary);">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="22" y1="12" x2="18" y2="12"/>
              <line x1="6" y1="12" x2="2" y2="12"/>
            </svg>
          </div>
          <h3 class="package-name">Interior Revival</h3>
          <p class="package-desc">Complete deep-cleaning treatment for your cabin. Sanitizes your seats and steering console thoroughly.</p>
          
          <p class="package-contains-title">Includes 3 Services</p>
          <ul class="package-services-list">
            <li class="service-item"><div class="service-dot" style="background: var(--color-secondary);"></div> Interior Cleaning</li>
            <li class="service-item"><div class="service-dot" style="background: var(--color-secondary);"></div> Vacuum Cleaning</li>
            <li class="service-item"><div class="service-dot" style="background: var(--color-secondary);"></div> Dashboard Cleaning</li>
          </ul>

          <div class="package-footer">
            <div class="package-price-box">
              <span class="package-price-val"><span>RS</span> 1,199</span>
            </div>
            <a href="http://localhost:8004/?type=package&id=interior" class="btn btn-primary btn-sm" style="background: linear-gradient(135deg, var(--color-secondary), var(--color-primary));">Book Now</a>
          </div>
        </div>

        <!-- Package 3: Showroom Ready -->
        <div class="package-card">
          <div class="package-tag">Save ₹348</div>
          <div class="package-icon-wrap">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5"/>
            </svg>
          </div>
          <h3 class="package-name">Showroom Ready</h3>
          <p class="package-desc">Ultimate deep exterior restoration. Incorporates paint scrubbing and high-pressure underbody dirt flushing.</p>
          
          <p class="package-contains-title">Includes 3 Services</p>
          <ul class="package-services-list">
            <li class="service-item"><div class="service-dot"></div> Car Washing & Scrubbing</li>
            <li class="service-item"><div class="service-dot"></div> Pressure Washing</li>
            <li class="service-item"><div class="service-dot"></div> Tire & Wheel Cleaning</li>
          </ul>

          <div class="package-footer">
            <div class="package-price-box">
              <span class="package-price-val"><span>RS</span> 1,299</span>
            </div>
            <a href="http://localhost:8004/?type=package&id=showroom" class="btn btn-primary btn-sm">Book Now</a>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-logo">Car Solution</div>
      <p class="footer-text">Professional Auto Aesthetics & Detailing Science.</p>
      <p>&copy; 2026 Car Solution. All rights reserved.</p>
    </div>
  </footer>
</body>
</html>"""

class PackagesHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/packages", "/index", "/index.html"):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(PACKAGES_PAGE.encode("utf-8"))
        else:
            self.send_error(404, "Page not found")

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), PackagesHandler) as httpd:
        print(f"Serving Car Solution packages page at http://localhost:{PORT}")
        httpd.serve_forever()
