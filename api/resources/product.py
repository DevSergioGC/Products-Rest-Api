from flask.views import MethodView
from flask_smorest import Blueprint, abort
from api.schemas import ProductSchema

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from api.db import db
from api.models import ProductModel

blp = Blueprint("products", __name__, description="Operations on products")

@blp.route("/product")
class ProductList(MethodView):
    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, new_data):
        """Create a new product"""
        product = ProductModel(**new_data)
        db.session.add(product)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, message="Product already exists")
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))
        return product, 201
    
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        """Get all products"""
        products = ProductModel.query.all()
        return products

@blp.route("/product/<int:product_id>")
class Product (MethodView):
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        """Get a product"""
        product = ProductModel.query.get_or_404(product_id)
        return product

    @blp.arguments(ProductSchema)
    @blp.response(200, ProductSchema)
    def put(self, new_data, product_id):
        """Update a product"""
        product = ProductModel.query.get_or_404(product_id)
        product.name = new_data["name"]
        product.url_img = new_data["url_img"]
        product.description = new_data["description"]
        product.price = new_data["price"]
        
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, message="Product already exists")
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))
        return product
    
    @blp.response(204)
    def delete(self, product_id):
        """Delete a product"""
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))
        return {"message": "Product deleted successfully"}, 204