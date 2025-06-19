from flask import Flask, request, session
from controllers.main_controller import main_bp
from controllers.user_controller import auth_bp
from controllers.predict_controllers import predict_bp
from flask_babel import Babel
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Babel Configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'fr'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

# Define the locale selector function FIRST
def get_locale():
    # 1. Check URL parameter first
    if request.args.get('lang'):
        session['language'] = request.args.get('lang')
        return session['language']
    
    # 2. Check session
    if 'language' in session:
        return session['language']
    
    # 3. Check Accept-Language header from browser
    return request.accept_languages.best_match(['fr', 'en', 'mg']) or 'fr'

# Initialize Babel with locale_selector parameter
babel = Babel(app, locale_selector=get_locale)

# Make get_locale available in templates
from flask_babel import get_locale as babel_get_locale

@app.context_processor
def inject_conf_vars():
    return {
        'get_locale': babel_get_locale
    }

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(predict_bp)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])