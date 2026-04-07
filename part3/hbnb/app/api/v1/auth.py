from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from flask import request
from app.models.user import User  # Import direct pour le debug SQL

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        email = credentials.get('email', '').strip()
        password = credentials.get('password', '')

        # --- DEBUG TOTAL DE LA BASE ---
        print("\n--- 🔍 SCAN DE LA BASE DE DONNÉES ---")
        try:
            all_users = User.query.all()
            print(f"Nombre d'utilisateurs en base : {len(all_users)}")
            for u in all_users:
                print(f" - Trouvé : '{u.email}' (ID: {u.id})")
        except Exception as e:
            print(f"❌ Erreur lors du scan SQL : {e}")
        
        user = User.query.filter_by(_email=email).first()

        if not user:
            user = User.query.filter_by(email=email).first()
        
        print(f"Recherche de '{email}' -> {'✅ TROUVÉ' if user else '❌ NON TROUVÉ'}")
        
        if user:
            is_valid = user.verify_password(password)
            print(f"Vérification mot de passe : {'✅ VALIDE' if is_valid else '❌ INVALIDE'}")
        print("--------------------------------------\n")
        # --- FIN SECTION DEBUG ---

        # Vérification et réponse
        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        
        return {'access_token': access_token}, 200