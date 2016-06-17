class Config:
    SECRET_KEY = '\x97\xe0\xcb\xff\x8a4\x11\x83U\xf5\x9a\x14\x9e\xf7\xcc\x13\x9c\\m\xe7\xb0X\x9d'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    POSTS_PER_PAGE = 5
    USER_REGISTER_CODE = 'yourcode'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@127.0.0.1/flask'


config = {
    'default': DevelopmentConfig
}
