from google.appengine.ext import db
from hpw import *


# [START GQL Blogposts datastore & entity types]
class Blogposts(db.Model):
    """
    enables adding to the App Engine database,
    and specifies the entity data types
    """
    title = db.StringProperty(required=True)
    blogPost = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    # required=True is a constraint enforces posts to db must have a title
    # auto_add_now adds an entry automatically with every submission
# [END GQL datastore & entity types]


# [START GQL User datastore & entity types]
# remove decorators? register needs to be kept
# start: move to models.py & convert to ndb
class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()      # no required statement as user optional

    # decorators
    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u
# [END GQL User datastore & entity types]
