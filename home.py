import http.server
import socketserver

PORT = 8000

HOME_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Car Solution | Elite Automotive Detailing</title>
  
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
        radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(99, 102, 241, 0.1) 0%, transparent 45%);
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

    /* Hero Section */
    .hero {
      padding-top: 180px;
      padding-bottom: 120px;
      position: relative;
      min-height: calc(100vh - 80px);
      display: flex;
      align-items: center;
    }

    .hero-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 60px;
      align-items: center;
      width: 100%;
    }

    @media (min-width: 992px) {
      .hero-grid {
        grid-template-columns: 1.2fr 1fr;
      }
    }

    .hero-content {
      max-width: 650px;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(14, 165, 233, 0.1);
      border: 1px solid rgba(14, 165, 233, 0.2);
      color: var(--color-primary);
      padding: 6px 16px;
      border-radius: 99px;
      font-size: 0.85rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 24px;
    }

    .hero-title {
      font-family: var(--font-display);
      font-weight: 800;
      font-size: clamp(2.5rem, 5vw, 4.2rem);
      line-height: 1.1;
      letter-spacing: -0.03em;
      margin-bottom: 24px;
    }

    .hero-title span {
      background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-desc {
      font-size: 1.15rem;
      color: var(--text-muted);
      margin-bottom: 40px;
      font-weight: 400;
      line-height: 1.7;
    }

    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
    }

    /* Hero Graphic (Premium Glowing SVG Car) */
    .hero-visual {
      position: relative;
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .car-glow-ring {
      position: absolute;
      width: 80%;
      height: 80%;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 60%);
      filter: blur(40px);
      z-index: 1;
      animation: pulsate 6s infinite ease-in-out;
    }

    .visual-wrapper {
      position: relative;
      z-index: 2;
      background: rgba(11, 15, 25, 0.5);
      border: 1px solid var(--border-glass);
      border-radius: 24px;
      padding: 30px;
      width: 100%;
      box-shadow: var(--glow-indigo);
      backdrop-filter: blur(10px);
    }

    .visual-svg {
      width: 100%;
      height: auto;
      display: block;
    }

    /* Footer */
    .footer {
      background: #020617;
      border-top: 1px solid var(--border-glass);
      padding: 48px 0;
      text-align: center;
      color: var(--text-dark);
      font-size: 0.9rem;
    }

    .footer-logo {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 1.25rem;
      color: var(--text-main);
      margin-bottom: 16px;
    }

    .footer-text {
      margin-bottom: 24px;
    }

    /* Keyframe Animations */
    @keyframes pulsate {
      0%, 100% {
        transform: scale(1);
        opacity: 0.8;
      }
      50% {
        transform: scale(1.08);
        opacity: 1;
      }
    }

    @keyframes dash {
      to {
        stroke-dashoffset: 0;
      }
    }
  </style>
</head>
<body>

  <!-- Navigation Bar -->
  <header class="header">
    <div class="container nav-container">
      <a href="#" class="logo">
        <div class="logo-icon">
          <!-- Sleek Clean/Wash Icon -->
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#020617" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
          </svg>
        </div>
        Car Solution
      </a>
      
      <nav class="nav-links">
        <a href="http://localhost:8000" class="nav-link">Home</a>
        <a href="http://localhost:8005" class="nav-link">About</a>
        <a href="http://localhost:8001" class="nav-link">Services</a>
        <a href="http://localhost:8002" class="nav-link">Pricing</a>
        <a href="http://localhost:8003" class="nav-link">Packages</a>
        <a href="http://localhost:8004" class="btn btn-primary btn-sm">Book Appointment</a>
      </nav>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero">
    <div class="container hero-grid">
      <div class="hero-content">
        <div class="badge">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" style="margin-top:-2px">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
          No. 1 Premium Car Care
        </div>
        <h1 class="hero-title">Stunning Glow.<br><span>Uncompromising Care.</span></h1>
        <p class="hero-desc">
          Car Solution delivers detailing excellence. Whether you need absolute gloss restoration or premium surface sterilization, we treat your automobile with ultimate precision.
        </p>
        <div class="hero-actions">
          <a href="http://localhost:8005" class="btn btn-primary">About Us</a>
          <a href="http://localhost:8001" class="btn btn-secondary">Check Services</a>
        </div>
      </div>

      <div class="hero-visual">
        <div class="car-glow-ring"></div>
        <div class="visual-wrapper">
          <!-- Sleek Vector wireframe sports car styling -->
          <svg class="visual-wrapper-svg" width="100%" height="240" viewBox="0 0 600 240" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Background Glow lines -->
            <path d="M50 120 h500" stroke="rgba(99, 102, 241, 0.15)" stroke-width="2" />
            <path d="M50 140 h500" stroke="rgba(14, 165, 233, 0.15)" stroke-width="1" />
            
            <!-- Sleek Sports Car Wireframe Silhouette -->
            <path d="M120 160 
                     C130 160, 160 160, 175 135 
                     C185 120, 205 95, 240 85 
                     C275 75, 340 75, 380 92 
                     C410 105, 435 125, 455 128 
                     C475 130, 485 135, 495 160
                     C500 165, 485 168, 475 168
                     C460 168, 455 160, 440 160
                     C420 160, 415 170, 395 170
                     C375 170, 370 160, 230 160
                     C210 160, 205 170, 185 170
                     C165 170, 160 160, 145 160
                     C135 160, 120 160, 120 160 Z" 
                  stroke="url(#car-gradient)" 
                  stroke-width="3" 
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  style="stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: dash 3.5s forwards ease-in-out;" />

            <!-- Highlight glow elements representing laser/clean details -->
            <circle cx="185" cy="160" r="22" stroke="var(--color-primary)" stroke-width="2.5" stroke-dasharray="8 4" />
            <circle cx="185" cy="160" r="6" fill="var(--color-primary)" />
            <circle cx="410" cy="160" r="22" stroke="var(--color-secondary)" stroke-width="2.5" stroke-dasharray="8 4" />
            <circle cx="410" cy="160" r="6" fill="var(--color-secondary)" />

            <!-- Underbody Light Glow -->
            <path d="M210 172 h170" stroke="var(--color-primary)" stroke-width="5" stroke-linecap="round" opacity="0.6" style="filter: blur(4px);" />

            <defs>
              <linearGradient id="car-gradient" x1="120" y1="120" x2="495" y2="120" gradientUnits="userSpaceOnUse">
                <stop stop-color="#0ea5e9" />
                <stop offset="0.5" stop-color="#6366f1" />
                <stop offset="1" stop-color="#f43f5e" />
              </linearGradient>
            </defs>
          </svg>
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

  <!-- Pure JS Logic -->
  <script>
    // Shrink header on scroll
    window.addEventListener('scroll', () => {
      const header = document.querySelector('.header');
      if (window.scrollY > 40) {
        header.style.padding = '8px 0';
        header.style.background = 'rgba(3, 7, 18, 0.85)';
      } else {
        header.style.padding = '0';
        header.style.background = 'var(--bg-surface-glass)';
      }
    });
  </script>
</body>
</html>"""

class HomeHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/home", "/index", "/index.html"):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HOME_PAGE.encode("utf-8"))
        elif self.path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico')):
            import os
            import mimetypes
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
    with socketserver.TCPServer(("", PORT), HomeHandler) as httpd:
        print(f"Serving Car Solution homepage at http://localhost:{PORT}")
        httpd.serve_forever()
