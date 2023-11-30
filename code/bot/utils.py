from telebot import types

def getUserAndChatFromMessage(message : types.Message) -> tuple[int,int]:
        userId = message.from_user.id
        chatId = message.chat.id
        return (chatId,userId)


