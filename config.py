import os


class Config:
    """Classe de configuration de base."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'une_clé_secrète_par_défaut')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'Mobilier')
    
class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False  # Désactive le mode débogage en production

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True  # Active le mode de débogage

class TestingConfig(Config):
    """Configuration pour les tests"""
    DEBUG = False
    TESTING = True  # Active le mode test pour une gestion plus stricte des erreurs