# OKWebStudio — Admin Dashboard Guide

## Logging in

Visit `/admin/login` on your site (e.g. `https://okwebstudi0.pythonanywhere.com/admin/login`).

Built-in default login (works with no setup — change it before going live, see below):
- Username: `admin`
- Password: `okwebstudio2026`

## Changing your login

1. In the project folder, copy `.env.example` to a new file named `.env` (if you don't already have one).
2. Set your own values:
   ```
   ADMIN_USERNAME=your-username
   ADMIN_PASSWORD=a-strong-password
   ```
3. Restart the app (on PythonAnywhere: reload the web app from the Web tab) for the change to take effect.

Until you set these, the dashboard keeps working with the built-in defaults above — the login page will show a small reminder banner about this so it's not forgotten.

## What you can do from the dashboard

- **Dashboard** — quick stats, plus your most recent enquiries at a glance.
- **Featured Projects** — add, edit, delete and reorder projects, and choose which ones are "Featured" (the first 4 featured projects show on the homepage; every project — featured or not — always shows on the public **View All Projects** page).
  For each project you choose how visitors interact with it:
  - **Coming Soon** — no link yet, just the card.
  - **Single Link** — a "View Project" button that opens the live site directly.
  - **Two Links** — a popup with "Admin's View" and "Visit Site" buttons (like the BrightHeaven project already on the site).
- **Testimonials** — add, edit, delete and reorder client testimonials, with a clickable star rating.
- **Enquiries** — every message submitted through the site's contact form appears here instead of being emailed. Unread ones are highlighted; mark them read/unread or delete once handled.

## Where everything is stored

Projects, testimonials and enquiries live in a small database file created automatically at `instance/okwebstudio.db` the first time the app runs. It's excluded from git, so future code updates never touch your content — only the admin dashboard does.

Uploaded project photos are saved in `static/images/projects/`.

**PythonAnywhere note:** both the database and uploaded images are ordinary files, so they persist on PythonAnywhere's storage exactly like the rest of the site — nothing extra to configure. If you ever move to a host with a *temporary* filesystem (e.g. a default Heroku dyno), the database would reset on every deploy — worth remembering if you switch hosts.

## Email is no longer used for enquiries

The contact form used to send new enquiries to your Gmail address via Flask-Mail. That's been replaced: messages now save straight into the Enquiries page above — faster (no email round-trip) and everything lives in one dashboard. `Flask-Mail` has been removed from `requirements.txt` since it's no longer used anywhere.
