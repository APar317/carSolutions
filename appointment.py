import http.server
import socketserver
import json
import urllib.parse

PORT = 8004

# In-memory booking database
# Bookings are represented as:
# {
#   "date": "YYYY-MM-DD",
#   "time": "HH:MM",
#   "duration": 15 | 30 | 60,
#   "name": "John Doe",
#   "phone": "9876543210",
#   "model": "Maruti Swift",
#   "type": "service" | "package" | "subscriber",
#   "itemId": "exterior"
# }
BOOKINGS = [
    # Pre-populate some dummy bookings for testing slot blocking
    {"date": "2026-06-10", "time": "18:00", "duration": 60, "name": "Rajesh Kumar", "phone": "9988776655", "model": "Jaguar XF", "type": "subscriber", "itemId": "elite"},
    {"date": "2026-06-10", "time": "20:30", "duration": 15, "name": "Amit Singh", "phone": "9876543211", "model": "Maruti Swift", "type": "service", "itemId": "exterior"},
    {"date": "2026-06-13", "time": "10:00", "duration": 30, "name": "Vikram Rathore", "phone": "9123456789", "model": "Maruti Baleno", "type": "package", "itemId": "express"},
]

def check_overlap(date, start_time, duration):
    """
    Returns True if a booking on `date` starting at `start_time` (HH:MM)
    with `duration` (minutes) overlaps with any existing booking.
    """
    new_h, new_m = map(int, start_time.split(":"))
    new_start = new_h * 60 + new_m
    new_end = new_start + duration

    for b in BOOKINGS:
        if b["date"] != date:
            continue
        exist_h, exist_m = map(int, b["time"].split(":"))
        exist_start = exist_h * 60 + exist_m
        exist_end = exist_start + b["duration"]

        # Standard overlap check:
        # A starts before B ends AND A ends after B starts
        if new_start < exist_end and new_end > exist_start:
            return True
    return False

