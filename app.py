from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os, io
from werkzeug.utils import secure_filename
import csv
from sqlalchemy import desc, asc
from datetime import datetime
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
db = SQLAlchemy(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Book model for the library inventory
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50))

# Define constants
DEFAULT_ROOMS_PER_PAGE = 10

# Function to get the page range for pagination
def get_page_range(current_page, total_pages, max_page_buttons=5):
    if total_pages <= max_page_buttons:
        return range(1, total_pages + 1)

    half_buttons = max_page_buttons // 2
    if current_page <= half_buttons:
        return range(1, max_page_buttons + 1)

    if current_page >= total_pages - half_buttons:
        return range(total_pages - max_page_buttons + 1, total_pages + 1)

    return range(current_page - half_buttons, current_page + half_buttons + 1)

@app.route("/")
def index():
    return redirect(url_for("rooms"))

# @app.route("/addroom", method="POST")
# def addroom():
#     if request.method == "POST":
#         try:
#             new_room = Room(
#                 id=request.form["id"],
                
#             )


@app.route("/rooms")
def rooms():
    page = request.args.get("page", 1, type=int)
    rooms_per_page = request.args.get(
        "rooms_per_page", DEFAULT_ROOMS_PER_PAGE, type=int
    )
    rooms = Room.query.order_by(asc(Room.id)).paginate(
        page=page, per_page=rooms_per_page, error_out=False
    )
    return render_template(
        "rooms.html",
        rooms=rooms,
        get_page_range=get_page_range,
        rooms_per_page=rooms_per_page,
    )

if __name__ == '__main__':
    app.secret_key = "super_secret_key"  # Change this to a random, secure key
    socketio.run(app,debug=True)