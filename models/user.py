from database import get_db_connection

class User:
    def __init__(self, idUser, pseudo, motdepasse):
        self.idUser = idUser
        self.pseudo = pseudo
        self.motdepasse = motdepasse

    # Getter et Setter pour chaque attribut
    @property
    def idUser(self):
        return self._idUser

    @idUser.setter
    def idUser(self, value):
        self._idUser = value

    @property
    def pseudo(self):
        return self._pseudo

    @pseudo.setter
    def pseudo(self, value):
        self._pseudo = value

    @property
    def motdepasse(self):
        return self._motdepasse

    @motdepasse.setter
    def motdepasse(self, value):
        self._motdepasse = value

    @staticmethod
    def login(pseudo, mdp):
        """Authentifie un utilisateur et retourne ses informations."""
        connection = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                # Requête paramétrée pour éviter les injections SQL
                sql = "SELECT * FROM User WHERE Pseudo = %s AND Motdepasse = %s"
                cursor.execute(sql, (pseudo, mdp))
                user = cursor.fetchone()  # Récupère le premier résultat
                return user  # Retourne l'utilisateur (dictionnaire) ou None
        except Exception as e:
            print(f"Erreur d'authentification : {e}")
            return None
        finally:
            if connection:
                connection.close()