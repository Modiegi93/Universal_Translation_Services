#!/usr/bin/python

import translator
import requests
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify
from flask import render_template, request, render_template
from googletrans import LANGUAGES
from translator import storage
from translator.settings import Settings
from translator.translation_model import TranslationModel, Base
from translator.text import TextTranslation
from translator.document import DocumentTranslation
from translator.image import ImageTranslation
from translator.website import WebsiteTranslation
from translator.detect_language import DetectLanguage
from translator.language import LanguageSupport
from translator.feedback import FeedBack
from translator.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
import uuid
from os import environ
from translator import storage
from translator.subsriber import Subscriber
from translator import storage
from translator.settings import Settings


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """Index"""
    return render_template('index.html', cache_id=uuid.uuid4())

@app.route('/login', strict_slashes=False)
def login():
    "User login"
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('psw')

        # Perform login validation and authentication
        user = User.storage.get(email=email).first()
        if user and user.password == password:
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'error': 'Invalid email or password'})

    return render_template('index.html', cache_id=uuid.uuid4())

# Sign up endpoint
@app.route('/sign_up', strict_slashes=False)
def signup():
    """Sign up new user"""
    if request.method == 'POST':
        full_name = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('psw')

        # Perform sign up and user registration
        user = User(full_name=full_name, email=email, password=password)
        storage.new(user)
        storage.save()

        return jsonify({'message': 'Sign up successful'})

    return render_template('index.html', cache_id=uuid.uuid4())

@app.route('/subscribe', strict_slashes=False)
def subscribe():
    email = request.form.get('email')
    daily_newsletter = True if request.form.get('daily-newsletter') else False

    # Perform subscription logic here
    subscriber = Subscriber(email=email, daily_newsletter=daily_newsletter)
    storage.new(subscriber)
    storage.save()

    # Send confirmation email
    send_confirmation_email(email)

    return render_template('subscription_success.html', email=email,
                           daily_newsletter=daily_newsletter, cache_id=uuid.uuid4())

def send_confirmation_email(email):
    msg = Message('Subscription Confirmation',
                  sender='your-email@example.com', recipients=[email])
    msg.body = 'Thank you for subscribing to our newsletter!'
    mail.send(msg)

@app.route('/logout', strict_slashes=False)
def logout():
    # Clear the session
    storage.close()
    return redirect(url_for('/'))  # Redirect to the login page

@app.route('/about_us', strict_slashes=False)
def about_us():
    return render_template('about_us.html', cache_id=uuid.uuid4())

@app.route('/translations', strict_slashes=False)
def translations():
    return render_template('translations.html', cache_id=uuid.uuid4())

@app.route('/privacy_terms', strict_slashes=False)
def privacy_terms():
    return render_template('my_account.html', cache_id=uuid.uuid4())


@app.route('/translations_history', strict_slashes=False)
def get_translations():
    """Get all translations history from storage"""
    translations = storage.all(TextTranslation, DocumentTranslation,
                                   ImageTranslation, WebsiteTranslation)

    for text_data = []
    for trans in text_translation:
        translation_entry = {
                'created_at': translation.created_at,
                'source_text': translation.input_text,
                'translated_text': translation.translated_text,
                'target_lang': translation.target_lang,
                'type': get_translation_type(translation)
        }
        translation_data.append(translation_entry)

        return render_template('translation_history.html',
                               translations=translation_data, cache_id=uuid.uuid4())


def get_translation_type(translation):
    """Get translation type"""
    if isinstance(translation, TextTranslation):
        return 'TextTranslation'
    elif isinstance(translation, WebsiteTranslation):
        return 'WebsiteTranslation'
    elif isinstance(translation, ImageTranslation):
        return 'ImageTranslation'
    elif isinstance(translation, DocumentTranslation):
        return 'DocumentTranslation'
    else:
        return 'Unknown'

# Define your settings route
@app.route('/settings', strict_slashes=False)
def settings():
    # Get the supported languages from the googletrans library
    supported_languages = {code: name for code, name in LANGUAGES.items()}

    # Render the settings template and pass the supported_languages to it
    return render_template('settings.html', supported_languages=supported_languages,
                            cache_id=uuid.uuid4())

def handle_settings():
    if request.method == 'POST':
        target_languages = request.form.get('target_languages')
        default_language = request.form.get('default_language')

        # Update the settings in the database
        settings = storage.get("Settings")
        if settings:
            settings.target_languages = target_languages
            settings.default_language = default_language
        else:
            settings = Settings(target_languages=target_languages, default_language=default_language)
            storage.new(settings)

        storage.save()

        # Save the settings to file storage
        save_settings(target_languages, default_language)

        # Render the template with the updated settings
        return render_template('settings.html', translation_settings=settings,
                                cache_id=uuid.uuid4())
    else:
        # Get the settings from the database
        settings = storage.get("Settings")

        # Render the template with the current settings
        return render_template('settings.html', translation_settings=settings,
                               cache_id=uuid.uuid4())


@app.route('/settings', strict_slashes=False)
def save_settings():
    # Retrieve the form data
    target_languages = request.form.get('target_languages')
    default_language = request.form.get('default_language')

    data = {
        'target_languages': target_languages,
                'default_language': default_language
    }
    with open('settings.json', 'w') as file:
        json.dump(data, file)



@app.route('/supported_languages', strict_slashes)
def get_supported_languages():
    supported_languages = {code: name for code, name in
                           sorted(LANGUAGES.items(), key=lambda x: x[1])}
    return jsonify(supported_languages)

@app.route('/languages', strict_slashes)
def render_language_selector():
    supported_languages = {code: name for code, name in sorted(LANGUAGES.items(), key=lambda x: x[1])}
    return render_template('languages.html', supported_languages=supported_languages,
                            cache_id=uuid.uuid4())


@app.teardown_appcontext
def close_session(exception):
    """Remove the db session or save file"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
                                                        
