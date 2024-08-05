from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from models import db, User, users_schema, Influencer, influencers_schema, bcrypt
from models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
from utils import DEFAULT_INFLUENCER_IMAGE, DEFAULT_SPONSOR_IMAGE


authAPI = Blueprint("authAPI", __name__)


@authAPI.route("/register_influencer", methods = ['POST'])
def register_influencer():
    data = request.get_json()
    #for user table
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    role = "influencer"
    image = DEFAULT_INFLUENCER_IMAGE
    description = ""
    location = data.get("location")
    flag = False

    if not email or not password or not name or not location:
        return jsonify({'error':'Required fields can\'t be empty!'}), 400
    
    existing_user = User.query.filter_by(email = email).first()

    if existing_user:
        return jsonify({'error':'Email is already registered!'}), 400

    new_user = User(email = email,
                    password = password,
                    name = name,
                    role = role,
                    image = image,
                    description = description,
                    location = location,
                    flag = flag)
    
    db.session.add(new_user)
    
    user = User.query.filter_by(email = email).first()

    user_id = user.id
    category_id = 1
    followers = ""
    platforms = ""

    new_influencer = Influencer(user_id = user_id,
                                category_id = category_id,
                                followers = followers,
                                platforms = platforms)
    
    try:
        db.session.add(new_influencer)
        db.session.commit()
        return jsonify({'message':'Influencer added successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409


@authAPI.route("/register_sponsor", methods=["POST"])
def register_sponsor():
    data = request.get_json()
    #for user table
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    role = "sponsor"
    image = DEFAULT_SPONSOR_IMAGE
    description = ""
    location = data.get("location")
    flag = False

    if not email or not password or not name or not location:
        return jsonify({'error':'Required fields can\'t be empty!'}), 400
    
    existing_user = User.query.filter_by(email = email).first()

    if existing_user:
        return jsonify({'error':'Email is already registered!'}), 400

    new_user = User(email = email,
                    password = password,
                    name = name,
                    role = role,
                    image = image,
                    description = description,
                    location = location,
                    flag = flag)
    
    db.session.add(new_user)
    
    user = User.query.filter_by(email = email).first()

    user_id = user.id
    is_approved = False
    industry = data.get("industry")

    if not industry:
        return jsonify({'error':'Required fields can\'t be empty!'}), 400

    new_sponsor = Sponsor(user_id=user_id,
                          is_approved=is_approved,
                          industry=industry)
    
    try:
        db.session.add(new_sponsor)
        db.session.commit()
        return jsonify({"message":"Sponsor added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409


@authAPI.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({'error':'Required fields can\'t be empty!'}), 400
    
    user = User.query.filter_by(email = email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error':'Invalid credentials'}), 401
    
    access_token = create_access_token(identity = {'id': user.id, 'role': user.role})

    return jsonify({"message":'Login successful!','access_token': access_token, 'role': user.role, 'id':user.id}), 200


@authAPI.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"message":"Logout successful."})
    unset_jwt_cookies(response)
    return response, 200


