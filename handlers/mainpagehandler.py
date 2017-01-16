from google.appengine.ext import db
from basehandler import BlogHandler

from models.post import Post, Like, Unlike, Comment, blog_key
from models.user import User, post_key, check_path
from functools import wraps
import time


class Landing(BlogHandler):
    def get(self):
        self.redirect('/blog')


class BlogFront(BlogHandler):
    def get(self):
        path_check = check_path(self)
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")
        if posts:
            self.render("blog.html", posts=posts, path_check=path_check)


class NewPost(BlogHandler):
    '''
       Creating a new post, checks for subject and content
    '''
    def get(self):
        path_check = check_path(self)
        if self.user:
            self.render('newpost.html')
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            return self.redirect('/login')
        subject = self.request.get("subject")
        content = self.request.get("content")
        user_id = User.by_name(self.user.name)
        author = self.user.name

        if subject and content:
            post = Post(
                parent=post_key(),
                subject=subject,
                content=content,
                user=user_id)
            post.put()
            self.redirect('/blog/%s' % str(post.key().id()))
        else:
            post_error = "All fields required"
            self.render(
                "newpost.html",
                subject=subject,
                content=content,
                post_error=post_error)


def is_post(function):
    @wraps(function)
    def wrapper(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=post_key())
        post = db.get(key)
        if post:
            return function(self, post_id, post)
        else:
            self.error(404)
            return
    return wrapper

class LikeHandler(BlogHandler):
    @is_post
    def get(self, post_id, post):
        
        user_id = User.by_name(self.user.name)
        comment_count = Comment.count_by_post_id(post)
        comments = Comment.all_by_post_id(post)
        likes = Like.by_post_id(post)
        unlikes = Unlike.by_post_id(post)
        liked = Like.check_like(post, user_id)
        unliked = Unlike.check_unlike(post, user_id)
        

        if self.user:
            if post.user.name != self.user.name:
                if liked == 0:
                    like = Like(
                         post=post, user=user_id)
                    like.put()
                    time.sleep(0.1)
                    self.redirect('/blog/%s' % str(post.key().id()))
                else:
                    error = "You can only like a post one time."
                    self.render("permalink.html",
                            post=post,
                            likes=likes,
                            unlikes=unlikes,
                            error=error,
                            comment_count=comment_count,
                            comments=comments)


class UnLikeHandler(BlogHandler):
    @is_post
    def get(self, post_id, post):

        user_id = User.by_name(self.user.name)
        comment_count = Comment.count_by_post_id(post)
        comments = Comment.all_by_post_id(post)
        likes = Like.by_post_id(post)
        unlikes = Unlike.by_post_id(post)
        liked = Like.check_like(post, user_id)
        unliked = Unlike.check_unlike(post, user_id)

        if self.user:
            if post.user.name != self.user.name:
                if unliked == 0:
                    ul = Unlike(
                        post=post, user=user_id)
                    ul.put()
                    time.sleep(0.1)
                    self.redirect('/blog/%s' % str(post.key().id()))
                else:
                   error = "You can only unlike a post one time."
                   self.render(
                      "permalink.html",
                       post=post,
                       likes=likes,
                       unlikes=unlikes,
                       error=error,
                       comment_count=comment_count,
                       comments=comments)


class CommentHandler(BlogHandler):
    @is_post
    def get(self, post_id, post):
        
        user_id = User.by_name(self.user.name)
        comment_count = Comment.count_by_post_id(post)
        comments = Comment.all_by_post_id(post)
        likes = Like.by_post_id(post)
        unlikes = Unlike.by_post_id(post)
        liked = Like.check_like(post, user_id)
        unliked = Unlike.check_unlike(post, user_id)

        if self.user:
            self.render("comment.html")
        else:
            self.redirect('/login')


    @is_post
    def post(self, post_id, post):

        user_id = User.by_name(self.user.name)
        comment_count = Comment.count_by_post_id(post)
        comments = Comment.all_by_post_id(post)
        likes = Like.by_post_id(post)
        unlikes = Unlike.by_post_id(post)
        liked = Like.check_like(post, user_id)
        unliked = Unlike.check_unlike(post, user_id)
        
        if self.request.get("post"):
            comment_text = self.request.get("comment_text")
            if comment_text:
                comment = Comment(
                            post=post, user=user_id,
                            author=self.user.name, text=comment_text)
                comment.put()
                comment_count += 1
                time.sleep(0.1)
                self.redirect('/blog/%s' % str(post.key().id()))
            else:
                comment_error = "All fields required."
                self.render(
                        "permalink.html",
                        post=post,
                        likes=likes,
                        unlikes=unlikes,
                        comment_count=comment_count,
                        comments=comments,
                        comment_error=comment_error)
        elif self.request.get("cancel"):
            self.redirect('/blog/%s' % str(post.key().id()))
            
                
            
                            
