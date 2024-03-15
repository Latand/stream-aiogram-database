from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import User, Transaction
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        user_id: int,
        full_name: str,
        language: str,
        username: Optional[str] = None,
    ):
        """
        Creates or updates a new user in the database and returns the user object.
        :param user_id: The user's ID.
        :param full_name: The user's full name.
        :param language: The user's language.
        :param username: The user's username. It's an optional parameter.
        :return: User object, None if there was an error while making a transaction.
        """

        insert_stmt = (
            insert(User)
            .values(
                user_id=user_id,
                username=username,
                full_name=full_name,
                language=language,
            )
            .on_conflict_do_update(
                index_elements=[User.user_id],
                set_=dict(
                    username=username,
                    full_name=full_name,
                ),
            )
            .returning(User)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()

    async def get_user_by_id(self, user_id: int):
        """
        Retrieves a user from the database by their ID.
        :param user_id: The user's ID.
        :return: User object, None if the user was not found.
        """
        select_stmt = select(
            User.user_id,
            User.full_name,
            func.sum(Transaction.amount).label("balance"),
        ).where(User.user_id == user_id)
        result = await self.session.execute(select_stmt)
        return result.scalar_one()
