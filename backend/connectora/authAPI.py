from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from connectora.models import db, User, user_schema, users_schema, Influencer, influencers_schema 
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
from connectora.utils import DEFAULT_INFLUENCER_IMAGE, DEFAULT_SPONSOR_IMAGE


authAPI = Blueprint("authAPI", __name__)

@authAPI.route("/", methods = ["GET"])
def login():
    return "hello"

@authAPI.route("/users", methods = ['GET'])
def get_all_users():
    users = User.query.all()
    users_output = users_schema.dump(users)

    return jsonify({"users": users_output}), 200

@authAPI.route("/influencers", methods = ['GET'])
def get_all_influencers():
    influencers = Influencer.query.all()
    influencers_output = influencers_schema.dump(influencers)

    return jsonify({"influencers": influencers_output}), 200

@authAPI.route("/sponsors", methods = ['GET'])
def get_all_sponsors():
    sponsors = Sponsor.query.all()
    sponsors_output = sponsors_schema.dump(sponsors)

    return jsonify({"sponsors": sponsors_output}), 200

@authAPI.route("/campaigns", methods = ['GET'])
def get_all_campaigns():
    campaigns = Campaign.query.all()
    campaigns_output = campaigns_schema.dump(campaigns)

    return jsonify({"campaigns": campaigns_output}), 200

@authAPI.route("/ads", methods = ['GET'])
def get_all_ads():
    ads = Ad.query.all()
    ads_output = ads_schema.dump(ads)

    return jsonify({"ads": ads_output}), 200

@authAPI.route("/categories", methods = ['GET'])
def get_all_categories():
    categories = Category.query.all()
    categories_output = categories_schema.dump(categories)

    return jsonify({"categories": categories_output}), 200



#login and sign up functions now

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
                    location = location)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409
    
    user = User.query.filter_by(email = email).first()

    user_id = user.id
    category_id = 1
    socials = ""
    followers = ""
    rates = ""
    platforms = ""

    new_influencer = Influencer(user_id = user_id,
                                category_id = category_id,
                                socials = socials,
                                followers = followers,
                                rates = rates,
                                platforms = platforms)
    
    try:
        db.session.add(new_influencer)
        db.session.commit()
        return jsonify({'message':'Influencer added successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409




