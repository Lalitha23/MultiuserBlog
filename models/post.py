from models import db
from models.authenticator import render_str
from models.user import User
import time


'''
Define the value of blog parent

'''

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    user = db.ReferenceProperty(User, collection_name='user_posts')

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("permalink.html", post=self)


class Like(db.Model):
    post = db.ReferenceProperty(Post, required=True)
    user = db.ReferenceProperty(User, required=True)

    @classmethod
    def by_post_id(cls, post_id):
        like = Like.all().filter('post =', post_id)
        return like.count()

    @classmethod
    def check_like(cls, post_id, user_id):
        liked = Like.all().filter(
            'post =', post_id).filter(
            'user =', user_id)
        return liked.count()


class Unlike(db.Model):
    post = db.ReferenceProperty(Post, required=True)
    user = db.ReferenceProperty(User, required=True)

    @classmethod
    def by_post_id(cls, post_id):
        unlike = Unlike.all().filter('post =', post_id)
        return unlike.count()

    @classmethod
    def check_unlike(cls, post_id, user_id):
        unliked = Unlike.all().filter(
            'post =', post_id).filter(
            'user =', user_id)
        return unliked.count()

class Comment(db.Model):
    post = db.ReferenceProperty(Post, required=True)
    user = db.ReferenceProperty(User, required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    text = db.TextProperty(required=True)

    @classmethod
    def count_by_post_id(cls, post_id):
        comments = Comment.all().filter('post =', post_id)
        return comments.count()

    @classmethod
    def all_by_post_id(cls, post_id):
        comments = Comment.all().filter('post =', post_id).order('created')
        return comments
