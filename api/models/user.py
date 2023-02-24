from api.db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"), nullable=False, unique=True)
    products = db.relationship('ProductModel', back_populates='users', secondary='product_user')
    
    def __init__(self, username, password, email, level):
        self.username = username
        self.password = password
        self.email = email
        self.level = level
    
    def json(self):
        return {'username': self.username, 'email': self.email, 'level': self.level}
    
    @classmethod
    def find_by_username(cls, id):
        return cls.query.filter_by(id=id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()