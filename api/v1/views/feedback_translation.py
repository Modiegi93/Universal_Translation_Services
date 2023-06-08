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

@app_views.route('/translations/<translation_id>/feedbacks', methods=['GET'],
                 strict_slashes=False)
def all_feedbacks(translation_id):
    """get list of all feedbacks"""
     all_feedbacks = []
    if not storage.get('TextTranslation', 'DocumentTranslation',
                       'WebsiteTranslation', 'ImageTranslation',
                       'translation_id'):
        abort(404)
    for review in storage.all('FeedBack').values():
        if translation_id == feedback.to_dict()['translation_id']:
            all_feedbacks.append(feedback.to_dict())
    return jsonify(all_feedbacks)


@app_views.route('/feedback/<feedback_id>', methods=['GET'],
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


@app_views.route('/translations/<translation_id>/feedbacks', methods=['POST'],
                 strict_slashes=False)
def create_feedback(translation_id):
    """ create feedback """
    feedback_name = request.get_json()
    if not storage.get('TextTranslation', 'DocumentTranslation',
                                     'WebsiteTranslation', 'ImageTranslation',
                                     'translation_id'):
        abort(404)
    if not feedback_name:
        abort(400, {'Not a JSON'})
    elif 'user_id' not in feedback_name:
        abort(400, {'Missing user_id'})
    elif not storage.get('User', feedback_name['user_id']):
        abort(404)
    elif 'text' not in feedback_name:
        abort(400, {'Missing text'})
    feedback_name['translation_id'] = translation_id
    new_feedback = FeedBack(**feedback_name)
    storage.new(new_feedback)
    storage.save()
    return new_feedback.to_dict(), 201


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
            setattr(my_review, key, value)
    storage.save()
    return my_feedback.to_dict()
