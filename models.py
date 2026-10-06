"""
models.py — lightweight data layer for OKWebStudio's admin-editable content.

Uses Python's built-in sqlite3 module only (no extra dependency to install).
Everything the admin dashboard manages — projects, testimonials and website
enquiries — lives in one small SQLite database at instance/okwebstudio.db.
That folder is already covered by .gitignore, so the database never gets
committed; it's created (and seeded with the site's current content) the
first time the app runs.
"""

import os
import sqlite3
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "okwebstudio.db")


def get_db():
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _row_to_dict(row):
    if row is None:
        return None
    d = dict(row)
    for bool_field in ("featured", "is_read"):
        if bool_field in d:
            d[bool_field] = bool(d[bool_field])
    return d


def _rows_to_dicts(rows):
    return [_row_to_dict(r) for r in rows]


# ---------------------------------------------------------------
# Setup
# ---------------------------------------------------------------

def init_db():
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            title            TEXT NOT NULL,
            category         TEXT NOT NULL DEFAULT '',
            description      TEXT NOT NULL DEFAULT '',
            image_filename   TEXT,
            placeholder_icon TEXT NOT NULL DEFAULT '🖥️',
            link_mode        TEXT NOT NULL DEFAULT 'none',
            project_url      TEXT,
            admin_url        TEXT,
            visit_url        TEXT,
            featured         INTEGER NOT NULL DEFAULT 0,
            sort_order       INTEGER NOT NULL DEFAULT 0,
            created_at       TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS testimonials (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name  TEXT NOT NULL,
            client_role  TEXT NOT NULL DEFAULT '',
            quote        TEXT NOT NULL,
            rating       INTEGER NOT NULL DEFAULT 5 CHECK(rating BETWEEN 1 AND 5),
            sort_order   INTEGER NOT NULL DEFAULT 0,
            created_at   TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS enquiries (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            email        TEXT NOT NULL,
            project_type TEXT NOT NULL DEFAULT '',
            message      TEXT NOT NULL,
            is_read      INTEGER NOT NULL DEFAULT 0,
            created_at   TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


def seed_if_empty():
    """Populate the database with the site's current live content, but only
    the first time it runs (so nothing is duplicated on every restart)."""
    conn = get_db()

    project_count = conn.execute("SELECT COUNT(*) AS c FROM projects").fetchone()["c"]
    if project_count == 0:
        now = _now()
        projects = [
            dict(title="BrightHeaven International School", category="School Portal",
                 description="A modern school management and student portal designed for "
                              "administrators, staff and students.",
                 image_filename="project1.jpg", placeholder_icon="🎓", link_mode="dual",
                 project_url=None,
                 admin_url="https://brightheavenschoolportal.pythonanywhere.com/admin/dashboard",
                 visit_url="https://brightheavenschoolportal.pythonanywhere.com/",
                 featured=1, sort_order=1),
            dict(title="Globe-Care Services Ltd", category="Security Website",
                 description="A professional security services website designed to establish "
                              "trust, showcase services, and provide customers with an easy way "
                              "to get in touch.",
                 image_filename="project2.jpg", placeholder_icon="🛡️", link_mode="single",
                 project_url="https://globe-care.onrender.com/", admin_url=None, visit_url=None,
                 featured=1, sort_order=2),
            dict(title="Creative Portfolio", category="Portfolio Websites",
                 description="A modern portfolio website designed to showcase creative work "
                              "through a clean and engaging digital experience.",
                 image_filename=None, placeholder_icon="🎨", link_mode="none",
                 project_url=None, admin_url=None, visit_url=None,
                 featured=1, sort_order=3),
            dict(title="DonBrands Boutique", category="Fashion Store",
                 description="A responsive fashion e-commerce website designed to showcase "
                              "products and provide customers with a smooth online shopping "
                              "experience.",
                 image_filename="project4.jpg", placeholder_icon="👗", link_mode="single",
                 project_url="https://D0NBrandsboutique.pythonanywhere.com/",
                 admin_url=None, visit_url=None,
                 featured=1, sort_order=4),
            dict(title="Velora Grands Hotel", category="Hotel Websites",
                 description="A modern hotel website designed to showcase rooms, amenities, "
                              "and the overall guest experience.",
                 image_filename=None, placeholder_icon="🏨", link_mode="none",
                 project_url=None, admin_url=None, visit_url=None,
                 featured=0, sort_order=5),
            dict(title="Choply Restaurant", category="Restaurant Websites",
                 description="A modern restaurant website built to showcase the menu and make "
                              "it easy for guests to get in touch.",
                 image_filename=None, placeholder_icon="🍽️", link_mode="none",
                 project_url=None, admin_url=None, visit_url=None,
                 featured=0, sort_order=6),
        ]
        for p in projects:
            conn.execute(
                """INSERT INTO projects
                   (title, category, description, image_filename, placeholder_icon,
                    link_mode, project_url, admin_url, visit_url, featured, sort_order, created_at)
                   VALUES (:title, :category, :description, :image_filename, :placeholder_icon,
                           :link_mode, :project_url, :admin_url, :visit_url, :featured, :sort_order, :created_at)""",
                {**p, "created_at": now},
            )

    testimonial_count = conn.execute("SELECT COUNT(*) AS c FROM testimonials").fetchone()["c"]
    if testimonial_count == 0:
        now = _now()
        testimonials = [
            dict(client_name="BrightHeaven International School", client_role="School Management",
                 quote="OKWebStudio delivered a modern school portal that completely "
                       "transformed our online presence. The design is beautiful, responsive "
                       "and very easy to use.",
                 rating=5, sort_order=1),
            dict(client_name="Divine Furniture Ltd.", client_role="Business Owner",
                 quote="Communication was excellent from start to finish. They delivered "
                       "exactly what our business needed.",
                 rating=4, sort_order=2),
            dict(client_name="Nova Digital", client_role="Marketing Agency",
                 quote="Fast delivery, clean code and an amazing design. We have already "
                       "recommended OKWebStudio to other businesses.",
                 rating=5, sort_order=3),
        ]
        for t in testimonials:
            conn.execute(
                """INSERT INTO testimonials (client_name, client_role, quote, rating, sort_order, created_at)
                   VALUES (:client_name, :client_role, :quote, :rating, :sort_order, :created_at)""",
                {**t, "created_at": now},
            )

    conn.commit()
    conn.close()


# ---------------------------------------------------------------
# Projects
# ---------------------------------------------------------------

def get_all_projects():
    conn = get_db()
    rows = conn.execute("SELECT * FROM projects ORDER BY sort_order ASC, id ASC").fetchall()
    conn.close()
    return _rows_to_dicts(rows)


def get_featured_projects(limit=4):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM projects WHERE featured = 1 ORDER BY sort_order ASC, id ASC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return _rows_to_dicts(rows)


def count_projects():
    conn = get_db()
    c = conn.execute("SELECT COUNT(*) AS c FROM projects").fetchone()["c"]
    conn.close()
    return c


def count_featured_projects():
    conn = get_db()
    c = conn.execute("SELECT COUNT(*) AS c FROM projects WHERE featured = 1").fetchone()["c"]
    conn.close()
    return c


def get_project(project_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    conn.close()
    return _row_to_dict(row)


def create_project(**fields):
    conn = get_db()
    max_order = conn.execute("SELECT COALESCE(MAX(sort_order), 0) AS m FROM projects").fetchone()["m"]
    fields.setdefault("sort_order", max_order + 1)
    fields.setdefault("created_at", _now())
    fields.setdefault("placeholder_icon", "🖥️")
    conn.execute(
        """INSERT INTO projects
           (title, category, description, image_filename, placeholder_icon,
            link_mode, project_url, admin_url, visit_url, featured, sort_order, created_at)
           VALUES (:title, :category, :description, :image_filename, :placeholder_icon,
                   :link_mode, :project_url, :admin_url, :visit_url, :featured, :sort_order, :created_at)""",
        fields,
    )
    conn.commit()
    new_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    conn.close()
    return new_id


def update_project(project_id, **fields):
    fields["id"] = project_id
    conn = get_db()
    conn.execute(
        """UPDATE projects SET
             title=:title, category=:category, description=:description,
             image_filename=:image_filename, placeholder_icon=:placeholder_icon,
             link_mode=:link_mode, project_url=:project_url,
             admin_url=:admin_url, visit_url=:visit_url, featured=:featured
           WHERE id=:id""",
        fields,
    )
    conn.commit()
    conn.close()


def delete_project(project_id):
    conn = get_db()
    row = conn.execute("SELECT image_filename FROM projects WHERE id=?", (project_id,)).fetchone()
    conn.execute("DELETE FROM projects WHERE id=?", (project_id,))
    conn.commit()
    conn.close()
    return row["image_filename"] if row else None


def toggle_project_featured(project_id):
    conn = get_db()
    conn.execute("UPDATE projects SET featured = 1 - featured WHERE id=?", (project_id,))
    conn.commit()
    conn.close()


def move_project(project_id, direction):
    conn = get_db()
    current = conn.execute("SELECT id, sort_order FROM projects WHERE id=?", (project_id,)).fetchone()
    if not current:
        conn.close()
        return
    if direction == "up":
        neighbor = conn.execute(
            "SELECT id, sort_order FROM projects WHERE sort_order < ? ORDER BY sort_order DESC LIMIT 1",
            (current["sort_order"],),
        ).fetchone()
    else:
        neighbor = conn.execute(
            "SELECT id, sort_order FROM projects WHERE sort_order > ? ORDER BY sort_order ASC LIMIT 1",
            (current["sort_order"],),
        ).fetchone()
    if neighbor:
        conn.execute("UPDATE projects SET sort_order=? WHERE id=?", (neighbor["sort_order"], current["id"]))
        conn.execute("UPDATE projects SET sort_order=? WHERE id=?", (current["sort_order"], neighbor["id"]))
        conn.commit()
    conn.close()


# ---------------------------------------------------------------
# Testimonials
# ---------------------------------------------------------------

def get_all_testimonials():
    conn = get_db()
    rows = conn.execute("SELECT * FROM testimonials ORDER BY sort_order ASC, id ASC").fetchall()
    conn.close()
    return _rows_to_dicts(rows)


def count_testimonials():
    conn = get_db()
    c = conn.execute("SELECT COUNT(*) AS c FROM testimonials").fetchone()["c"]
    conn.close()
    return c


def get_testimonial(testimonial_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM testimonials WHERE id=?", (testimonial_id,)).fetchone()
    conn.close()
    return _row_to_dict(row)


def create_testimonial(**fields):
    conn = get_db()
    max_order = conn.execute("SELECT COALESCE(MAX(sort_order), 0) AS m FROM testimonials").fetchone()["m"]
    fields.setdefault("sort_order", max_order + 1)
    fields.setdefault("created_at", _now())
    conn.execute(
        """INSERT INTO testimonials (client_name, client_role, quote, rating, sort_order, created_at)
           VALUES (:client_name, :client_role, :quote, :rating, :sort_order, :created_at)""",
        fields,
    )
    conn.commit()
    conn.close()


def update_testimonial(testimonial_id, **fields):
    fields["id"] = testimonial_id
    conn = get_db()
    conn.execute(
        """UPDATE testimonials SET client_name=:client_name, client_role=:client_role,
             quote=:quote, rating=:rating WHERE id=:id""",
        fields,
    )
    conn.commit()
    conn.close()


def delete_testimonial(testimonial_id):
    conn = get_db()
    conn.execute("DELETE FROM testimonials WHERE id=?", (testimonial_id,))
    conn.commit()
    conn.close()


def move_testimonial(testimonial_id, direction):
    conn = get_db()
    current = conn.execute("SELECT id, sort_order FROM testimonials WHERE id=?", (testimonial_id,)).fetchone()
    if not current:
        conn.close()
        return
    if direction == "up":
        neighbor = conn.execute(
            "SELECT id, sort_order FROM testimonials WHERE sort_order < ? ORDER BY sort_order DESC LIMIT 1",
            (current["sort_order"],),
        ).fetchone()
    else:
        neighbor = conn.execute(
            "SELECT id, sort_order FROM testimonials WHERE sort_order > ? ORDER BY sort_order ASC LIMIT 1",
            (current["sort_order"],),
        ).fetchone()
    if neighbor:
        conn.execute("UPDATE testimonials SET sort_order=? WHERE id=?", (neighbor["sort_order"], current["id"]))
        conn.execute("UPDATE testimonials SET sort_order=? WHERE id=?", (current["sort_order"], neighbor["id"]))
        conn.commit()
    conn.close()


# ---------------------------------------------------------------
# Enquiries (contact form submissions)
# ---------------------------------------------------------------

def create_enquiry(name, email, project_type, message):
    conn = get_db()
    conn.execute(
        """INSERT INTO enquiries (name, email, project_type, message, is_read, created_at)
           VALUES (?, ?, ?, ?, 0, ?)""",
        (name, email, project_type, message, _now()),
    )
    conn.commit()
    conn.close()


def get_all_enquiries():
    conn = get_db()
    rows = conn.execute("SELECT * FROM enquiries ORDER BY created_at DESC, id DESC").fetchall()
    conn.close()
    return _rows_to_dicts(rows)


def count_enquiries():
    conn = get_db()
    c = conn.execute("SELECT COUNT(*) AS c FROM enquiries").fetchone()["c"]
    conn.close()
    return c


def count_unread_enquiries():
    conn = get_db()
    c = conn.execute("SELECT COUNT(*) AS c FROM enquiries WHERE is_read = 0").fetchone()["c"]
    conn.close()
    return c


def toggle_enquiry_read(enquiry_id):
    conn = get_db()
    conn.execute("UPDATE enquiries SET is_read = 1 - is_read WHERE id=?", (enquiry_id,))
    conn.commit()
    conn.close()


def delete_enquiry(enquiry_id):
    conn = get_db()
    conn.execute("DELETE FROM enquiries WHERE id=?", (enquiry_id,))
    conn.commit()
    conn.close()
