import webapp2
import os
import jinja2

import hmac

from handlers.authhandler import Signup, Register, Login, Logout
from handlers.mainpagehandler import Landing, BlogFront,NewPost,LikeHandler,\
                                     UnLikeHandler,CommentHandler,PostPage,\
                                     DeletePost,EditPost,EditComment,DeleteComment




app = webapp2.WSGIApplication([('/', Landing),
                            ('/blog/?', BlogFront),
                            ('/blog/newpost', NewPost),
                            ('/blog/like/([0-9]+)', LikeHandler),
                            ('/blog/unlike/([0-9]+)', UnLikeHandler),
                            ('/blog/([0-9]+)/comment', CommentHandler),
                            ('/login', Login),
                            ('/blog/([0-9]+)', PostPage),
                            ('/blog/deletepost/([0-9]+)', DeletePost),
                            ('/blog/editpost/([0-9]+)', EditPost),
                            ('/blog/([0-9]+)/editcomment/([0-9]+)', EditComment),
                            ('/blog/([0-9]+)/deletecomment/([0-9]+)', DeleteComment),
                            ('/logout', Logout),
                            ('/signup', Register),
                            ],
                            debug=True)