class PostPage(BlogHandler):
    @is_post
    def get(self, post_id, post):

        likes = Like.by_post_id(post)
        unlikes = Unlike.by_post_id(post)
        comments = Comment.all_by_post_id(post)
        comment_count = Comment.count_by_post_id(post)

        self.render(
            "permalink.html",
            post=post,
            likes=likes,
            unlikes=unlikes,
            comments=comments,
            comment_count=comment_count)

    @is_post
    def post(self, post_id, post):
        if self.user:
            if self.request.get("edit"):
                self.redirect('/blog/editpost/%s' % str(post.key().id()))
            elif self.request.get("delete"):
                self.redirect('/blog/deletepost/%s' % str(post.key().id()))
            elif self.request.get("like"):
                self.redirect('/blog/like/%s' % str(post.key().id()))
            elif self.request.get("unlike"):
                self.redirect('/blog/unlike/%s' % str(post.key().id()))
            elif self.request.get("add_comment"):
                self.redirect('/blog/%s/comment' % str(post.key().id()))

    
            

class EditPost(BlogHandler):
    @is_post
    def get(self, post_id, post):
    
        if self.user.name == post.user.name:
            self.render("editpost.html", post=post)
        else:
            self.redirect("/login")

    @is_post
    def post(self, post_id, post):
        if self.request.get("update"):

            subject = self.request.get("subject")
            content = self.request.get("content").replace('\n', '<br>')

            if subject and content:
                post.subject = subject
                post.content = content
                post.put()
                time.sleep(0.1)
                self.redirect('/blog/%s' % str(post.key().id()))
            else:
                post_error = "All fields required."
                self.render(
                    "editpost.html",
                    post=post,
                    subject=subject,
                    content=content,
                    post_error=post_error)
        elif self.request.get("cancel"):
            self.redirect('/blog/%s' % str(post.key().id()))
            

def is_comment(function):
    @wraps(function)
    def wrapper(self, post_id, comment_id):
        pkey = db.Key.from_path("Post", int(post_id), parent=post_key())
        post = db.get(pkey)
        key = db.Key.from_path("Comment", int(comment_id))
        comment = db.get(key)
        if comment:
            return function(self, comment, post_id, post, comment_id)
        else:
            self.error(404)
            return
    return wrapper

class EditComment(BlogHandler):
    @is_comment
    def get(self, comment, post_id, post, comment_id):
        
        if self.user:
            if comment.user.name == self.user.name:
                self.render("editcomment.html", comment=comment)
        else:
            error = "This comment no longer exists"
            self.render("editcomment.html", edit_error=error)
            
    @is_comment
    def post(self, comment, post_id, post, comment_id):

        if self.user:
            if comment.user.name == self.user.name:
                if self.request.get("update"):
                    content = self.request.get("comment")

                    if content:
                        comment.text = content
                        comment.put()
                        time.sleep(0.1)
                        self.redirect('/blog/%s' % str(post.key().id()))
                    else:
                        edit_error = "All fields required."
                        self.render('editcomment.html', comment=comment,
                        edit_error=edit_error)
                elif self.request.get("cancel"):
                    self.redirect('/blog/%s' % str(post.key().id()))


class DeleteComment(BlogHandler):
    @is_comment
    def get(self, comment, post_id, post, comment_id):
        if self.user:
            if comment.user.name == self.user.name:
                db.delete(comment.key())
                self.render("deletecomment.html")
        else:
            self.redirect('/login')


class DeletePost(BlogHandler):
    @is_post
    def get(self, post_id, post):
        if self.user:
            if self.user.name == post.user.name:
                db.delete(post.key())
                time.sleep(0.1)
                self.render("deletepost.html")
        else:
            self.redirect('/login')
            
