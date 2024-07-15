from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from connectora.models import db, User, user_schema, Influencer, influencers_schema, bcrypt, sponsor_schema
from connectora.models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
from connectora.utils import DEFAULT_INFLUENCER_IMAGE, DEFAULT_SPONSOR_IMAGE, API_KEY, API_SECRET, CLOUD_NAME


sponsorsAPI = Blueprint("sponsorsAPI", __name__)

@sponsorsAPI.route("/sponsors", methods = ['GET'])
def get_all_sponsors():
    sponsors = Sponsor.query.all()
    sponsors_output = sponsors_schema.dump(sponsors)

    return jsonify({"sponsors": sponsors_output}), 200


@sponsorsAPI.route("/sponsor/<int:user_id>", methods=["GET"])
def get_sponsor_by_id(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error':'Resource not found.'}), 404
    
    if not user.role == "sponsor":
        return jsonify({"error":"User isn't an influencer"}), 400
    
    sponsor = Sponsor.query.get(user_id)
    user_output = user_schema.dump(user)
    sponsor_output = sponsor_schema.dump(sponsor)

    return jsonify({"user":user_output},{"sponsor":sponsor_output}), 200


@sponsorsAPI.route("/update_sponsor/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_sponsor(user_id):
    this_user = get_jwt_identity()
    logged_in_user = User.query.get(this_user["id"])
    if user_id != logged_in_user.id:
        return jsonify({'error':'Unauthorised access. You can only edit your own profile.'}), 403 
    
    if logged_in_user.role != "sponsor":
        return jsonify({"error":"Bad request"}), 400
    
    update_name = request.form.get("update_name")
    update_description = request.form.get("update_description")
    update_location = request.form.get("update_location")
    update_industry = request.form.get("update_industry")

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
            if cloudinary_url_info != DEFAULT_SPONSOR_IMAGE:
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

    logged_in_sponsor = Sponsor.query.filter_by(user_id = user_id).first()
    logged_in_sponsor.industry = update_industry

    try:
        db.session.commit()
        return jsonify({'message':'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'{str(e)}.'}), 409
    
