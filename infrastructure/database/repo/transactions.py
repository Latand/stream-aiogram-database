from re import I
from typing import Optional

from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import Transaction
from infrastructure.database.models.transactions import TransactionType
from infrastructure.database.repo.base import BaseRepo


class TransactionRepo(BaseRepo):
    async def create_transaction(
        self,
        user_id: int,
        amount: float,
        type: TransactionType,
        description: Optional[str] = None,
    ):
        """
        Creates a new transaction in the database and returns the transaction object.
        :param user_id: The user's ID.
        :param amount: The amount of the transaction.
        :param type: The type of the transaction.
        :param description: An optional description of the transaction.
        :return: Transaction object, None if there was an error while making a transaction.
        """

        insert_stmt = (
            insert(Transaction)
            .values(
                user_id=user_id,
                amount=amount,
                type=type,
                description=description,
            )
            .returning(Transaction)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()
