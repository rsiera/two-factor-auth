from flask import request, render_template, jsonify, g

from application.auth import generate_token, requires_auth, validate_token
from index import app, db
from .models import User


@app.before_first_request
def create_all():
    db.session.query(User).delete()
    db.session.commit()

    no_2fa_user = User(email='no-2fa-auth@gmail.com', password='test')
    with_2fa_user = User(email='2fa-auth@gmail.com', password='test')
    with_2fa_user.is_two_factor_authentication_enabled = True
    with_2fa_user.phone = '+48727842536'

    db.session.add(no_2fa_user)
    db.session.add(with_2fa_user)
    db.session.commit()


@app.route('/', methods=['GET'])
@app.route('/protected', methods=['GET'])
@app.route('/login', methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/api/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(g.current_user)


@app.route("/api/get-token", methods=["POST"])
def get_token():
    custom_error_messages = {
        'invalid_login': ["Please enter a correct email and password. Note that both fields may be case-sensitive."],
        'invalid_code': ['Invalid security code. Please enter the last correct security code you received by SMS.'],
        'enter_code': ['Please enter the last correct security code you received by SMS.'],
    }

    data = request.get_json()
    user = User.get_user_with_email_and_password(data["email"], data["password"])

    if user is None:
        return jsonify(show_2fa=False, non_field_errors=custom_error_messages['invalid_login']), 400

    if user.is_two_factor_authentication_enabled:
        two_fa_code = data['two_fa_code']
        if two_fa_code == '':
            user.send_2fa_code()
            return jsonify(show_2fa=True, non_field_errors=custom_error_messages['enter_code']), 400
        if not user.is_valid_two_factor_code(two_fa_code):
            return jsonify(show_2fa=True, non_field_errors=custom_error_messages['invalid_code']), 400
        if user.is_valid_two_factor_code(two_fa_code):
            return jsonify(token=generate_token(user))

    return jsonify(token=generate_token(user))


@app.route("/api/verify-token", methods=["POST"])
def verify_token():
    incoming = request.get_json()
    is_valid = validate_token(incoming["token"])

    if not is_valid:
        return jsonify(token_is_valid=False), 403
    return jsonify(token_is_valid=True)
