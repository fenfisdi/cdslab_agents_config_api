from src.models.db import User


class UserInterface:

    @staticmethod
    def find_one(email: str) -> User:
        """
        Find User by its email.

        :param email: User email to find.
        """
        filters = dict(
            email=email
        )
        return User.objects(**filters).first()
