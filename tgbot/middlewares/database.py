import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, Update

from infrastructure.database.repo.requests import RequestsRepo


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool) -> None:
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            repo = RequestsRepo(session)
            event_from_user = data.get("event_from_user")

            user = await repo.users.get_or_create_user(
                event_from_user.id,
                event_from_user.full_name,
                event_from_user.language_code,
                event_from_user.username,
            )
            result = await repo.users.get_user_by_id(user.user_id)
            logging.info(f"User: {dict(result)}")
            data["repo"] = repo
            data["user"] = user

            result = await handler(event, data)
        return result
