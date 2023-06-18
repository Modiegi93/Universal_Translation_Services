#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON: status:
    OK (see example)"""

from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from translator import storage
from translator.text import TextTranslation
from translator.document import DocumentTranslation
from translator.image import ImageTranslation
from translator.website import WebsiteTranslation
from translator.feedback import FeedBack
from translator.user import User
from translator.language import LanguageSupport
from translator.detect_language import DetectLanguage

@app_views.route('/status', strict_slashes=False)
def _status():
    """return a JSON file with Status: OK"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def stats():
    """Create an endpoint that retrieves the number of each objects by type"""
    countTextTranslations = storage.count("TextTranslation")
    countDocumentTranslations = storage.count("DocumentTranslation")
    countImageTranslations = storage.count("ImageTranslation")
    countWebsiteTranslations = storage.count("WebsiteTranslation")
    countFeedBack = storage.count("FeedBack")
    countLanguageSupported = storage.count("LanguageSupport")
    countDetectedLanguage = storage.count("DetectLanguage")
    countUsers = storage.count("User")
    
    return jsonify(text_translations=countTextTranslations,
                   document_translations=countDocumentTranslations,
                   image_translations=countImageTranslations,
                   website_translations=countWebsiteTranslations,
                   detect_languages=countDetectedLanguage,
                   languages_supported=countLanguageSupported,
                   feedbacks=countFeedBack,
                   users=countUsers)
