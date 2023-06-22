#!/usr/bin/python

from translator import storage
from translator.settings import Settings
from translator.translation_model import TranslationModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv

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
                               translations=translation_data)


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
    return render_template('settings.html', supported_languages=supported_languages)

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
        return render_template('settings.html', translation_settings=settings)
    else:
        # Get the settings from the database
        settings = storage.get("Settings")

        # Render the template with the current settings
        return render_template('settings.html', translation_settings=settings)


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


@app.route('/payment', strict_slashes=False)
def choose_subscription

@app.teardown_appcontext
def close_session(exception):
    """Remove the db session or save file"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
