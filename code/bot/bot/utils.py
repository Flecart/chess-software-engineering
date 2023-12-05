from telebot import types


def get_user_and_chat_from_message(message: types.Message) -> tuple[int, int]:
    user_id = message.from_user.id
    chat_id = message.chat.id
    return (chat_id, user_id)

