from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os, io
from werkzeug.utils import secure_filename
import csv
from sqlalchemy import desc, asc
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
db = SQLAlchemy(app)


# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/team")
def team():
    return render_template("team.html")


if __name__ == "__main__":
    app.secret_key = "super_secret_key"  # Change this to a random, secure key
    app.run(debug=True)
