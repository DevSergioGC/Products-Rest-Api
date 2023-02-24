from api.db import db

class ProductModel(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    url_img = db.Column(db.String(250))
    description = db.Column(db.String(250))
    price = db.Column(db.Float(precision=2), nullable=False)
    users = db.relationship('UserModel', secondary='product_user', back_populates='products')
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()