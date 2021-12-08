from unittest import TestCase
from unittest.mock import Mock, patch

from jose import JWTError, jwt

from src.models.db import User
from src.use_case.security_use_case import SecurityUseCase


def solve_path(path: str):
    source = 'src.use_case.security_use_case'
    return ".".join([source, path])


def create_fake_token(data: dict, key: str) -> str:
    try:
        token = jwt.encode(data, key)
        return token
    except JWTError as error:
        raise error


class SecurityUseCaseTestCase(TestCase):

    def setUp(self):
        self.token_secret_key = "13b445dc691051bc13a88d0b97844320"
        self.user_data = dict(name="test@test.co", email="User Test")

    @patch(solve_path('User.save'))
    @patch(solve_path('UserAPI'))
    @patch(solve_path('UserInterface'))
    @patch(solve_path('environ'))
    def test_validate_success(
        self,
        mock_environ: Mock,
        mock_user_interface: Mock,
        mock_user_api: Mock,
        mock_user: Mock
    ):
        mock_environ.get.side_effect = [self.token_secret_key, 'HS256']
        mock_user_interface.find_one.return_value = None
        api_response = dict(data=self.user_data)
        mock_user_api.find_user.return_value = (api_response, False)
        mock_user.return_value = None

        token = create_fake_token(self.user_data, self.token_secret_key)
        result = SecurityUseCase.validate(token)

        self.assertIsInstance(result, User)
