from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from  ..models import User,Post, Comment
from .. import db,photos
from . forms import UpdateProfile, CommentForm, PostForm

@main.route('/')
def index():
  
  return render_template('index.html')

@main.route('/user/<username>')
def profile(username):
  user = User.get_user(username=User.username)
  
  if user is None:
    abort(404)
    
  return render_template("profile/profile.html", user = user)  

@main.route('/user/<username>/update',methods = ['GET','POST'])
@login_required 
def update_profile(username):
  user = User.get_user(username=username)
  
  if user is None:
    abort(404)
    
  form = UpdateProfile()
  
  if form.validate_on_submit():
    user.bio=form.bio.data
    user.gender=form.gender.data
    
    db.session.add(user)
    db.session.commit()
    
    return redirect(url_for('.profile',username=user.username))
  return render_template('profile/update.html',form=form)

@main.route('/user/<username>/update/pic',methods=['POST'])
@login_required
def update_pic(username):
  user = User.get_user(username=username)
  if 'photo' in request.files:
    filename = photos.save(request.files['photo'])
    path =f'photos/{filename}'
    user.profile_pic_path = path
    db.session.commit()
  return redirect(url_for('main.profile', username=username))  
    