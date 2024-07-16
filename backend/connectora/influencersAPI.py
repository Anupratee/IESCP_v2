from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from connectora.models import db, User, user_schema, users_schema, Influencer, influencer_schema, influencers_schema, bcrypt
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
from connectora.utils import DEFAULT_INFLUENCER_IMAGE, API_KEY, API_SECRET, CLOUD_NAME

influencersAPI = Blueprint("/influencersAPI", __name__)

@influencersAPI.route("/influencers", methods = ['GET'])
def get_all_influencers():
    influencers = Influencer.query.all()
    influencers_output = influencers_schema.dump(influencers)

    return jsonify({"influencers": influencers_output}), 200


@influencersAPI.route("/influencer/<int:user_id>", methods=["GET"])
def get_influencer_by_id(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error':'Resource not found.'}), 404
    
    if not user.role == "influencer":
        return jsonify({"error":"User isn't an influencer"}), 400
    
    influencer = Influencer.query.get(user_id)
    user_output = user_schema.dump(user)
    influencer_output = influencer_schema.dump(influencer)

    return jsonify({"user":user_output},{"influencer":influencer_output}), 200


@influencersAPI.route("/update_influencer/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_influencer(user_id):
    this_user = get_jwt_identity()
    logged_in_user = User.query.get(this_user["id"])
    if user_id != logged_in_user.id:
        return jsonify({'error':'Unauthorised access. You can only edit your own profile.'}), 403 
    
    if logged_in_user.role != "influencer":
        return jsonify({"error":"Bad request"}), 400
    
    update_name = request.form.get("update_name")
    update_description = request.form.get("update_description")
    update_location = request.form.get("update_location")
    update_followers = request.form.get("update_followers")
    update_platforms = request.form.get("update_platforms")

    update_category_name = request.form.get("update_category_name")
    if update_category_name:
        update_category = Category.query.filter_by(name = update_category_name).first()
        if not update_category:
            return jsonify({"error":"Category doesn't exist"}), 400
    
        update_category_id = update_category.id
        logged_in_influencer.category_id = update_category_id
    
    if not update_name:
            return jsonify({'error':'Required fields can\'t be empty!'}), 400
    
    image = None
    if "update_image" in request.files:
        image = request.files["update_image"]
        if not image.filename.endswith(('.jpg', '.jpeg', '.png')):
            return jsonify({'error':'Profile picture must be an image file'}), 400
        
    if image:
        cloudinary_url_info = cloudinary_url(logged_in_user.image)
        if cloudinary_url_info:
            cloudinary_public_id = cloudinary_url_info[0].split("/")[-1].split(".")[0]
            if cloudinary_url_info != DEFAULT_INFLUENCER_IMAGE:
                cloudinary.uploader.destroy(cloudinary_public_id, 
                                            invalidate=True,
                                            api_key = API_KEY, 
                                            api_secret = API_SECRET, 
                                            cloud_name = CLOUD_NAME)
                
            uploaded_image = cloudinary.uploader.upload(image, 
                                                        api_key = API_KEY, 
                                                        api_secret = API_SECRET, 
                                                        cloud_name = CLOUD_NAME)
                
            image_url = uploaded_image['secure_url']
            logged_in_user.image = image_url

    logged_in_user.name = update_name
    logged_in_user.description = update_description
    logged_in_user.location = update_location

    logged_in_influencer = Influencer.query.filter_by(user_id = user_id).first()
    logged_in_influencer.followers = update_followers
    logged_in_influencer.platforms = update_platforms

    try:
        db.session.commit()
        return jsonify({'message':'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409


@influencersAPI.route("/delete_influencer/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_influencer(user_id):
    this_user = get_jwt_identity()
    logged_in_user = User.query.get(this_user['id'])

    if user_id != logged_in_user.id:
        if logged_in_user.role != "admin" or "influencer":
            return jsonify({'error':'Unauthorised access. You can only delete your own profile.'}), 403 
        
    user = User.query.get(user_id)
    influencer = Influencer.query.get(user_id)

    if not user:
        return jsonify({'error':'Influencer not found'}), 404
    
    try:
        if user.image != DEFAULT_INFLUENCER_IMAGE:
            cloudinary_url_info = cloudinary_url(user.image)
            if cloudinary_url_info:
                cloudinary_public_id = cloudinary_url_info[0].split("/")[-1].split(".")[0]
                cloudinary.uploader.destroy(cloudinary_public_id, 
                                            invalidate=True, 
                                            api_key = API_KEY, 
                                            api_secret = API_SECRET, 
                                            cloud_name = CLOUD_NAME)
                
        db.session.delete(influencer)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message':'Influencer deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409

