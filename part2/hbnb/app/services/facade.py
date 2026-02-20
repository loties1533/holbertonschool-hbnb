from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    """
    Facade pour gérer la logique métier des utilisateurs 
    les autres dépots  pour les taches future
    """
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods

    # créer un utilisateur
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    # récup un utilisateur par ID
    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    # récup un utilisateur par email
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # récup tous les utilisateur
    def get_all_users(self):
        return self.user_repo.get_all()

    # mettre à jour un utilisateur
    def update_user(self, user_id, data):
        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)


# l'instance globale de la façade
facade = HBnBFacade()