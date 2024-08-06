CLOUD_NAME = "daxlzqjke"
API_KEY = "423476535432448"
API_SECRET = "uqVIryJIZB5gB9uBUm3Qhy4LJ1o"

DEFAULT_SPONSOR_IMAGE = "https://asset.cloudinary.com/daxlzqjke/9701f4b015c6c77da93853c41637e490"
DEFAULT_INFLUENCER_IMAGE = "https://asset.cloudinary.com/daxlzqjke/33367be5396809a2507a886857d18e46"
DEFAULT_CAMPAIGN_IMAGE = "https://asset.cloudinary.com/daxlzqjke/4cc07a109b2b1acf74fe22350be04ea1"
ADMIN_IMAGE = "https://asset.cloudinary.com/daxlzqjke/d42e0c19cc6bd13e7613da16521303df"

def create_admin():
    from models import db, User
    email = "admin@connectora.com"
    password = "admin"
    name = "Admin"
    role = "admin"
    image = ADMIN_IMAGE
    description = "admin"
    location = "India"
    flag = False

    admin = User(email = email,
                 password = password,
                 name = name,
                 role = role,
                 image = image,
                 description = description,
                 location = location,
                 flag = flag)
    
    db.session.add(admin)
    db.session.commit()
    print("admin added")


def create_categories():
    from models import db, Category
    new_categories = [
        Category(name = "General"),
        Category(name = "Fashion and Beauty"),
        Category(name = "Health and Fitness"),
        Category(name = "Travel"),
        Category(name = "Lifestyle"),
        Category(name = "Tech"),
        Category(name = "Food and Cooking"),
        Category(name = "Entertainment"),
        Category(name = "Education"),
        Category(name = "Art"),
        Category(name = "Business and Finance"),
        Category(name = "Gaming"),
        Category(name = "Pets"),
        Category(name = "Relationships"),
        Category(name = "Parenting"),
        Category(name = "Sports"),
        Category(name = "Music and Performing Arts"),
        Category(name = "Social Issues")
    ]

    db.session.add_all(new_categories)
    db.session.commit()
    print("categories added")
    



import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='numpy')



# from flask_caching import Cache
# cache = Cache()