from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import hashlib

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
#    return "<h1>Test</h1>"
    if request.method == "POST":
        note = request.form.get("note")
        print(note)
        note = note.replace("\n", "<br \>")
        note_title = request.form.get("note_title")
        if note_title == "":
            note_title = "Untitled"

        if len(note) < 1:
            flash("Note is too short", category="error")
        else:
            new_note = Note(data=note, note_title=note_title, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added", category="success")

    return render_template("home.html", user=current_user)

# @views.route(note.note_title+hashlib.sha256(note.encode()), methods=["GET"])
# /viewnote/<noteid>
@views.route("/viewnote/<noteid>", methods=["GET"])
def viewnote(noteid):
    # return f'{ noteid } is the note id'
    note = Note.query.get(noteid)
    return render_template("note.html", user=current_user, note=note)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})