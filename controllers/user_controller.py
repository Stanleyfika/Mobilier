from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User

# Création d'un Blueprint pour les routes d'authentification
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def pageLogin():
    if request.method == 'POST':
        # Récupère les données du formulaire
        pseudo = request.form.get('pseudo')
        mdp = request.form.get('mdp')

        # Vérifie les identifiants
        user = User.login(pseudo, mdp)  # Récupère l'utilisateur
        if user:
            # Stocke l'ID de l'utilisateur dans la session
            session['idUser'] = user['IdUser']  # Assure-toi que la clé est correcte
          # Optionnel : Stocke aussi le pseudo
            flash("Connexion réussie !", "success")
            return redirect(url_for('main.acceuil'))  # Redirige vers la page d'achat
        else:
            flash("Pseudo ou mot de passe incorrect", "error")
            return redirect(url_for('auth.pageLogin'))  # Redirige vers la page de connexion

    # Affiche le formulaire de connexion
    return render_template('login.html')