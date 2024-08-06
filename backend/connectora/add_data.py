import logging
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from models import db, User, users_schema, Influencer, influencers_schema, bcrypt, Request, influencer_ads_association
from models import Sponsor, sponsors_schema, Campaign, campaigns_schema, Ad, ads_schema, Category, categories_schema
from utils import DEFAULT_INFLUENCER_IMAGE, DEFAULT_SPONSOR_IMAGE, API_KEY, API_SECRET, CLOUD_NAME

def add_influencers():
    email = "madeleine_white@connectora.com"
    password = "madeleine_white"
    name = "Madeleine White"
    role = "influencer"
    description = "I am an influencer known for her fashion, beauty, and lifestyle content. I often shares styling tips, beauty routines, and glimpses into my personal life."
    location = "Maharashtra"
    flag = False
    category_id = 2
    followers = 3,450,000
    platforms = "Instagram, YouTube"
    image_path = "backend/connectora/static/madeleine.jpg"
    uploaded_image = cloudinary.uploader.upload(image_path, 
                                                api_key = API_KEY,
                                                api_secret = API_SECRET,
                                                cloud_name = CLOUD_NAME)
    image_url = uploaded_image["secure_url"]

    new_user = User(email = email, 
                    password = password,
                    name = name,
                    role = role,
                    image = image_url,
                    description = description,
                    location = location,
                    flag = flag)
    
    try:
        db.session.add(new_user)
        print("madeleine user added")
    except Exception as e:
        db.session.rollback    
        logging.error(f'Error during setup: {e}')

    new_influencer = Influencer(user_id = new_user.id,
                                category_id = category_id,
                                followers = followers,
                                platforms = platforms)
    
    try:
        db.session.add(new_influencer)
        print("madeleine influencer added")
    except Exception as e:
        db.session.rollback    
        logging.error(f'Error during setup: {e}')


add_influencers()
