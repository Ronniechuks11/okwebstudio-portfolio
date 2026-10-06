import os

from flask import (
    Flask, render_template, request, jsonify, send_from_directory,
    redirect, url_for, flash,
)
from dotenv import load_dotenv

import models

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB upload limit for project images

HOMEPAGE_PROJECT_LIMIT = 4

# Create the database (if it doesn't exist yet) and seed it with the site's
# current content the very first time the app runs.
models.init_db()
models.seed_if_empty()

from admin import admin_bp  # noqa: E402 (imported after db setup, before it's registered)
app.register_blueprint(admin_bp)


@app.route('/googlee3424370c0985eb2.html')
def google_verification():
    return send_from_directory('.', 'googlee3424370c0985eb2.html')


@app.route("/")
def home():
    featured_projects = models.get_featured_projects(limit=HOMEPAGE_PROJECT_LIMIT)
    total_projects = models.count_projects()
    testimonials = models.get_all_testimonials()
    return render_template(
        "index.html",
        featured_projects=featured_projects,
        show_view_all=total_projects > len(featured_projects),
        testimonials=testimonials,
    )


@app.route("/projects")
def all_projects():
    projects = models.get_all_projects()
    return render_template("all_projects.html", projects=projects)


@app.route("/contact", methods=["POST"])
def contact():

    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip()
    project = (request.form.get("project") or "").strip()
    message = (request.form.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({
            "success": False,
            "message": "❌ Please fill in your name, email and message."
        }), 400

    try:

        models.create_enquiry(name=name, email=email, project_type=project, message=message)

        return jsonify({
            "success": True,
            "message": "🎉 Thank you! We've received your message and will get back to you within 24 hours."
        })

    except Exception as e:

        print("ENQUIRY SAVE ERROR:", e)

        return jsonify({
            "success": False,
            "message": "❌ Sorry, something went wrong. Please try again later."
        }), 500


@app.route("/sitemap.xml")
def sitemap():

    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://okwebstudi0.pythonanywhere.com/</loc>
    </url>
</urlset>""", 200, {
        "Content-Type": "application/xml"
    }


@app.route("/robots.txt")
def robots():

    return """User-agent: *
Allow: /

Sitemap: https://okwebstudi0.pythonanywhere.com/sitemap.xml
""", 200, {
        "Content-Type": "text/plain"
    }


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(413)
def file_too_large(e):
    flash("That image is too large. Please upload a file under 8MB.", "error")
    return redirect(request.referrer or url_for("admin.dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
