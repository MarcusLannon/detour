import os
from flask import Flask, render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename

from detour.main import main


UPLOAD_FOLDER = "temp"
ALLOWED_EXTENSIONS = {"gpx"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)


def allowed_file(filename):
    ok_ext = filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    return "." in filename and ok_ext


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print("file was sent")
        if "file" not in request.files:
            flash("No file part")
            return "no file detected"
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(full_path)
            flags = main(full_path)
            is_incidents = len(flags) > 0
            return render_template(
                "incidents.html", is_incidents=is_incidents, incidents=flags)

    return render_template("home.html")
