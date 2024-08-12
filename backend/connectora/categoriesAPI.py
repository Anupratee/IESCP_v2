from flask import Blueprint, jsonify
from models import Category, categories_schema, category_schema



categoriesAPI = Blueprint("categoriesAPI", __name__)

@categoriesAPI.route("/categories", methods = ['GET'])
def get_all_categories():
    categories = Category.query.all()
    categories_output = categories_schema.dump(categories)

    return jsonify({"categories": categories_output}), 200


@categoriesAPI.route("/category_by_id/<int:id>", methods=["GET"])
def category_by_id(id):
    category = Category.query.filter_by(id=id).first()
    category_output = category_schema.dump(category)

    return jsonify({"category": category_output}), 200