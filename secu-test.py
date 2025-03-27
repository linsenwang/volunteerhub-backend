from flask import Flask, redirect, url_for, jsonify, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, auth_required
from authlib.integrations.flask_client import OAuth
import os
import uuid

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECURITY_PASSWORD_SALT"] = "your_salt"
app.config["SECURITY_REGISTERABLE"] = True  # 允许注册
app.config["SECURITY_SEND_REGISTER_EMAIL"] = False  # 关闭注册邮件验证

db = SQLAlchemy(app)

# 创建用户和角色的数据库模型
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary="user_roles", backref=db.backref('users', lazy='dynamic'))
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

# 设置 Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# 配置 OAuth
oauth = OAuth(app)
oauth.register(
    "google",
    client_id=os.environ['GOAUTH_ID'],
    client_secret=os.environ['GOAUTH_SECRET'],
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    client_kwargs={"scope": "openid email profile"},
)

@app.route("/login/google")
def login_google():
    # 将生成的 state 参数存入 session
    state = uuid.uuid4().hex
    session['oauth_state'] = state
    return oauth.google.authorize_redirect(url_for("authorize_google", _external=True, state=state))

@app.route("/authorize/google")
def authorize_google():
    # 检查请求中的 state 参数是否与 session 中的匹配
    state_from_request = request.args.get('state')
    if state_from_request != session.get('oauth_state'):
        return jsonify({"error": "Invalid state parameter"}), 400

    # 授权访问并获取令牌
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    
    # 检查用户是否存在
    user = User.query.filter_by(email=user_info["email"]).first()
    if not user:
        user = User(email=user_info["email"], active=True)
        db.session.add(user)
        db.session.commit()

    # 你可以为新用户分配角色
    user_role = Role.query.filter_by(name='User').first()
    if user_role and user not in user_role.users:
        user.roles.append(user_role)
        db.session.commit()

    return jsonify({"message": "OAuth 登录成功", "user": user_info})

@app.route("/")
@auth_required()  # 任何已登录用户都可以访问
def home():
    return "Hello, World!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
