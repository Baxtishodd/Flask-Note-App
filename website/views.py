from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Contact
from . import db
import json

views = Blueprint('views', __name__)


# --- Home
@views.route('/')
def home():

    return render_template("home.html", user=current_user)



# --- Notes
@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("note.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


# --- Contacts
@views.route('/contacts', methods=['GET', 'POST'])
@login_required
def contacts():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')

        if len(first_name) < 1:
            flash('Name is too short!', category='error')
        elif len(last_name) < 1:
            flash('Surname is too short!', category='error')
        elif len(phone_number) < 1:
            flash('Phone number is too short!', category='error')
        else:
            new_contact = Contact(name=first_name, sname=last_name, pnumber=phone_number, user_id=current_user.id)
            db.session.add(new_contact)
            db.session.commit()
            flash('Contact added!', category='success')

    return render_template("contact.html", user=current_user)



@views.route('/delete-contact', methods=['POST'])
def delete_contact():
    contact = json.loads(request.data)
    contactId = contact['contactId']
    contact = Contact.query.get(contactId)
    if contact:
        if contact.user_id == current_user.id:
            db.session.delete(contact)
            db.session.commit()

    return jsonify({})
