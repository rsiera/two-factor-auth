from functools import wraps
from flask import request, g, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from index import app

TWO_WEEKS = 60 * 60 * 24 * 14


def generate_token(user, expiration=TWO_WEEKS):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'id': user.id, 'email': user.email}).decode('utf-8')
    return token


def validate_token(token):
    serializer = Serializer(app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token)
    except (BadSignature, SignatureExpired):
        return None
    return data


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token:
            string_token = token.encode('ascii', 'ignore')
            user = validate_token(string_token)
            if user:
                g.current_user = user
                return f(*args, **kwargs)

        return jsonify(message="Authentication is required to access this resource"), 401
    return decorated
