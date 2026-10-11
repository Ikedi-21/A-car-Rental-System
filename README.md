# 🚗 Driftwood Motors — Car Rental System

A full-featured car rental web application built with **Django 6.1**, featuring customer-facing browsing/booking flows and a dedicated admin dashboard for complete fleet and business management.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [URL Routes](#url-routes)
- [Getting Started](#getting-started)
- [Running the Project](#running-the-project)
- [Admin Dashboard](#admin-dashboard)
- [User Roles](#user-roles)
- [Configuration](#configuration)
- [Car Filtering & Sorting](#car-filtering--sorting)
- [Booking Logic](#booking-logic)

---

## Overview

Driftwood Motors is a semester project implementing a complete **Car Rental System (CRS)**. Customers can browse an available fleet, filter and sort vehicles, make booking requests, and manage their account. Site administrators get a dedicated dashboard to manage every aspect of the platform — cars, brands, bookings, users, testimonials, contact queries, newsletter subscribers, site content, and contact details.

---

## Features

### 🧑‍💻 Customer-Facing

| Feature | Description |
|---|---|
| **Browse Fleet** | View all available cars with filtering (category, brand, fuel type, transmission, price range) and sorting |
| **Car Detail** | Full vehicle info page with similar car suggestions |
| **Booking** | Authenticated users can book a car — total price calculated server-side |
| **Booking History** | Users can view all past and current bookings |
| **User Registration & Login** | Standard register/login/logout flow |
| **Password Reset** | Full 4-step email-based password reset flow |
| **User Profile** | View and update profile (phone, address) and change password |
| **Testimonials** | Registered users can submit reviews with a 1–5 star rating |
| **Contact Form** | Public contact form that logs queries for admin review |
| **Newsletter Signup** | Footer newsletter subscription form |

### 🛠️ Admin Dashboard

| Feature | Description |
|---|---|
| **Overview** | Stats: user count, booking count, subscriber count, and new queries |
| **Brand Management** | Add, edit, delete car brands with logo upload |
| **Fleet Management** | Add, edit, delete vehicles with full details and image upload |
| **Booking Management** | View all bookings; update status (Pending → Confirmed → Completed / Cancelled) |
| **User Management** | View all registered users |
| **Testimonial Management** | Activate / deactivate customer testimonials |
| **Contact Query Management** | View and resolve submitted contact queries |
| **Subscriber Management** | View and delete newsletter subscribers |
| **Site Content Editor** | Edit page content (titles, body text) by key — no code changes needed |
| **Contact Details Editor** | Update the public contact info (address, phone, email, map embed) |
| **Admin Password Change** | Secure in-dashboard password change |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | Django 6.1.1 |
| **Language** | Python 3.x |
| **Database** | SQLite 3 (development) |
| **Image Handling** | Pillow 12.3.0 |
| **Static Files** | WhiteNoise 6.12.0 |
| **WSGI / ASGI** | Gunicorn / Uvicorn |
| **Templating** | Django Templates |

---

## Project Structure

```
car-rental-system/
│
├── core/                   # Project config (settings, root URLs, WSGI/ASGI)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── static/             # Global static files (CSS, JS, images)
│   └── templates/          # Base templates and shared partials
│       ├── base.html
│       ├── admin_base.html
│       └── includes/
│
├── accounts/               # Registration, login, profile, password management
├── cars/                   # Car catalogue, filtering, and detail pages
├── bookings/               # Booking creation and booking history
├── testimonials/           # Customer reviews / testimonials
├── contact/                # Contact Us form, newsletter signup, contact details
├── pages/                  # Static pages (Home, About) + SiteContent model
├── dashboard/              # Staff-only admin dashboard (full CRUD)
│
├── media/                  # Uploaded files (car images, brand logos)
├── db.sqlite3              # Development database
├── requirements.txt        # Python dependencies
├── manage.py
└── README.md
```

---

## Data Models

### `accounts` — `Profile`
Extends Django's built-in `User` via a `OneToOneField`.

| Field | Type | Notes |
|---|---|---|
| `user` | OneToOneField(User) | Linked Django user |
| `phone` | CharField | Optional phone number |
| `address` | TextField | Optional address |
| `is_admin_profile` | BooleanField | Flags dashboard access (separate from `is_staff`) |
| `created_at` | DateTimeField | Auto-set on creation |

---

### `cars` — `Brand`

| Field | Type | Notes |
|---|---|---|
| `name` | CharField | Unique brand name |
| `logo` | ImageField | Optional logo, stored in `media/brands/` |
| `created_at` | DateTimeField | Auto-set on creation |

### `cars` — `Car`

| Field | Type | Notes |
|---|---|---|
| `brand` | ForeignKey(Brand) | Cascades on brand deletion |
| `name` | CharField | Model name (e.g. "5 Series") |
| `category` | CharField | `small` / `premium` / `large` |
| `price_per_day` | DecimalField | Rental rate |
| `transmission` | CharField | `automatic` / `manual` |
| `fuel_type` | CharField | `petrol` / `diesel` / `hybrid` / `electric` |
| `seats` | PositiveSmallIntegerField | Defaults to 4 |
| `description` | TextField | Optional long description |
| `image` | ImageField | Stored in `media/cars/` |
| `is_available` | BooleanField | Controls public listing visibility |
| `is_featured` | BooleanField | Drives "Executive Fleet" homepage section |
| `created_at` | DateTimeField | Auto-set on creation |

---

### `bookings` — `Booking`

| Field | Type | Notes |
|---|---|---|
| `user` | ForeignKey(User) | Customer who made the booking |
| `car` | ForeignKey(Car) | Vehicle booked |
| `pickup_date` | DateField | |
| `return_date` | DateField | |
| `pickup_location` | CharField | |
| `status` | CharField | `pending` → `confirmed` → `completed` / `cancelled` |
| `total_price` | DecimalField | Calculated server-side (days × price_per_day) |
| `created_at` | DateTimeField | Auto-set on creation |

---

### `testimonials` — `Testimonial`

| Field | Type | Notes |
|---|---|---|
| `user` | ForeignKey(User) | Review author |
| `message` | TextField | Review text |
| `rating` | PositiveSmallIntegerField | 1–5 stars, defaults to 5 |
| `is_active` | BooleanField | Admin can hide without deleting |
| `created_at` | DateTimeField | Auto-set on creation |

---

### `contact` — Three Models

- **`ContactQuery`** — Messages from the contact form (status: `new` / `resolved`)
- **`Subscriber`** — Newsletter signups (unique email per subscriber)
- **`ContactDetails`** — Single-row site contact info (address, phone, email, map embed)

---

### `pages` — `SiteContent`

| Field | Type | Notes |
|---|---|---|
| `page_key` | CharField | Unique slug identifier for a page section |
| `title` | CharField | Editable section title |
| `content` | TextField | Editable body copy |
| `updated_at` | DateTimeField | Auto-updated on save |

---

## URL Routes

| URL Prefix | App | Purpose |
|---|---|---|
| `/` | `pages` | Home, About, and static pages |
| `/cars/` | `cars` | Fleet listing and car detail pages |
| `/accounts/` | `accounts` | Register, login, logout, password reset, profile |
| `/bookings/` | `bookings` | Create booking, booking history |
| `/testimonials/` | `testimonials` | Submit and view testimonials |
| `/contact/` | `contact` | Contact form and newsletter subscribe |
| `/dashboard/` | `dashboard` | Staff-only admin dashboard (all CRUD) |
| `/admin/` | Django Admin | Built-in Django admin site |

### Key Named URL Patterns

| Name | Path | Notes |
|---|---|---|
| `home` | `/` | Default redirect after login/logout |
| `login` | `/accounts/login/` | `LOGIN_URL` setting |
| `register` | `/accounts/register/` | |
| `profile` | `/accounts/profile/` | Requires login |
| `change_password` | `/accounts/change-password/` | User-facing |
| `booking_history` | `/bookings/history/` | Requires login |
| `admin_dashboard` | `/dashboard/` | Requires `is_staff` |
| `admin_car_list` | `/dashboard/cars/` | Requires `is_staff` |
| `admin_booking_list` | `/dashboard/bookings/` | Requires `is_staff` |

---

## Getting Started

### Prerequisites
- Python 3.10+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Ikedi-21/A-car-Rental-System.git
cd A-car-Rental-System
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

> The core runtime packages are **Django 6.1.1**, **Pillow** (image handling), and **WhiteNoise** (static files serving).

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

This account will have access to both `/admin/` and the custom `/dashboard/`.

### 6. (Optional) Load Sample Data

```bash
python manage.py loaddata <fixture_name>.json
```

---

## Running the Project

```bash
python manage.py runserver
```

The app will be available at **http://127.0.0.1:8000/**

| URL | Description |
|---|---|
| `http://127.0.0.1:8000/` | Public homepage |
| `http://127.0.0.1:8000/cars/` | Fleet browsing |
| `http://127.0.0.1:8000/accounts/login/` | Customer login |
| `http://127.0.0.1:8000/dashboard/` | Admin dashboard (staff only) |
| `http://127.0.0.1:8000/admin/` | Django admin interface |

---

## Admin Dashboard

The custom dashboard at `/dashboard/` is accessible only to users with `is_staff = True`. It provides a purpose-built UI separate from Django's generic `/admin/` panel.

### Accessing the Dashboard
1. Log in with a staff / superuser account
2. Navigate to `http://127.0.0.1:8000/dashboard/`

### Dashboard Sections

| Section | URL | Actions |
|---|---|---|
| **Overview** | `/dashboard/` | Stats: users, bookings, subscribers, new queries |
| **Brands** | `/dashboard/brands/` | List, Add, Edit, Delete |
| **Fleet (Cars)** | `/dashboard/cars/` | List, Add, Edit, Delete |
| **Bookings** | `/dashboard/bookings/` | List, Update Status |
| **Users** | `/dashboard/users/` | List view |
| **Testimonials** | `/dashboard/testimonials/` | List, Toggle active/inactive |
| **Contact Queries** | `/dashboard/queries/` | List, Mark as Resolved |
| **Subscribers** | `/dashboard/subscribers/` | List, Delete |
| **Site Content** | `/dashboard/content/` | Edit page content by key |
| **Contact Details** | `/dashboard/contact-details/` | Edit site contact info |
| **Change Password** | `/dashboard/change-password/` | Admin password update |

---

## User Roles

| Role | Access | How to Set |
|---|---|---|
| **Anonymous** | Browse cars, contact form, newsletter signup | Default (not logged in) |
| **Registered Customer** | + Booking, booking history, profile, testimonials | Register at `/accounts/register/` |
| **Staff / Admin** | + Full dashboard access | Set `is_staff = True` via Django admin or `createsuperuser` |

---

## Configuration

Key settings in `core/settings.py`:

| Setting | Value | Notes |
|---|---|---|
| `DEBUG` | `True` | **Must be `False` in production** |
| `ALLOWED_HOSTS` | `localhost`, `127.0.0.1` | Add your domain for production |
| `DATABASES` | SQLite3 | Swap to PostgreSQL for production |
| `MEDIA_URL` | `/media/` | Served by Django in DEBUG mode only |
| `LOGIN_REDIRECT_URL` | `home` | Post-login landing page |
| `LOGOUT_REDIRECT_URL` | `home` | Post-logout landing page |
| `DEFAULT_FROM_EMAIL` | `noreply@driftwoodmotors.com` | Sender for password reset emails |
| `EMAIL_BACKEND` | `console.EmailBackend` | Prints emails to terminal (dev only) |

> **Security Warning:** The `SECRET_KEY` in `settings.py` is hardcoded for development. Before deploying, move it to an environment variable using `python-decouple` (already in `requirements.txt`).

### Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Move `SECRET_KEY` to an environment variable
- [ ] Add production domain to `ALLOWED_HOSTS`
- [ ] Configure a real SMTP email backend
- [ ] Switch database to PostgreSQL
- [ ] Run `python manage.py collectstatic`
- [ ] Serve media files via a CDN or dedicated file server

---

## Car Filtering & Sorting

The fleet listing page (`/cars/`) supports comprehensive querystring-based filtering:

**Filters (multi-select where applicable):**
- Category: Small / Premium / Large
- Brand
- Fuel Type: Petrol / Diesel / Hybrid / Electric
- Transmission: Automatic / Manual
- Min / Max price per day

**Sorting:**
- Price: Low to High (default)
- Price: High to Low
- Newest first

Results are paginated at **9 cars per page** (3×3 grid on desktop).

---

## Booking Logic

- Total price is recalculated **server-side** as `days × price_per_day` on every booking submission — client-side JS totals are display-only and cannot be tampered with.
- Validation enforces `return_date > pickup_date`.
- New bookings default to `pending`. Admins update the status to `confirmed`, `completed`, or `cancelled` from `/dashboard/bookings/`.

---

*Built as a Semester 4 academic project.*
