from flask import Blueprint, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(400)
def bad_request_error(error):
    return jsonify({"message": "Bad Request", "details": str(error)}), 400

@errors.app_errorhandler(404)
def not_found_error(error):
    return jsonify({"message": "Not Found", "details": str(error)}), 404

@errors.app_errorhandler(415)
def unsupported_media_type_error(error):
    return jsonify({"message": "Unsupported Media Type", "details": str(error)}), 415

@errors.app_errorhandler(500)
def internal_server_error(error):
    return jsonify({"message": "Internal Server Error", "details": str(error)}), 500

@errors.app_errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({"message": "Validation Error", "details": error.messages}), 400

@errors.app_errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(error):
    return jsonify({"message": "Database Error", "details": str(error)}), 500

@errors.app_errorhandler(Exception)
def handle_generic_error(error):
    return jsonify({"message": "An unexpected error occurred", "details": str(error)}), 500
