# HomeMate/server/app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from .tasks.celery import init_celery
from flask_caching import Cache

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()
cache = Cache()

def app_creator(MyConfig):
    app = Flask(__name__)
    app.config.from_object(MyConfig)
    db.init_app(app)
    api = Api(app)
    mail.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    CORS(app, resources={r"/*": {"origins": app.config.get('FRONTEND_URL'), "supports_credentials": True}})

    from .models import User, Admin, Customer, ServiceProfessional, Service, ServiceRequest, Notification, Review, ServiceablePincode, OAuth
    with app.app_context():
        db.create_all()

    from .api import HomeApi, SignupApi, LoginApi, ServiceApi, LogoutApi, ResetPasswordApi ,GoogleAuthSignupApi, GoogleAuthLoginApi, FacebookAuthLoginApi, FacebookAuthSignupApi, TokenApi, ProfileApi, ServicerApi, AutoCompleteApi, PincodeToCityApi, ServiceRequestApi, PaymentApi, StatsApi, ReviewApi, CustomerApi, TasksApi
    api.add_resource(HomeApi, '/')
    api.add_resource(SignupApi, '/api/signup')
    api.add_resource(LoginApi, '/api/login')
    api.add_resource(ServiceApi, '/api/services', '/api/services/<int:service_id>')
    api.add_resource(GoogleAuthSignupApi, '/api/signup/google-oauth')
    api.add_resource(GoogleAuthLoginApi, '/api/login/google-oauth')
    api.add_resource(FacebookAuthSignupApi, '/api/signup/facebook-oauth')
    api.add_resource(FacebookAuthLoginApi, '/api/login/facebook-oauth')
    api.add_resource(TokenApi, '/api/token-chekcer')
    api.add_resource(LogoutApi, '/api/logout')
    api.add_resource(ResetPasswordApi, '/api/reset-password')
    api.add_resource(ProfileApi, '/api/profile')
    api.add_resource(ServicerApi, '/api/servicer', '/api/servicer/<int:servicer_id>')
    api.add_resource(AutoCompleteApi, '/api/autocomplete')
    api.add_resource(PincodeToCityApi, '/api/pincode-to-city')
    api.add_resource(ServiceRequestApi, '/api/service-requests', '/api/service-requests/<int:service_request_id>')
    api.add_resource(PaymentApi, '/api/payment')
    api.add_resource(StatsApi, '/api/stats')
    api.add_resource(ReviewApi, '/api/review/<service_request_id>')
    api.add_resource(CustomerApi, '/api/customers', '/api/customers/<customer_id>')
    api.add_resource(TasksApi, '/api/tasks')

    
    migrate.init_app(app, db)
    celery = init_celery(app)

    return app, celery