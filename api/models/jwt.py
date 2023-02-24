from api.db import db

class RevokedJWTModel (db.Model):
    __tablename__ = 'revoked_jwt'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(180), unique=True, nullable=False)    
    
    @classmethod
    def find_by_jti(cls, jti):
        return cls.query.filter_by(jti=jti).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()