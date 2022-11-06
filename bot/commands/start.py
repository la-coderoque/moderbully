from aiogram import types


async def start_command(message: types.Message) -> None:
    await message.answer(
        f'Hello {message.from_user.first_name}',
    )
