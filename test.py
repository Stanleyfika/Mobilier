import pymysql
from pymysql import Error

# Configuration de la base de données
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Mot de passe de votre base de données
    'database': 'Materiel',  # Nom de votre base de données
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

print("Tentative de connexion à la base de données...")

try:
    # Établir la connexion à la base de données
    print("Tentative de connexion avec les paramètres :", db_config)
    connection = pymysql.connect(**db_config)
    print("Connexion établie avec succès !")
    
    # Vérifier si la connexion est réussie
    with connection.cursor() as cursor:
        print("Exécution de la requête SQL...")
        cursor.execute("SELECT version()")
        result = cursor.fetchone()
        print("Version de la base de données :", result)

except Error as e:
    # Afficher l'erreur en cas d'échec de la connexion
    print(f"Erreur de connexion à la base de données : {e}")

except Exception as e:
    # Capturer toute autre exception
    print(f"Une erreur inattendue s'est produite : {e}")

finally:
    # Fermer la connexion à la base de données
    if 'connection' in locals():
        connection.close()
        print("Connexion à la base de données fermée.")