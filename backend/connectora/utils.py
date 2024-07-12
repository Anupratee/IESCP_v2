CLOUD_NAME = "daxlzqjke"
API_KEY = "423476535432448"
API_SECRET = "uqVIryJIZB5gB9uBUm3Qhy4LJ1o"

DEFAULT_SPONSOR_IMAGE = "https://asset.cloudinary.com/daxlzqjke/9701f4b015c6c77da93853c41637e490"
DEFAULT_INFLUENCER_IMAGE = "https://asset.cloudinary.com/daxlzqjke/33367be5396809a2507a886857d18e46"
ADMIN_IMAGE = "https://asset.cloudinary.com/daxlzqjke/d42e0c19cc6bd13e7613da16521303df"

def create_admin():
    from connectora.models import db, bcrypt, User
    email = "admin@connectora.com"
    password = "admin"
    name = "Admin"
    role = "admin"
    image = ADMIN_IMAGE
    description = "admin"
    location = "India"

    admin = User(email = email,
                 password = password,
                 name = name,
                 role = role,
                 image = image,
                 description = description,
                 location = location)
    
    try:
        db.session.add(admin)
        db.session.commit()
        print("admin added")
    except Exception as e:
        db.session.rollback()
        print("error:", e)



