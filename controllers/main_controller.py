from flask import Blueprint, render_template,session, redirect, request, url_for


main_bp = Blueprint('main', __name__)


@main_bp.route('/set_language')
def set_language():
    language = request.args.get('language')
    if language and language in ['fr', 'mg', 'en']:  # Validate supported languages
        session['language'] = language
    
    # Redirect to either:
    # 1. The 'next' parameter if provided
    # 2. The referrer URL
    # 3. The default index page as fallback
    return redirect(
        request.args.get('next') or 
        request.referrer or 
        url_for('main.index')
    )

@main_bp.route('/acceuil')
def acceuil():
  
    return render_template('acceuil.html')

@main_bp.route('/maison')
def maison_critere():
  
    return render_template('predict_maison.html')

@main_bp.route('/terrain')
def terrain_critere():
  
    return render_template('predict_terrain.html')



