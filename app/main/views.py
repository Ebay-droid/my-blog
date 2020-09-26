from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from  ..models import User,Post, Comment,Quotes
from .. import db,photos
from . forms import UpdateProfile, CommentForm, PostForm
from ..request import  get_quotes

@main.route('/')
def index():
  
  return render_template('index.html')

@main.route('/user/<username>')
def profile(username):
  user = User.query.filter_by(username=username).first()
  
  if user is None:
    abort(404)
    
  return render_template("profile/profile.html", user = user)  

@main.route('/user/<username>/update',methods = ['GET','POST'])
@login_required 
def update_profile(username):
  user = User.query.filter_by(username=username).first()
  
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
  user = User.query.filter_by(username=username).first()
  if 'photo' in request.files:
    filename = photos.save(request.files['photo'])
    path =f'photos/{filename}'
    user.profile_pic_path = path
    db.session.commit()
  return redirect(url_for('main.profile', username=username))  
    
    
@main.route('/blogs/new_post', methods=['GET','POST'])
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    title = form.title.data
    post=form.post.data
    
    new_post=Post(title=title,post=post)
    new_post.save_post()
    return redirect(url_for('.all_posts'))
  
  return render_template('new_blog.html',post_form=form)

@main.route('/blogs')
def all_posts():
  # user = User.query.filter_by(username=username).first()
  posts = Post.query.all()
  user = current_user
  quote = get_quotes()
  
  return render_template('blog.html', posts=posts,user=user,quote = quote)

@main.route('/blogs/comment/<int:post_id>',methods = ['GET','POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    comments = Comment.get_comments(post_id)
    
    if form.validate_on_submit():
        comment = form.comment.data
        post_id = post_id
        new_comment = Comment(comment = comment, post_id=post_id)
        
        
        new_comment.save_comment()
        return redirect(url_for('.index',form =form,post_id =post_id))
    
    return render_template('comments.html', comment_form =form, comments = comments, post_id =post_id)
  
# @main.route('/')  
# @login_required
# def Quotes():
#   quote = get_quotes()
  
#   return render_template