from flask import Flask, render_template, request, flash, redirect
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "okzwebstudio"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "okzwebstudio@gmail.com"
app.config["MAIL_PASSWORD"] = "htgclzpsxpjhntai"
app.config["MAIL_PASSWORD"] = "htgclzpsxpjhntai"
mail = Mail(app)
app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

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

    mail.send(msg)

    flash("🎉 Thank you! We've received your message and will get back to you within 24 hours.")

    return redirect("/")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)