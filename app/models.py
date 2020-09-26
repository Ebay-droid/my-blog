from . import db 
from  . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User (UserMixin,db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer,primary_key=True)
  username = db.Column(db.String(255),index=True)
  email = db.Column(db.String(255),unique=True,index=True)
  pass_secure = db.Column(db.String(255))
  
  @property
  def password(self):
    raise AttributeError('You cannot reade the password attribute')
  
  @password.setter 
  def password(self, password):
    self.pass_secure = generate_password_hash(password)
    
  def verify_password(self, password):
    return check_password_hash(self.pass_secure,password) 
 
class  Post(db.Model):
  __tablename__ = 'posts'
  
  id = db.Column(db.Integer, primary_key=True) 
  title = db.Column(db.String(255))
  blog = db.Column(db.String(255))
  posted = db.Column(db.DateTime,default=datetime.utcnow) 
  comment = db.relationship('Comment', backref = 'post',lazy ="dynamic")
  
  
  def save_post(self):
    db.session.add(self)
    db.session.commit()
    
  def delete_post(self):
     db.session.delete(self)
     db.session.commit() 
     
  def __repr__(self):
    return f'Post{self.post}'   
  
