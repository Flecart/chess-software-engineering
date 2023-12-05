from telebot import types


def get_user_and_chat_from_message(message: types.Message) -> tuple[int, int]:
    user_id = message.from_user.id
    chat_id = message.chat.id
    return (chat_id, user_id)


def pretty_print_time(td):
    parts = []
    if td.days > 0:
        parts.append(f"{td.days} giorni")
    hours = td.seconds // 3600
    if hours > 0:
        parts.append(f"{hours} ore")
    minutes = (td.seconds % 3600) // 60
    if minutes > 0:
        parts.append(f"{minutes} minuti")
    seconds = td.seconds % 60
    if seconds > 0:
        parts.append(f"{seconds} secondi")
    return " ".join(parts)