APPOINTMENT_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Car Solution | Book Appointment</title>
  
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
        radial-gradient(circle at 50% 10%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 10% 90%, rgba(14, 165, 233, 0.1) 0%, transparent 45%);
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

    .btn-primary:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 15px 30px -5px rgba(14, 165, 233, 0.5);
    }

    .btn-primary:disabled {
      opacity: 0.5;
      cursor: not-allowed;
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

    /* Page Layout */
    .page-intro {
      padding-top: 160px;
      padding-bottom: 40px;
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
    }

    /* Booking Grid */
    .booking-layout {
      display: grid;
      grid-template-columns: 1fr;
      gap: 40px;
      padding-bottom: 120px;
    }

    @media (min-width: 992px) {
      .booking-layout {
        grid-template-columns: 1fr 1.3fr;
      }
    }

    /* Left panel: Config and Calendar */
    .config-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-glass);
      border-radius: 24px;
      padding: 36px;
      height: fit-content;
    }

    .section-subtitle {
      font-family: var(--font-display);
      font-size: 1.4rem;
      font-weight: 700;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border-glass);
      padding-bottom: 12px;
    }

    .form-group {
      margin-bottom: 24px;
    }

    .form-label {
      display: block;
      font-size: 0.82rem;
      font-weight: 700;
      margin-bottom: 8px;
      color: var(--text-main);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .form-control {
      width: 100%;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border-glass);
      border-radius: 12px;
      padding: 14px 18px;
      color: var(--text-main);
      font-size: 0.95rem;
      transition: all 0.25s ease;
    }

    .form-control:focus {
      outline: none;
      border-color: var(--color-primary);
      background: rgba(255, 255, 255, 0.05);
      box-shadow: 0 0 10px rgba(14, 165, 233, 0.15);
    }

    select.form-control {
      appearance: none;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394a3b8'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: right 18px center;
      background-size: 16px;
    }

    .summary-badge {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(14, 165, 233, 0.05);
      border: 1px solid rgba(14, 165, 233, 0.15);
      padding: 16px 20px;
      border-radius: 14px;
      margin-top: 10px;
    }

    .summary-label {
      font-size: 0.9rem;
      color: var(--text-muted);
    }

    .summary-val {
      font-family: var(--font-display);
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--color-primary);
    }

    /* Right panel: Slots and Client details */
    .slots-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-glass);
      border-radius: 24px;
      padding: 36px;
      display: flex;
      flex-direction: column;
    }

    .operating-info {
      font-size: 0.88rem;
      color: var(--text-muted);
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border-glass);
      border-radius: 12px;
      padding: 14px 18px;
      margin-bottom: 24px;
      display: flex;
      align-items: flex-start;
      gap: 12px;
    }

    .operating-info-icon {
      color: var(--color-primary);
      width: 20px;
      height: 20px;
      flex-shrink: 0;
      margin-top: 2px;
    }

    /* Slots Grid */
    .slots-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
      gap: 12px;
      margin-bottom: 32px;
      max-height: 280px;
      overflow-y: auto;
      padding-right: 6px;
    }

    .slot-item {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border-glass);
      border-radius: 10px;
      padding: 12px;
      text-align: center;
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }

    .slot-item:hover:not(.booked):not(.selected) {
      border-color: var(--color-primary);
      background: rgba(14, 165, 233, 0.08);
      color: var(--text-main);
    }

    .slot-item.selected {
      background: var(--color-primary);
      border-color: var(--color-primary);
      color: #020617;
      box-shadow: var(--glow-cyan);
    }

    .slot-item.booked {
      opacity: 0.35;
      background: rgba(255, 255, 255, 0.01);
      border-color: var(--border-glass);
      color: var(--text-dark);
      cursor: not-allowed;
      position: relative;
    }

    .slot-item-status {
      font-size: 0.72rem;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }

    .slot-item.booked .slot-item-status {
      color: var(--color-accent);
    }

    .slot-item:not(.booked) .slot-item-status {
      color: #10b981;
    }

    .slot-item.selected .slot-item-status {
      color: #020617;
    }

    .form-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
    }

    @media (min-width: 768px) {
      .form-grid {
        grid-template-columns: 1fr 1fr;
      }
    }

    /* Success screen overlay */
    .success-container {
      display: none;
      text-align: center;
      padding: 40px 0;
      max-width: 600px;
      margin: 0 auto;
      background: var(--bg-surface);
      border: 1px solid var(--border-glass);
      border-radius: 28px;
      padding: 50px;
      box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
    }

    .success-icon-wrap {
      width: 80px;
      height: 80px;
      background: rgba(14, 165, 233, 0.15);
      border: 2px solid var(--color-primary);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 28px;
      color: var(--color-primary);
      box-shadow: var(--glow-cyan);
    }

    .success-title {
      font-family: var(--font-display);
      font-size: 2.2rem;
      font-weight: 800;
      margin-bottom: 12px;
    }

    .success-desc {
      font-size: 1.05rem;
      color: var(--text-muted);
      margin-bottom: 36px;
    }

    .receipt-box {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border-glass);
      border-radius: 16px;
      padding: 24px;
      text-align: left;
      margin-bottom: 36px;
    }

    .receipt-row {
      display: flex;
      justify-content: space-between;
      padding: 10px 0;
      border-bottom: 1px solid rgba(255,255,255,0.04);
      font-size: 0.95rem;
    }

    .receipt-row:last-child {
      border-bottom: none;
    }

    .receipt-label {
      color: var(--text-muted);
    }

    .receipt-val {
      font-weight: 600;
      color: var(--text-main);
    }

    .receipt-val.highlighted {
      color: var(--color-primary);
      font-family: var(--font-display);
      font-weight: 700;
    }

    /* Footer */
    .footer {
      background: #020617;
      border-top: 1px solid var(--border-glass);
      padding: 48px 0;
      text-align: center;
      color: var(--text-dark);
      font-size: 0.9rem;
      margin-top: auto;
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
        <a href="http://localhost:8003" class="nav-link">Packages</a>
        <a href="#" class="btn btn-primary btn-sm">Book Appointment</a>
      </nav>
    </div>
  </header>

  <!-- Page Intro -->
  <section class="page-intro" id="introSection">
    <div class="container">
      <h1 class="intro-title">Automotive <span>Scheduler</span></h1>
      <p class="intro-desc">Real-time slot allocation with optimized hold times for your wash session.</p>
    </div>
  </section>

  <!-- Main Booking Form Content -->
  <section class="container" id="bookingMainContent">
    <div class="booking-layout">
      
      <!-- Left Config Card -->
      <div class="config-card">
        <h3 class="section-subtitle">1. Booking Options</h3>
        
        <div class="form-group">
          <label class="form-label">Booking Category</label>
          <select class="form-control" id="formType" onchange="updateBookingCategory()" required>
            <option value="service">Individual Service</option>
            <option value="package">Service Package</option>
            <option value="subscriber">Subscriber Plan</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Item / Plan Selection</label>
          <select class="form-control" id="formItem" onchange="updateSelectedDetails()" required>
            <!-- Dynamically populated -->
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Detailing Date</label>
          <input type="date" class="form-control" id="formDate" onchange="loadSlots()" required />
        </div>

        <div class="summary-badge">
          <span class="summary-label">Car Hold Duration:</span>
          <span class="summary-val" id="holdDurationText">15 Minutes</span>
        </div>
      </div>

      <!-- Right Slots & Client Details Card -->
      <div class="slots-card">
        <h3 class="section-subtitle">2. Time Slot & Customer Info</h3>
        
        <!-- Operating Hours Display -->
        <div class="operating-info">
          <svg class="operating-info-icon" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <div>
            <p style="font-weight: 600; color: var(--text-main); margin-bottom: 2px;">Shop Detailing Hours</p>
            <p id="operatingHoursText">Select a date to view scheduling times.</p>
          </div>
        </div>

        <!-- Time Slots Grid -->
        <div class="form-group">
          <label class="form-label">Select Start Time</label>
          <div class="slots-grid" id="slotsGrid">
            <!-- Dynamically populated -->
          </div>
        </div>

        <!-- Customer Form -->
        <form id="reservationForm" onsubmit="submitReservation(event)">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Client Name</label>
              <input type="text" class="form-control" id="formName" placeholder="Your full name" required />
            </div>
            <div class="form-group">
              <label class="form-label">Phone Number</label>
              <input type="tel" class="form-control" id="formPhone" placeholder="Your phone number" required />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Car Brand & Model</label>
            <input type="text" class="form-control" id="formCarModel" placeholder="e.g. Maruti Swift, Jaguar XF, G-Wagon" required />
          </div>

          <button type="submit" class="btn btn-primary" id="submitBtn" style="width: 100%; margin-top: 10px;" disabled>Confirm Detailing Appointment</button>
        </form>

      </div>

    </div>
  </section>

  <!-- Success Page Content -->
  <section class="container" style="padding: 100px 0;" id="bookingSuccessContent">
    <div class="success-container">
      <div class="success-icon-wrap">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
      </div>
      <h2 class="success-title">Spot Reserved!</h2>
      <p class="success-desc">Your automobile detailing appointment has been locked successfully.</p>
      
      <div class="receipt-box">
        <div class="receipt-row">
          <span class="receipt-label">Booking Code</span>
          <span class="receipt-val highlighted" id="successResId">CS-89247</span>
        </div>
        <div class="receipt-row">
          <span class="receipt-label">Detailing Date</span>
          <span class="receipt-val" id="successDate">2026-06-10</span>
        </div>
        <div class="receipt-row">
          <span class="receipt-label">Time Window (Hold)</span>
          <span class="receipt-val" id="successTimeWindow">06:00 PM - 07:00 PM (60 mins)</span>
        </div>
        <div class="receipt-row">
          <span class="receipt-label">Service Category</span>
          <span class="receipt-val" id="successCategory">Elite Plan Subscription</span>
        </div>
        <div class="receipt-row">
          <span class="receipt-label">Vehicle Type</span>
          <span class="receipt-val" id="successVehicle">Jaguar XF</span>
        </div>
      </div>

      <button class="btn btn-secondary" onclick="resetForm()">Book Another Appointment</button>
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

  <!-- Real-time slot selection and booking JS -->
  <script>
    const categoryOptions = {
      service: [
        { id: 'scrubbing', name: 'Car Washing & Scrubbing (RS 999)', duration: 15 },
        { id: 'exterior', name: 'Exterior Car Wash (RS 499)', duration: 15 },
        { id: 'interior', name: 'Interior Cleaning (RS 899)', duration: 15 },
        { id: 'vacuum', name: 'Vacuum Cleaning (RS 299)', duration: 15 },
        { id: 'dashboard', name: 'Dashboard Cleaning (RS 349)', duration: 15 },
        { id: 'glass', name: 'Glass & Mirror Cleaning (RS 199)', duration: 15 },
        { id: 'tire', name: 'Tire & Wheel Cleaning (RS 249)', duration: 15 },
        { id: 'pressure', name: 'Pressure Washing (RS 399)', duration: 15 }
      ],
      package: [
        { id: 'express', name: 'Express Shine Package (RS 749)', duration: 30 },
        { id: 'interior', name: 'Interior Revival Package (RS 1199)', duration: 30 },
        { id: 'showroom', name: 'Showroom Ready Package (RS 1299)', duration: 30 }
      ],
      subscriber: [
        { id: 'basic', name: 'Basic Plan Subscription (RS 2999/mo)', duration: 60 },
        { id: 'elite', name: 'Elite Plan Subscription (RS 7999/mo)', duration: 60 }
      ]
    };

    // Hold durations based on type
    const durations = {
      service: 15,
      package: 30,
      subscriber: 60
    };

    let selectedTime = null;

    // Set today as minimum date
    const dateInput = document.getElementById('formDate');
    const todayStr = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', todayStr);
    dateInput.value = todayStr;

    // Parse Query Params on Load
    window.addEventListener('DOMContentLoaded', () => {
      const urlParams = new URLSearchParams(window.location.search);
      const urlType = urlParams.get('type');
      const urlId = urlParams.get('id');

      if (urlType && categoryOptions[urlType]) {
        document.getElementById('formType').value = urlType;
      }
      
      updateBookingCategory();

      if (urlId) {
        document.getElementById('formItem').value = urlId;
        updateSelectedDetails();
      }
      
      loadSlots();
    });

    function updateBookingCategory() {
      const type = document.getElementById('formType').value;
      const itemSelect = document.getElementById('formItem');
      
      // Clear options
      itemSelect.innerHTML = '';
      
      // Populate items
      categoryOptions[type].forEach(opt => {
        const el = document.createElement('option');
        el.value = opt.id;
        el.innerText = opt.name;
        itemSelect.appendChild(el);
      });

      updateSelectedDetails();
      loadSlots();
    }

    function updateSelectedDetails() {
      const type = document.getElementById('formType').value;
      const duration = durations[type];
      document.getElementById('holdDurationText').innerText = duration + ' Minutes';
      
      // Clear selected slot when changing type since holds can now overlap differently
      selectedTime = null;
      document.getElementById('submitBtn').disabled = true;
    }

    function isWeekend(dateStr) {
      const day = new Date(dateStr).getDay();
      return day === 0 || day === 6; // Sunday or Saturday
    }

    async function loadSlots() {
      const dateVal = dateInput.value;
      if (!dateVal) return;

      const type = document.getElementById('formType').value;
      const duration = durations[type];
      const slotsGrid = document.getElementById('slotsGrid');
      const operatingHoursText = document.getElementById('operatingHoursText');
      
      slotsGrid.innerHTML = '<p style="color: var(--text-dark); grid-column: 1/-1;">Loading slots...</p>';
      selectedTime = null;
      document.getElementById('submitBtn').disabled = true;

      // Update operating info text
      const weekend = isWeekend(dateVal);
      let startHour = 17; // 5 PM
      let endHour = 23;   // 11 PM
      if (weekend) {
        startHour = 6;    // 6 AM
        endHour = 18;     // 6 PM
        operatingHoursText.innerText = 'Weekend hours: 6:00 AM to 6:00 PM';
      } else {
        operatingHoursText.innerText = 'Weekday hours: 5:00 PM to 11:00 PM';
      }

      // Fetch booked slots for the date
      let bookedIntervals = [];
      try {
        const res = await fetch(`/api/bookings?date=${dateVal}`);
        if (res.ok) {
          bookedIntervals = await res.json();
        }
      } catch (err) {
        console.error('Error fetching bookings:', err);
      }

      // Clear loading indicator
      slotsGrid.innerHTML = '';

      // Generate 15-minute slot intervals
      let currentMin = startHour * 60;
      const endMin = endHour * 60;

      while (currentMin < endMin) {
        const hh = String(Math.floor(currentMin / 60)).padStart(2, '0');
        const mm = String(currentMin % 60).padStart(2, '0');
        const timeStr = `${hh}:${mm}`;

        // Verify if booking this start time with the current duration would overlap with any booked interval
        const isOverlap = checkBookingOverlap(currentMin, duration, bookedIntervals);

        const slotEl = document.createElement('div');
        slotEl.className = 'slot-item';
        
        // Formatted display
        const displayH = Math.floor(currentMin / 60);
        const ampm = displayH >= 12 ? 'PM' : 'AM';
        const displayH12 = displayH % 12 || 12;
        const displayTime = `${displayH12}:${mm} ${ampm}`;

        if (isOverlap) {
          slotEl.classList.add('booked');
          slotEl.innerHTML = `
            <span>${displayTime}</span>
            <span class="slot-item-status">Booked</span>
          `;
        } else {
          slotEl.onclick = () => selectSlot(slotEl, timeStr);
          slotEl.innerHTML = `
            <span>${displayTime}</span>
            <span class="slot-item-status">Available</span>
          `;
        }

        slotsGrid.appendChild(slotEl);
        currentMin += 15; // Increment by 15 mins
      }
    }

    function checkBookingOverlap(startMin, duration, bookedList) {
      const newStart = startMin;
      const newEnd = startMin + duration;

      for (let b of bookedList) {
        const parts = b.time.split(':');
        const existStart = parseInt(parts[0]) * 60 + parseInt(parts[1]);
        const existEnd = existStart + b.duration;

        if (newStart < existEnd && newEnd > existStart) {
          return true;
        }
      }
      return false;
    }

    function selectSlot(element, timeStr) {
      // Remove selection from previous
      const active = document.querySelector('.slot-item.selected');
      if (active) active.classList.remove('selected');

      element.classList.add('selected');
      selectedTime = timeStr;
      
      // Enable submit button
      document.getElementById('submitBtn').disabled = false;
    }

    async function submitReservation(e) {
      e.preventDefault();
      if (!selectedTime) return;

      const type = document.getElementById('formType').value;
      const itemId = document.getElementById('formItem').value;
      const duration = durations[type];
      
      const payload = {
        date: dateInput.value,
        time: selectedTime,
        duration: duration,
        name: document.getElementById('formName').value,
        phone: document.getElementById('formPhone').value,
        model: document.getElementById('formCarModel').value,
        type: type,
        itemId: itemId
      };

      try {
        const res = await fetch('/api/book', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          const data = await res.json();
          showSuccess(data.booking);
        } else {
          const errData = await res.json();
          alert('Error: ' + errData.message);
        }
      } catch (err) {
        alert('Booking failed. Please try again.');
      }
    }

    function showSuccess(booking) {
      document.getElementById('bookingMainContent').style.display = 'none';
      document.getElementById('introSection').style.display = 'none';
      
      document.getElementById('successResId').innerText = booking.resId;
      document.getElementById('successDate').innerText = booking.date;
      
      // Calculate end time
      const parts = booking.time.split(':');
      const startMin = parseInt(parts[0]) * 60 + parseInt(parts[1]);
      const endMin = startMin + booking.duration;

      const formatTime = (min) => {
        const h = Math.floor(min / 60);
        const m = String(min % 60).padStart(2, '0');
        const ampm = h >= 12 ? 'PM' : 'AM';
        const h12 = h % 12 || 12;
        return `${h12}:${m} ${ampm}`;
      };

      document.getElementById('successTimeWindow').innerText = `${formatTime(startMin)} - ${formatTime(endMin)} (${booking.duration} mins)`;
      
      const itemSelect = document.getElementById('formItem');
      const serviceName = itemSelect.options[itemSelect.selectedIndex].text.split(' (RS')[0];
      document.getElementById('successCategory').innerText = serviceName;
      document.getElementById('successVehicle').innerText = booking.model;

      document.getElementById('bookingSuccessContent').style.display = 'block';
      window.scrollTo(0, 0);
    }

    function resetForm() {
      document.getElementById('bookingSuccessContent').style.display = 'none';
      document.getElementById('bookingMainContent').style.display = 'grid';
      document.getElementById('introSection').style.display = 'block';
      
      document.getElementById('reservationForm').reset();
      selectedTime = null;
      document.getElementById('submitBtn').disabled = true;
      loadSlots();
    }
  </script>
</body>
</html>"""

class AppointmentHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # JSON API: GET /api/bookings?date=YYYY-MM-DD
        if parsed_path.path == "/api/bookings":
            params = urllib.parse.parse_qs(parsed_path.query)
            date_query = params.get("date", [""])[0]
            
            # Filter bookings for the requested date
            filtered = [
                {"time": b["time"], "duration": b["duration"]}
                for b in BOOKINGS if b["date"] == date_query
            ]
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(filtered).encode("utf-8"))
            
        # HTML Page: GET /
        elif parsed_path.path in ("/", "/appointment", "/index", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(APPOINTMENT_PAGE.encode("utf-8"))
        else:
            self.send_error(404, "Page not found")

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # JSON API: POST /api/book
        if parsed_path.path == "/api/book":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length).decode("utf-8")
            
            try:
                data = json.loads(body)
                date = data.get("date")
                time = data.get("time")
                duration = int(data.get("duration", 15))
                name = data.get("name")
                phone = data.get("phone")
                model = data.get("model")
                b_type = data.get("type")
                item_id = data.get("itemId")
                
                # Check for overlaps on the server-side as well (integrity check)
                if check_overlap(date, time, duration):
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"message": "This time slot overlaps with an existing booking."}).encode("utf-8"))
                    return
                
                # Generate reservation ID
                res_id = "CS-RES-" + str(100000 + len(BOOKINGS) * 7 + hash(name + phone) % 899999)
                
                new_booking = {
                    "date": date,
                    "time": time,
                    "duration": duration,
                    "name": name,
                    "phone": phone,
                    "model": model,
                    "type": b_type,
                    "itemId": item_id,
                    "resId": res_id
                }
                
                BOOKINGS.append(new_booking)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "booking": new_booking}).encode("utf-8"))
                
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Server error processing booking.", "details": str(e)}).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint not found")

    def do_OPTIONS(self):
        # Support CORS pre-flight
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), AppointmentHandler) as httpd:
        print(f"Serving Car Solution scheduler at http://localhost:{PORT}")
        httpd.serve_forever()
