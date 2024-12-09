
from flask import Flask, redirect
from flask_migrate import Migrate
from app.configs.config import Config
from app.configs.connector import db, migrate, jwt,mail  # Import extensions
def create_app():
    
    """Create a new Flask application instance.

    This function sets up a new Flask application instance and configures it
    with the correct database and authentication settings. It also sets up a
    few basic routes for creating the database and seeding it with data.

    Returns:
        A new Flask application instance.
    """
    app = Flask(__name__)
    migrate = Migrate(app, db)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # Register Blueprints
    from app.routes.api_routes import user_bp, profile_bp, auth_bp, product_bp, seller_bp, cart_bp, wishlist_bp, voucher_bp, review_bp

    app.register_blueprint(user_bp, url_prefix='/api/v1/users')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(profile_bp, url_prefix='/api/v1/profile')
    app.register_blueprint(product_bp, url_prefix='/api/v1/products')
    app.register_blueprint(seller_bp, url_prefix='/api/v1/sellers')
    app.register_blueprint(cart_bp, url_prefix='/api/v1/carts')
    app.register_blueprint(wishlist_bp, url_prefix='/api/v1/wishlist')
    app.register_blueprint(voucher_bp, url_prefix='/api/v1/vouchers')
    app.register_blueprint(review_bp, url_prefix='/api/v1/reviews')
    
    # Define basic routes for DB creation and seeding
    @app.route('/')
    def index():
       return redirect('https://documenter.getpostman.com/view/40195523/2sAYBd7o1D')
   
   
    @app.route('/create-all-db')
    def create_all_db():
        db.create_all()  # No need to return anything here
        return 'Database tables created successfully!'
    
    return app
