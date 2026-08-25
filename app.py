from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "okzwebstudio")

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

app.config["MAIL_USERNAME"] = "okzwebstudio@gmail.com"
app.config["MAIL_PASSWORD"] = "wuajcwijqgckkhqb"
app.config["MAIL_DEFAULT_SENDER"] = "okzwebstudio@gmail.com"

mail = Mail(app)


@app.route('/googlee3424370c0985eb2.html')
def google_verification():
    return send_from_directory('.', 'googlee3424370c0985eb2.html')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():

    name = request.form.get("name")
    email = request.form.get("email")
    project = request.form.get("project")
    message = request.form.get("message")

    msg = Message(
        subject=f"New Project: {project}",
        sender=app.config["MAIL_USERNAME"],
        recipients=[app.config["MAIL_USERNAME"]]
    )

    msg.body = f"""
NEW WEBSITE ENQUIRY

--------------------------------

👤 Name:
{name}

📧 Email:
{email}

💼 Project:
{project}

📝 Message:
{message}

--------------------------------

Sent from OKWebStudio Portfolio
"""

    try:

        mail.send(msg)

        return jsonify({
            "success": True,
            "message": "🎉 Thank you! We've received your message and will get back to you within 24 hours."
        })

    except Exception as e:

        print("MAIL ERROR:", e)

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


if __name__ == "__main__":
    app.run(debug=True)
