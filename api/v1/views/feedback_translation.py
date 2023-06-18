#!/usr/bin/python3

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from translator import storage
from translator.feedback import FeedBack
from translator.user import User
from translator.text import TextTranslation
from translator.document import DocumentTranslation
from translator.image import ImageTranslation
from translator.website import WebsiteTranslation
from translator.translation_model import TranslationModel,Base

@app_views.route('/users/<user_id>/feedbacks', methods=['GET'],
                 strict_slashes=False)
def all_feedbacks(user_id):
    """get list of all feedbacks"""
    all_feedbacks = []
    if not storage.get('User', user_id):
        abort(404)
    for feedback in storage.all('FeedBack').values():
        if user_id == feedback.to_dict()['user_id']:
            all_feedbacks.append(feedback.to_dict())
    return jsonify(all_feedbacks)


@app_views.route('/feedbacks/<feedback_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_feedback(feedback_id):
    """ get a single Feedback """
    feedback = storage.get('FeedBack', feedback_id)
    if feedback:
        return feedback.to_dict()
    abort(404)


@app_views.route('/feedbacks/<feedback_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_feedback(feedback_id):
    """ delete a Feedback """
    feedback = storage.get('FeedBack', feedback_id)
    if feedback:
        storage.delete(feedback)
        storage.save()
        return {}
    abort(404)


@app_views.route('/users/<user_id>/feedbacks', methods=['POST'],
                 strict_slashes=False)
def create_feedback(user_id):
    """ create feedback """
    feedback_data = request.get_json()
    if not feedback_data:
        abort(400, {'error': 'Not a JSON'})
    if 'text' not in feedback_data:
        abort(400, {'error':'Missing text'})

    user = storage.get('User', user_id)
    if not user:
        abort(404)
    
    feedback = FeedBack()
    feedback.user_id = user.id
    feedback.text = feedback_data['text']
    storage.new(feedback)
    storage.save()

    return jsonify(feedback.to_dict()), 201

@app_views.route('/feedbacks/<feedback_id>', methods=['PUT'],
                 strict_slashes=False)
def update_feedback(feedback_id):
    """ update a Feedback """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_feedback = storage.get('FeedBack', feedback_id)
    if not my_feedback:
        abort(404)
    for key, value in update_attr.items():
        if key not in ['id', 'user_id', 'translation_id', 'created_at',
                       'updated_at']:
            setattr(my_feedback, key, value)
    storage.save()
    return my_feedback.to_dict()
