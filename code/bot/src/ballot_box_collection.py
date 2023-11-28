from telebot import types
from .singleton import SingletonMeta

class BallotBoxCollection(metaclass=SingletonMeta):

    _vote: dict[int,dict[str,list[int]]] = {}
    '''
    _vote :: { (chat_id) -> { (move) -> ([user_id]) } }
    votes :: { (move) -> votes_given }  #TO CHANGE

    _vote has as 
        key the chat id of groups where games are on and
        value a dictionary with
            key the move
            value a userid list of users that voted that move
    '''


    def _getChatAndUser(self, message : types.Message) -> tuple[int,int]:
        userId = message.from_user.id
        chatId = message.chat.id
        return (chatId,userId)


    def _getChatVotes(self, message : types.Message):
        (chat,_) = self._getChatAndUser(message)

        if chat not in self._vote.keys():
            self._vote[chat] = dict()

        return self._vote[chat]


    def add_vote(self, message : types.Message, vote : str) -> None: # TODO valuare utlità di `vote` , posso ottenerlo da message

        """
        Add a vote to a move
        """
        # TODO aggiungere controllo sulla validità di `vote`

        (_,user) = self._getChatAndUser(message)
        votes = self._getChatVotes(message)

        for move in votes:
            if user in votes[move]:
                votes[move].remove(user)

        if vote not in votes.keys():
            votes[vote] = []

        votes[vote].append(user)


    def reset_box(self, message : types.Message):
        """
        Reset votes 
        """

        (chat,_) = self._getChatAndUser(message)
        self._vote.pop(chat)


    def mostVoted(self, message : types.Message):
        (chat,_) = self._getChatAndUser(message)

        if chat not in self._vote.keys():
            self._vote[chat] = ([],dict())

        votes = self._getChatVotes(message)
        return max(votes, key=lambda k: len(votes[k]))
        

