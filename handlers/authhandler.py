from basehandler import BlogHandler
from models.user import User
from models.authenticator import valid_username, valid_password, valid_email
from models.user import check_path


class Signup(BlogHandler):
    def get(self):
        path_check = check_path(self)
        self.render('signup-form.html', path_check=path_check)

    def post(self):
        have_error = False
        path_check = check_path(self)
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not valid_username(self.username):
            params['error_username'] = "Invalid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "Invalid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Passwords do not match"
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "Invalid email"
            have_error = True

        if have_error:
            self.render('signup-form.html', path_check=path_check, **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):
    def done(self):
        path_check = check_path(self)
        u = User.by_name(self.username)
        if u:
            error = 'That user already exists.'
            self.render('signup-form.html', error_username=error,
                         path_check=path_check)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/blog/')


class Login(BlogHandler):
    def get(self):
        path_check = check_path(self)
        self.render('login-form.html', path_check=path_check)

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        path_check = check_path(self)
        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog/')
        else:
            error = 'Invalid login'
            self.render('login-form.html', error=error, path_check=path_check)


class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/login')
