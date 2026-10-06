"""
admin.py — the admin dashboard blueprint.

Everything under /admin lives here: login, the Featured Projects manager,
the testimonials manager, and the enquiries inbox that now replaces the
old "email me the contact form" flow.
"""

import hmac
import os
import uuid
from functools import wraps

from flask import (
    Blueprint, render_template, request, redirect, url_for,
    session, flash, abort,
)

import models

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ---------------------------------------------------------------
# Credentials — read from the environment (see .env.example).
# Sensible defaults are provided so the dashboard works out of the box,
# but they should be changed before the site goes live.
# ---------------------------------------------------------------
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "okwebstudio2026")
USING_DEFAULT_CREDENTIALS = not (os.getenv("ADMIN_USERNAME") and os.getenv("ADMIN_PASSWORD"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_UPLOAD_DIR = os.path.join(BASE_DIR, "static", "images", "projects")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


# ---------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@admin_bp.context_processor
def inject_sidebar_data():
    if session.get("is_admin"):
        return {"sidebar_unread_count": models.count_unread_enquiries()}
    return {}


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("is_admin"):
        return redirect(url_for("admin.dashboard"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if hmac.compare_digest(username, ADMIN_USERNAME) and hmac.compare_digest(password, ADMIN_PASSWORD):
            session.clear()
            session["is_admin"] = True
            session.permanent = True
            next_url = request.args.get("next", "")
            if next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect(url_for("admin.dashboard"))
        error = "Incorrect username or password."

    return render_template(
        "admin/login.html",
        error=error,
        using_default_credentials=USING_DEFAULT_CREDENTIALS,
    )


@admin_bp.route("/logout")
def logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin.login"))


# ---------------------------------------------------------------
# Image upload helpers
# ---------------------------------------------------------------

def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_project_image(file_storage):
    if not _allowed_file(file_storage.filename):
        raise ValueError("Please upload a PNG, JPG, WEBP or GIF image.")
    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    filename = f"proj_{uuid.uuid4().hex[:12]}.{ext}"
    os.makedirs(PROJECTS_UPLOAD_DIR, exist_ok=True)
    file_storage.save(os.path.join(PROJECTS_UPLOAD_DIR, filename))
    return filename


def delete_project_image_file(filename):
    """Only ever deletes files we generated ourselves (the proj_ prefix),
    so the original launch images can never be touched by accident."""
    if not filename or not filename.startswith("proj_"):
        return
    path = os.path.join(PROJECTS_UPLOAD_DIR, filename)
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


# ---------------------------------------------------------------
# Dashboard home
# ---------------------------------------------------------------

@admin_bp.route("/")
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    stats = {
        "total_projects": models.count_projects(),
        "featured_projects": models.count_featured_projects(),
        "total_testimonials": models.count_testimonials(),
        "total_enquiries": models.count_enquiries(),
        "unread_enquiries": models.count_unread_enquiries(),
    }
    recent_enquiries = models.get_all_enquiries()[:5]
    return render_template("admin/dashboard.html", stats=stats, recent_enquiries=recent_enquiries)


# ---------------------------------------------------------------
# Projects
# ---------------------------------------------------------------

def _normalize_url(value):
    value = (value or "").strip()
    if not value:
        return None
    if not (value.startswith("http://") or value.startswith("https://") or value.startswith("/")):
        value = "https://" + value
    return value


def _parse_project_form(form):
    title = (form.get("title") or "").strip()
    category = (form.get("category") or "").strip()
    description = (form.get("description") or "").strip()
    placeholder_icon = (form.get("placeholder_icon") or "🖥️").strip() or "🖥️"
    link_mode = form.get("link_mode") or "none"
    if link_mode not in ("none", "single", "dual"):
        link_mode = "none"
    featured = 1 if form.get("featured") == "on" else 0

    project_url = _normalize_url(form.get("project_url")) if link_mode == "single" else None
    admin_url = _normalize_url(form.get("admin_url")) if link_mode == "dual" else None
    visit_url = _normalize_url(form.get("visit_url")) if link_mode == "dual" else None

    errors = []
    if not title:
        errors.append("Please give the project a title.")
    if not category:
        errors.append("Please add a short category tag (e.g. \"School Portal\").")
    if not description:
        errors.append("Please add a description.")
    if link_mode == "single" and not project_url:
        errors.append("Please add the project link, or choose a different link option.")
    if link_mode == "dual" and (not admin_url or not visit_url):
        errors.append("Please add both the admin link and the visit-site link, or choose a different link option.")

    data = {
        "title": title, "category": category, "description": description,
        "placeholder_icon": placeholder_icon, "link_mode": link_mode,
        "project_url": project_url, "admin_url": admin_url, "visit_url": visit_url,
        "featured": featured,
    }
    return data, errors


@admin_bp.route("/projects")
@login_required
def projects_list():
    projects = models.get_all_projects()
    return render_template("admin/projects_list.html", projects=projects)


@admin_bp.route("/projects/new", methods=["GET", "POST"])
@login_required
def project_new():
    if request.method == "POST":
        data, errors = _parse_project_form(request.form)

        image_filename = None
        if not errors:
            image_file = request.files.get("image")
            if image_file and image_file.filename:
                try:
                    image_filename = save_project_image(image_file)
                except ValueError as exc:
                    errors.append(str(exc))

        if errors:
            for err in errors:
                flash(err, "error")
            return render_template("admin/project_form.html", project=data, mode="new"), 400

        data["image_filename"] = image_filename
        models.create_project(**data)
        flash(f"\u201c{data['title']}\u201d was added to Featured Projects.", "success")
        return redirect(url_for("admin.projects_list"))

    return render_template("admin/project_form.html", project=None, mode="new")


@admin_bp.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def project_edit(project_id):
    project = models.get_project(project_id)
    if not project:
        abort(404)

    if request.method == "POST":
        data, errors = _parse_project_form(request.form)
        remove_image = request.form.get("remove_image") == "on"
        new_image_filename = None

        if not errors:
            image_file = request.files.get("image")
            if image_file and image_file.filename:
                try:
                    new_image_filename = save_project_image(image_file)
                except ValueError as exc:
                    errors.append(str(exc))

        if errors:
            for err in errors:
                flash(err, "error")
            merged = {**project, **data, "id": project_id}
            return render_template("admin/project_form.html", project=merged, mode="edit"), 400

        image_filename = project["image_filename"]
        if new_image_filename:
            delete_project_image_file(project["image_filename"])
            image_filename = new_image_filename
        elif remove_image:
            delete_project_image_file(project["image_filename"])
            image_filename = None

        data["image_filename"] = image_filename
        models.update_project(project_id, **data)
        flash(f"\u201c{data['title']}\u201d was updated.", "success")
        return redirect(url_for("admin.projects_list"))

    return render_template("admin/project_form.html", project=project, mode="edit")


@admin_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
@login_required
def project_delete(project_id):
    project = models.get_project(project_id)
    if not project:
        abort(404)
    old_image = models.delete_project(project_id)
    delete_project_image_file(old_image)
    flash(f"\u201c{project['title']}\u201d was deleted.", "success")
    return redirect(url_for("admin.projects_list"))


@admin_bp.route("/projects/<int:project_id>/toggle-featured", methods=["POST"])
@login_required
def project_toggle_featured(project_id):
    if not models.get_project(project_id):
        abort(404)
    models.toggle_project_featured(project_id)
    return redirect(url_for("admin.projects_list"))


@admin_bp.route("/projects/<int:project_id>/move/<direction>", methods=["POST"])
@login_required
def project_move(project_id, direction):
    if direction not in ("up", "down"):
        abort(404)
    models.move_project(project_id, direction)
    return redirect(url_for("admin.projects_list"))


# ---------------------------------------------------------------
# Testimonials
# ---------------------------------------------------------------

def _parse_testimonial_form(form):
    client_name = (form.get("client_name") or "").strip()
    client_role = (form.get("client_role") or "").strip()
    quote = (form.get("quote") or "").strip()
    try:
        rating = int(form.get("rating", 5))
    except (TypeError, ValueError):
        rating = 5
    rating = max(1, min(5, rating))

    errors = []
    if not client_name:
        errors.append("Please add the client's name.")
    if not quote:
        errors.append("Please add the testimonial text.")

    data = {
        "client_name": client_name, "client_role": client_role,
        "quote": quote, "rating": rating,
    }
    return data, errors


@admin_bp.route("/testimonials")
@login_required
def testimonials_list():
    testimonials = models.get_all_testimonials()
    return render_template("admin/testimonials_list.html", testimonials=testimonials)


@admin_bp.route("/testimonials/new", methods=["GET", "POST"])
@login_required
def testimonial_new():
    if request.method == "POST":
        data, errors = _parse_testimonial_form(request.form)
        if errors:
            for err in errors:
                flash(err, "error")
            return render_template("admin/testimonial_form.html", testimonial=data, mode="new"), 400
        models.create_testimonial(**data)
        flash(f"Testimonial from \u201c{data['client_name']}\u201d was added.", "success")
        return redirect(url_for("admin.testimonials_list"))
    return render_template("admin/testimonial_form.html", testimonial=None, mode="new")


@admin_bp.route("/testimonials/<int:testimonial_id>/edit", methods=["GET", "POST"])
@login_required
def testimonial_edit(testimonial_id):
    testimonial = models.get_testimonial(testimonial_id)
    if not testimonial:
        abort(404)
    if request.method == "POST":
        data, errors = _parse_testimonial_form(request.form)
        if errors:
            for err in errors:
                flash(err, "error")
            merged = {**testimonial, **data, "id": testimonial_id}
            return render_template("admin/testimonial_form.html", testimonial=merged, mode="edit"), 400
        models.update_testimonial(testimonial_id, **data)
        flash("Testimonial updated.", "success")
        return redirect(url_for("admin.testimonials_list"))
    return render_template("admin/testimonial_form.html", testimonial=testimonial, mode="edit")


@admin_bp.route("/testimonials/<int:testimonial_id>/delete", methods=["POST"])
@login_required
def testimonial_delete(testimonial_id):
    if not models.get_testimonial(testimonial_id):
        abort(404)
    models.delete_testimonial(testimonial_id)
    flash("Testimonial deleted.", "success")
    return redirect(url_for("admin.testimonials_list"))


@admin_bp.route("/testimonials/<int:testimonial_id>/move/<direction>", methods=["POST"])
@login_required
def testimonial_move(testimonial_id, direction):
    if direction not in ("up", "down"):
        abort(404)
    models.move_testimonial(testimonial_id, direction)
    return redirect(url_for("admin.testimonials_list"))


# ---------------------------------------------------------------
# Enquiries (the messages that used to go to email)
# ---------------------------------------------------------------

@admin_bp.route("/enquiries")
@login_required
def enquiries_list():
    enquiries = models.get_all_enquiries()
    return render_template("admin/enquiries_list.html", enquiries=enquiries)


@admin_bp.route("/enquiries/<int:enquiry_id>/toggle-read", methods=["POST"])
@login_required
def enquiry_toggle_read(enquiry_id):
    models.toggle_enquiry_read(enquiry_id)
    return redirect(url_for("admin.enquiries_list"))


@admin_bp.route("/enquiries/<int:enquiry_id>/delete", methods=["POST"])
@login_required
def enquiry_delete(enquiry_id):
    models.delete_enquiry(enquiry_id)
    flash("Enquiry deleted.", "success")
    return redirect(url_for("admin.enquiries_list"))
