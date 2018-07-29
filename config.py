import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '452rjlk&*#HJKJnkj23kfs-23+NIOs'

