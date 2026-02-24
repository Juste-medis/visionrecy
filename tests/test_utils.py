import unittest
from app.routes.auth.utils import validate_login, validate_registration
from app.models.user import User
from werkzeug.security import generate_password_hash
from unittest.mock import patch, MagicMock


class TestAuthUtils(unittest.TestCase):

    @patch('app.routes.auth.utils.User')
    def test_validate_login_success(self, mock_user):
        # Simuler un utilisateur existant
        mock_user_instance = MagicMock()
        mock_user_instance.password = generate_password_hash('password123')
        mock_user.query.filter_by().first.return_value = mock_user_instance

        user, error = validate_login('test@example.com', 'password123')
        self.assertIsNotNone(user)
        self.assertIsNone(error)

    @patch('app.routes.auth.utils.User')
    def test_validate_login_invalid_credentials(self, mock_user):
        # Simuler un utilisateur inexistant
        mock_user.query.filter_by().first.return_value = None

        user, error = validate_login('test@example.com', 'password123')
        self.assertIsNone(user)
        self.assertEqual(error, "Email ou mot de passe incorrect")

    def test_validate_login_missing_fields(self):
        user, error = validate_login('', '')
        self.assertIsNone(user)
        self.assertEqual(error, "Email et mot de passe requis")

    @patch('app.routes.auth.utils.User')
    def test_validate_registration_success(self, mock_user):
        # Simuler que l'utilisateur n'existe pas encore
        mock_user.query.filter_by().first.return_value = None

        user, error = validate_registration(
            'newuser', 'new@example.com', 'password123')
        self.assertIsNotNone(user)
        self.assertIsNone(error)

    # @patch('app.routes.auth.utils.User')
    # def test_validate_registration_existing_username(self, mock_user):
    #     # Simuler un nom d'utilisateur existant
    #     mock_user.query.filter_by(
    #         username='existinguser').first.return_value = MagicMock()
    #     mock_user.query.filter_by(
    #         email='new@example.com').first.return_value = None

    #     user, error = validate_registration(
    #         'existinguser', 'new@example.com', 'password123')
    #     self.assertIsNone(user)
    #     self.assertEqual(error, "Cet nom d'utilisateur est déjà utilisé")

    # @patch('app.routes.auth.utils.User')
    # def test_validate_registration_existing_email(self, mock_user):
    #     # Simuler un email existant
    #     mock_user.query.filter_by(username='newuser').first.return_value = None
    #     mock_user.query.filter_by(
    #         email='existing@example.com').first.return_value = MagicMock()

    #     user, error = validate_registration(
    #         'newuser', 'existing@example.com', 'password123')
    #     self.assertIsNone(user)
    #     self.assertEqual(error, "Cet email est déjà utilisé")

    # def test_validate_registration_missing_fields(self):
    #     user, error = validate_registration('', '', '')
    #     self.assertIsNone(user)
    #     self.assertEqual(error, "Tous les champs sont requis")


if __name__ == '__main__':
    unittest.main()
