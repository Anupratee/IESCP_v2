from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

DB_NAME = "Connectora.db"

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(45), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    name = db.Column(db.String(45), nullable = False)
    role = db.Column(db.Text, nullable = False)
    image = db.Column(db.Text, nullable = False, default = "https://res.cloudinary.com/daxlzqjke/image/upload/v1707745689/cld-sample-2.jpg")
    description = db.Column(db.Text)
    location = db.Column(db.Text)
    flag = db.Column(db.Boolean)

    def __init__(self, email, password, name, role, image, description, location, flag):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.name = name
        self.role = role
        self.image = image
        self.description = description
        self.location = location
        self.flag = flag

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", 
                  "email",
                  "password",
                  "name",
                  "role",
                  "image",
                  "description",
                  "location",
                  "flag")
        
user_schema = UserSchema()
users_schema = UserSchema(many = True)


class Sponsor(db.Model):
    __tablename__="sponsors"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key = True)
    is_approved = db.Column(db.Boolean, nullable= False, default = False)
    industry = db.Column(db.Text, nullable = False, default = None)
    campaigns = db.relationship("Campaign", back_populates = "sponsors")

    def __init__(self, user_id, industry, is_approved):
        self.user_id = user_id
        self.is_approved = is_approved
        self.industry = industry

class SponsorSchema(ma.Schema):
    class Meta:
        fields = ("user_id", 
                  "is_approved",
                  "industry",
                  )
        
sponsor_schema = SponsorSchema()
sponsors_schema = SponsorSchema(many = True)


influencer_ads_association = db.Table("influencer_ads_association",
                                      db.Column("influencer_id", db.Integer, db.ForeignKey("influencers.user_id")),
                                      db.Column("ad_id", db.Integer, db.ForeignKey("ads.id")),
                                      db.Column("payment_amount", db.Integer))


class Influencer(db.Model):
    __tablename__="influencers"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key = True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable = False)
    followers = db.Column(db.Text)
    platforms = db.Column(db.Text)
    ads = db.relationship("Ad", secondary = influencer_ads_association, back_populates = "influencers")

    def __init__(self, user_id, category_id, followers, platforms):
        self.user_id = user_id
        self.category_id = category_id
        self.followers = followers
        self.platforms = platforms

class InfluencerSchema(ma.Schema):
    class Meta:
        fields = ("user_id", 
                  "category_id",
                  "followers",
                  "platforms",
                  )
               
influencer_schema = InfluencerSchema()
influencers_schema = InfluencerSchema(many = True)


class Category(db.Model):
    __tablename__="categories"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(45), nullable=False)

    def __init__(self, name):
        self.name = name

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", 
                  "name",)

category_schema = CategorySchema()
categories_schema = CategorySchema(many = True)


class Campaign(db.Model):
    __tablename__="campaigns"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("sponsors.user_id"), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable = False)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text, nullable = False, default = None)
    status = db.Column(db.Boolean) #0 is incomplete, 1 is completed
    image = db.Column(db.Text, nullable = False, default = None)
    sponsors = db.relationship("Sponsor", back_populates = "campaigns")
    ads = db.relationship("Ad", back_populates = "campaigns")

    def __init__(self, sponsor_id, category_id, name, description, status, image):
        self.sponsor_id = sponsor_id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.status = status
        self.status
        self.image = image
    
class CampaignSchema(ma.Schema):
    class Meta:
        fields = ("id", 
                  "sponsor_id",
                  "category_id",
                  "name",
                  "description",
                  "status",
                  "image")
        

campaign_schema = CampaignSchema()
campaigns_schema = CampaignSchema(many = True)


class Ad(db.Model):
    __tablename__="ads"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"), nullable = False)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text, nullable = False, default = None)
    budget = db.Column(db.Integer, nullable = False, default = None)
    status = db.Column(db.Boolean, nullable = False, default = False)
    campaigns = db.relationship("Campaign", back_populates = "ads")
    influencers = db.relationship("Influencer", secondary = influencer_ads_association, back_populates = "ads")

    def __init__(self, campaign_id, name, description, budget, status):
        self.campaign_id = campaign_id
        self.name = name
        self.description = description
        self.budget = budget
        self.status = status

class AdSchema(ma.Schema):
    class Meta:
        fields = ("id", 
                  "campaign_id",
                  "name",
                  "description",
                  "budget",
                  "status")
        

ad_schema = AdSchema()
ads_schema = AdSchema(many = True)


class Request(db.Model):
    __tablename__="requests"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencers.user_id"))
    sponsor_id = db.Column(db.Integer, db.ForeignKey("sponsors.user_id"))
    ad_id = db.Column(db.Integer, db.ForeignKey("ads.id"))
    from_who = db.Column(db.Text, nullable = False)
    payment_amount = db.Column(db.Integer, nullable=False)
    influencer = db.relationship("Influencer", backref="requests")
    sponsor = db.relationship("Sponsor", backref="requests")
    ad = db.relationship("Ad", backref="requests")

    def __init__(self, influencer_id, sponsor_id, ad_id, from_who, payment_amount):
        self.influencer_id = influencer_id
        self.sponsor_id = sponsor_id
        self.ad_id = ad_id
        self.from_who = from_who
        self.payment_amount = payment_amount

class RequestSchema(ma.Schema):
        class Meta:
            fields = ("id",
                      "influencer_id",
                      "sponsor_id",
                      "ad_id",
                      "from_who",
                      "payment_amount")   
            
request_schema = RequestSchema()
requests_schema = RequestSchema(many=True)

