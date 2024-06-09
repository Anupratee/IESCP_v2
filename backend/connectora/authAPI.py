from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies

authAPI = Blueprint('authAPI', __name__)

@authAPI.route('/', methods = ['GET'])
def login():
    return 'hello'