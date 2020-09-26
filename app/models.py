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
  posts = db.relationship('Post',backref = 'author',lazy = "dynamic")
  comments = db.relationship('Comment',backref = 'author',lazy = "dynamic") 
  bio = db.Column(db.String(255))
  gender = db.Column(db.String(255))
  profile_pic_path = db.Column(db.String(255))
  
  
  @property
  def password(self):
    raise AttributeError('You cannot reade the password attribute')
  
  @password.setter 
  def password(self, password):
    self.pass_secure = generate_password_hash(password)
    
  def verify_password(self, password):
    return check_password_hash(self.pass_secure,password) 
  
  @classmethod
  def get_user(cls, username):
    user= User.query.filter_by(username=username).all()
    return user
    
       
     
 
class  Post(db.Model):
  __tablename__ = 'posts'
  
  id = db.Column(db.Integer, primary_key=True) 
  title = db.Column(db.String(255))
  post = db.Column(db.String(255))
  posted = db.Column(db.DateTime,default=datetime.utcnow) 
  comment = db.relationship('Comment', backref = 'post',lazy ="dynamic")
  user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
  
  def save_post(self):
    db.session.add(self)
    db.session.commit()
    
  def delete_post(self):
     db.session.delete(self)
     db.session.commit() 
     
     
  @classmethod
  def get_posts(cls, user_id):
    post= Post.query.filter_by(user_id=user_id).all()   
    return post
    
     
  def __repr__(self):
    return f'Post{self.post}'   
  
class Comment(db.Model):
  __tablename__ = 'comments'
  
  id = db.Column(db.Integer, primary_key=True) 
  posted = db.Column(db.DateTime,default=datetime.utcnow) 
  user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
  comment = db.Column(db.String(255))
  post_id = db.Column(db.Integer,db.ForeignKey("posts.id"))
  
  
  def save_comment(self):
    db.session.add(self)
    db.session.commit()
    
  def delete_comment(self):
    db.session.delete(self)
    db.session.commit()
    
  @classmethod 
  def get_comments(cls,post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    return comments
      
  def __repr__(self):
    return f'comment:{self.comment}'    
    
     
  
  
  
