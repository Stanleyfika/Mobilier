from flask import Blueprint, render_template, request, flash, redirect, url_for
import joblib
import numpy as np
from controllers.main_controller import main_bp
import os
from werkzeug.utils import secure_filename

predict_bp = Blueprint('predict', __name__, template_folder='../templates')

# Charger les modèles
def load_model(model_type):
    model_path = os.path.join(
        os.path.dirname(__file__),
        '../regression/model_files',
        f'modele_{model_type}.joblib'

    )
    return joblib.load(model_path)

# Modèles chargés au démarrage
terrain_model = load_model('terrain')
maison_model = load_model('maison')

@predict_bp.route('/predict/maison', methods=['GET', 'POST'])
def predict_maison():
    if request.method == 'POST':
        try:
            # Récupération des données du formulaire
            data = {
                'acces': int(request.form.get('acces')),
                'typeMaison': int(request.form.get('typeMaison')),
                'type': int(request.form.get('type')),
                'toilette': request.form.get('toilette'),
                'nbChambres': int(request.form.get('nbChambres')),
                'latitude': float(request.form.get('latitude')),
                'longitude': float(request.form.get('longitude'))
            }

            # Préparation des données pour la prédiction
            features = prepare_maison_features(data)
            
            # Prédiction
            prediction = maison_model.predict([features])[0]
            prediction_formatted = "{:,.0f} Ar".format(prediction)

            return render_template('result_maison.html', 
                               prediction=prediction_formatted,
                               data=data)

        except Exception as e:
           
            import traceback
            traceback.print_exc()  # Affiche l'erreur complète dans la console
            flash(f"Erreur lors de la prédiction: {str(e)}", 'error')
            return redirect(url_for('main.maison_critere'))

    return render_template('predict_maison.html')
    

@predict_bp.route('/predict/terrain', methods=['GET', 'POST'])
def predict_terrain():
    if request.method == 'POST':
        try:
            data = {
                'surface': float(request.form.get('surface')),
                'acces': int(request.form.get('acces')),
                'typePapier': request.form.get('typePapier'),
                'pretBatir': request.form.get('pretBatir'),
                'cloture': request.form.get('cloture'),
                'latitude': float(request.form.get('latitude')),
                'longitude': float(request.form.get('longitude'))
            }

            features = prepare_terrain_features(data)
            prediction = terrain_model.predict([features])[0]
            prediction_formatted = "{:,.0f} Ar".format(prediction)

            return render_template('result_terrain.html',
                                prediction=prediction_formatted,
                                data=data)

        except Exception as e:
            flash(f"Erreur lors de la prédiction: {str(e)}", 'error')
            return redirect(url_for('main.terrain_critere'))

    return render_template('predict_terrain.html')

def prepare_maison_features(data):
    """Préparer les features pour le modèle maison"""
    # Implémentez votre logique de préparation des données ici
    features = [
        data['acces'],
        data['typeMaison'],
        data['type'],
        1 if data['toilette'] == 'Oui' else 0,
        data['nbChambres'],
        data['latitude'],
        data['longitude']
    ]
    return features

def prepare_terrain_features(data):
    """Préparer les features pour le modèle terrain"""
    # Implémentez votre logique de préparation des données ici
    features = [
        data['surface'],
        data['acces'],
        1 if data['typePapier'] == 'Titre Foncier' else 0,
        1 if data['pretBatir'] == 'Oui' else 0,
        1 if data['cloture'] == 'Oui' else 0,
        data['latitude'],
        data['longitude']
    ]
    return features