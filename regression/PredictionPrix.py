import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

class PredicteurPrixMadagascar:
    def __init__(self, model_dir="model_files"):
        """
        Initialise le prédicteur avec un répertoire de stockage des modèles
        
        Args:
            model_dir (str): Répertoire où sauvegarder/charger les modèles
        """
        self.model_dir = model_dir
        self.model_terrain = None
        self.model_maison = None
        self.scaler_terrain = StandardScaler()
        self.scaler_maison = StandardScaler()
        self.encoders = {}
        
        # Créer le répertoire s'il n'existe pas
        os.makedirs(self.model_dir, exist_ok=True)
    
    def _get_model_path(self, filename):
        """Retourne le chemin complet vers un fichier de modèle"""
        return os.path.join(self.model_dir, filename)
    
    def preparer_donnees_terrain(self, df):
        """
        Prépare les données pour la prédiction de prix de terrain
        Se concentre uniquement sur les données fournies
        """
        # Encoder les variables catégorielles
        if 'typePapier' not in self.encoders:
            self.encoders['typePapier'] = LabelEncoder()
            df['typePapier_encoded'] = self.encoders['typePapier'].fit_transform(df['typePapier'])
        else:
            df['typePapier_encoded'] = self.encoders['typePapier'].transform(df['typePapier'])
            
        # Convertir les variables booléennes
        df['pretBatir_bin'] = (df['pretBatir'] == 'Oui').astype(int)
        df['cloture_bin'] = (df['cloture'] == 'Oui').astype(int)
        
        # Sélectionner les features pour le terrain (sans classification de zone)
        features = ['surface', 'acces', 'typePapier_encoded', 'pretBatir_bin', 
                   'cloture_bin', 'latitude', 'longitude']
        
        return df[features]
    
    def preparer_donnees_maison(self, df):
        """
        Prépare les données pour la prédiction de loyer de maison
        Se concentre uniquement sur les données fournies
        """
        # Encoder la variable toilette si c'est une chaîne
        if df['toilette'].dtype == 'object':
            df['toilette_encoded'] = df['toilette'].map({'Oui': 0, 'Non': 1, 'Aucune': 2})
        else:
            df['toilette_encoded'] = df['toilette']
        
        # Sélectionner les features pour la maison (sans classification de zone)
        features = ['acces', 'typeMaison', 'type', 'toilette_encoded', 'nbChambres',
                   'latitude', 'longitude']
        
        return df[features]
    
    def entrainer_modele_terrain(self, fichier_csv):
        """
        Entraîne le modèle de régression pour les terrains
        """
        # Charger les données
        df = pd.read_csv(fichier_csv)
        
        # Préparer les features
        X = self.preparer_donnees_terrain(df)
        y = df['prix']
        
        # Diviser les données
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Normaliser les données
        X_train_scaled = self.scaler_terrain.fit_transform(X_train)
        X_test_scaled = self.scaler_terrain.transform(X_test)
        
        # Entraîner le modèle
        self.model_terrain = LinearRegression()
        self.model_terrain.fit(X_train_scaled, y_train)
        
        # Évaluer le modèle
        y_pred = self.model_terrain.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Modèle Terrain - MSE: {mse:.2f}, R²: {r2:.4f}")
        
        # Sauvegarder le modèle
        self.sauvegarder_modele('terrain')
        
        return mse, r2
    
    def entrainer_modele_maison(self, fichier_csv):
        """
        Entraîne le modèle de régression pour les maisons
        """
        # Charger les données
        df = pd.read_csv(fichier_csv)
        
        # Préparer les features
        X = self.preparer_donnees_maison(df)
        y = df['loyer']
        
        # Diviser les données
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Normaliser les données
        X_train_scaled = self.scaler_maison.fit_transform(X_train)
        X_test_scaled = self.scaler_maison.transform(X_test)
        
        # Entraîner le modèle
        self.model_maison = LinearRegression()
        self.model_maison.fit(X_train_scaled, y_train)
        
        # Évaluer le modèle
        y_pred = self.model_maison.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Modèle Maison - MSE: {mse:.2f}, R²: {r2:.4f}")
        
        # Sauvegarder le modèle
        self.sauvegarder_modele('maison')
        
        return mse, r2
    
    def predire_prix_terrain(self, donnees):
        """
        Prédit le prix d'un terrain
        donnees: dict avec les clés surface, acces, typePapier, pretBatir, cloture, latitude, longitude
        """
        if self.model_terrain is None:
            self.charger_modele('terrain')
            if self.model_terrain is None:
                raise ValueError("Modèle terrain non chargé. Veuillez d'abord entraîner le modèle.")
        
        # Créer un DataFrame temporaire
        df_temp = pd.DataFrame([donnees])
        X = self.preparer_donnees_terrain(df_temp)
        X_scaled = self.scaler_terrain.transform(X)
        
        prediction = self.model_terrain.predict(X_scaled)[0]
        return max(0, prediction)  # Prix ne peut pas être négatif
    
    def predire_loyer_maison(self, donnees):
        """
        Prédit le loyer d'une maison
        donnees: dict avec les clés acces, typeMaison, type, toilette, nbChambres, latitude, longitude
        """
        if self.model_maison is None:
            self.charger_modele('maison')
            if self.model_maison is None:
                raise ValueError("Modèle maison non chargé. Veuillez d'abord entraîner le modèle.")
        
        # Créer un DataFrame temporaire
        df_temp = pd.DataFrame([donnees])
        X = self.preparer_donnees_maison(df_temp)
        X_scaled = self.scaler_maison.transform(X)
        
        prediction = self.model_maison.predict(X_scaled)[0]
        return max(0, prediction)  # Loyer ne peut pas être négatif
    
    def sauvegarder_modele(self, type_modele):
        """Sauvegarde le modèle et les transformateurs dans le répertoire spécifié"""
        if type_modele == 'terrain':
            joblib.dump(self.model_terrain, self._get_model_path('modele_terrain.joblib'))
            joblib.dump(self.scaler_terrain, self._get_model_path('scaler_terrain.joblib'))
        elif type_modele == 'maison':
            joblib.dump(self.model_maison, self._get_model_path('modele_maison.joblib'))
            joblib.dump(self.scaler_maison, self._get_model_path('scaler_maison.joblib'))
        
        # Sauvegarder les encoders
        if self.encoders:
            joblib.dump(self.encoders, self._get_model_path('encoders.joblib'))
    
    def charger_modele(self, type_modele):
        """Charge le modèle et les transformateurs depuis le répertoire spécifié"""
        try:
            if type_modele == 'terrain':
                self.model_terrain = joblib.load(self._get_model_path('modele_terrain.joblib'))
                self.scaler_terrain = joblib.load(self._get_model_path('scaler_terrain.joblib'))
            elif type_modele == 'maison':
                self.model_maison = joblib.load(self._get_model_path('modele_maison.joblib'))
                self.scaler_maison = joblib.load(self._get_model_path('scaler_maison.joblib'))
            
            # Charger les encoders
            encoders_path = self._get_model_path('encoders.joblib')
            if os.path.exists(encoders_path):
                self.encoders = joblib.load(encoders_path)
                
        except FileNotFoundError as e:
            print(f"Erreur: Modèle non trouvé dans {self.model_dir}. Veuillez d'abord entraîner le modèle. {e}")

    def obtenir_importance_features(self, type_modele):
        """
        Retourne l'importance des features pour le modèle spécifié
        """
        if type_modele == 'terrain' and self.model_terrain is not None:
            feature_names = ['surface', 'acces', 'typePapier', 'pretBatir', 
                           'cloture', 'latitude', 'longitude']
            coefficients = self.model_terrain.coef_
            return dict(zip(feature_names, coefficients))
        elif type_modele == 'maison' and self.model_maison is not None:
            feature_names = ['acces', 'typeMaison', 'type', 'toilette', 
                           'nbChambres', 'latitude', 'longitude']
            coefficients = self.model_maison.coef_
            return dict(zip(feature_names, coefficients))
        return None

if __name__ == "__main__":
    # Initialiser le prédicteur
    predicteur = PredicteurPrixMadagascar()
    
    print("1. Entraînement des modèles")
    print("2. Prédiction de prix")
    choix = input("Choisissez une option (1 ou 2): ")
    
    if choix == "1":
        # Entraîner les modèles (vous devez avoir les fichiers CSV)
        try:
            print("\nEntraînement modèle terrain...")
            predicteur.entrainer_modele_terrain("terrain.csv")
            
            print("\nEntraînement modèle maison...")
            predicteur.entrainer_modele_maison("maison.csv")
            
            print("\nModèles entraînés avec succès!")
        except FileNotFoundError:
            print("Erreur: Fichier CSV non trouvé. Veuillez vérifier les chemins.")
    
    elif choix == "2":
        # Exemple de prédiction
        print("\nPrédiction pour un terrain:")
        prix = predicteur.predire_prix_terrain({
            'surface': 500,
            'acces': 2,
            'typePapier': 'Titre foncier',
            'pretBatir': 'Oui',
            'cloture': 'Non',
            'latitude': -18.8792,
            'longitude': 47.5079
        })
        print(f"Prix prédit: {prix:.2f} Ariary")
    
    else:
        print("Option invalide")