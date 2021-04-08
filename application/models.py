import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from index import db

TWO_FA_CODE_EXPIRY_TIMEDELTA = timedelta(minutes=15)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    is_two_factor_authentication_enabled = db.Column(db.Boolean, default=False)
    two_factor_authentication_code = db.Column(db.String(20))
    two_factor_authentication_last_requested = db.Column(db.DateTime)

    phone = db.Column(db.String(25))

    def __init__(self, email, password):
        self.email = email
        self.password = self.hashed_password(password)
        self.active = True

    def hashed_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_with_email_and_password(cls, email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None

    def is_two_factor_enabled(self):
        return self.is_two_factor_authentication_enabled and self.phone

    def is_valid_two_factor_code(self, two_fa_code):
        return two_fa_code != '' and two_fa_code == self.two_factor_authentication_code and \
               self.two_factor_authentication_last_requested > datetime.now() - TWO_FA_CODE_EXPIRY_TIMEDELTA

    def send_2fa_code(self):
        code = random.randrange(100000, 999999)
        self.two_factor_authentication_code = code
        self.two_factor_authentication_last_requested = datetime.now()
        db.session.add(self)
        db.session.commit()
        print(code, self.phone)
