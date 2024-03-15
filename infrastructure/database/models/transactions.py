from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DECIMAL, ForeignKey, String
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TableNameMixin, TimestampMixin, int_pk

# Additional imports for type annotations and utilities
if TYPE_CHECKING:
    from .users import User


class TransactionType(Enum):
    TOPUP = "topup"
    EXPENDITURE = "expenditure"


class Transaction(Base, TableNameMixin, TimestampMixin):
    """
    This class represents a financial transaction, which could be a top-up or an expenditure.

    Attributes:
        transaction_id (Mapped[int]): The unique identifier of the transaction.
        user_id (Mapped[int]): Foreign key linking to the User table.
        amount (Mapped[float]): The amount of the transaction.
        type (Mapped[TransactionType]): The type of the transaction (top-up or expenditure).
        description (Mapped[Optional[str]]): An optional description of the transaction.

    Relationships:
        user: A relationship to the User who performed the transaction.
    """

    transaction_id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    amount: Mapped[Decimal] = mapped_column(DECIMAL(16, 8))
    type: Mapped[TransactionType]
    description: Mapped[Optional[str]]

    user: Mapped["User"] = relationship("User", back_populates="transactions")
