from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.repo.transactions import TransactionRepo
from infrastructure.database.repo.users import UserRepo
from infrastructure.database.setup import create_engine


@dataclass
class RequestsRepo:
    """
    Repository for handling database operations. This class holds all the repositories for the database models.

    You can add more repositories as properties to this class, so they will be easily accessible.
    """

    session: AsyncSession

    @property
    def users(self) -> UserRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return UserRepo(self.session)

    @property
    def transactions(self) -> TransactionRepo:
        """
        The Transaction repository sessions are required to manage transaction operations.
        """
        return TransactionRepo(self.session)
