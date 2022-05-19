from operator import pos
from flask import render_template,request,flash,redirect,url_for,abort
from . import main
from .. import db,photos
from ..models import User,Post,Comment,Like,Dislike,Subscriber
from .forms import PostForm,UpdateProfile
from ..request import get_random_quote
from flask_login import login_required,current_user
# from ..email import mail_message





@main.route('/')
def index():

    quote = get_random_quote()
    posts = Post.query.order_by(Post.time_created.desc())

    return render_template('index.html',quote=quote,posts=posts)


@main.route('/create-post', methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    subscribers = Subscriber.query.all()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        post = Post(content=content, title=title, user_id=current_user.id)
        post.save_post()
        flash('Post created!', category='success')
        # for subscriber in subscribers:
        #     mail_message('New Blog Post','email/new_post',subscriber.email,post=post)
        return redirect(url_for('.index'))

    return render_template('create_post.html',post_form=form,user=current_user)


@main.route('/posts/<username>')
@login_required
def posts(id):

    post = User.query.get(id)

    comments = Comment.query.filter_by(post_id=id).all()
    return render_template('posts.html',user=current_user,post=post,comments=comments)


@main.route('/post/<post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if post.user != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('.index',id = post.id))
    
    if request.method =='GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('update_post.html', form = form)


@main.route('/create-comment/<post_id>', methods=['GET','POST'])
@login_required
def create_comment(post_id):

    comment = request.form.get('comment')
    title = 'Comment'

    if comment is None:
        abort(404)

    else:
        posts = Post.query.filter_by(id=post_id)
        if posts:
                new_comment = Comment(comment=comment, user_id=current_user.id,post_id=post_id)
                new_comment.save_comment()

    return redirect(url_for('.index'))

    


@main.route('/delete-post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if post is  None:
        abort(404)

    elif current_user.id != post.id:
        flash('You do not have permission to delete this post!')

    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!')

    return redirect(url_for('.index'))



@main.route('/delete-comment/<id>')
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()

    if comment is None:
        flash('Comment not found!')

    elif current_user.id != comment.user_id and current_user.id != comment.post.user_id:
        flash('You are not allowed to delete this comment!')

    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('.index'))


@main.route('/subscribe',methods=['GET','POST'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscription = Subscriber(email=email)
    new_subscription.save_subscribers()


    return redirect(url_for('.index'))


@main.route('/like-post<id>', methods=['GET','POST'])
@login_required
def like_post(id):
    get_posts = Like.get_likes(id)
    valid_string = f'{current_user.id}:{id}'
    for post in get_posts:
        to_str = f'{post}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('.index',id=id))
        else:
            continue
    like = Like(user = current_user, post_id=id)
    like.save_likes()
    return redirect(url_for('.index',id=id))


@main.route('/dislike-post<id>', methods=['GET','POST'])
@login_required
def dislike_post(id):
    get_posts = Dislike.get_dislikes(id)
    valid_string = f'{current_user.id}:{id}'
    for post in get_posts:
        to_str = f'{post}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('.index',id=id))
        else:
            continue
    dislike = Dislike(user = current_user,post_id=id)
    dislike.save_dislikes()
    return redirect(url_for('.index',id=id))


@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))