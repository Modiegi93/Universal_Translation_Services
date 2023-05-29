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
    countTextTranslation = storage.count("TextTranslation")
    countDocumentTranslation = storage.count("DocumentTranslation")
    countImageTranslation = storage.count("ImageTranslation")
    countWebsiteTranslation = storage.count("WebsiteTranslation")
    countFeedBack = storage.count("FeedBack")
    countLanguageSupport = storage.count("LanguageSupport")
    countDetectLanguage = storage.count("DetectLanguage")
    countUsers = storage.count("User")
    
    return jsonify(text_translations=countTextTranslation,
                   document_translations=countDocumentTranslation,
                   image_translations=countImageTranslation,
                   website_translations=countWebsiteTranslation,
                   detect_languages=countDetectLanguage,
                   languages_supported=countLanguageSupport,
                   feedbacks=countFeedBack,
                   users=countUsers)
