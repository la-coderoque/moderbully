from aiogram import Router

from middlewares.register import GroupRegisterCheck


def register_middlewares(router: Router) -> None:
    router.message.middleware(GroupRegisterCheck())
    router.callback_query.middleware(GroupRegisterCheck())
