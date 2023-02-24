from api.db import db

class ProductModel(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    url_img = db.Column(db.String(250))
    description = db.Column(db.String(250))
    price = db.Column(db.Float(precision=2), nullable=False)
    users = db.relationship('UserModel', secondary='products_users', back_populates='products')
    
    def __init__(self, name, price, description, url_img):
        self.name = name
        self.description = description
        self.img = url_img
        self.price = price
    
    def json(self):
        return {
            'name': self.name, 
            'description': self.description, 
            'img': self.url_img, 
            'price': self.price
        }
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()