from telebot import types
from .singleton import SingletonMeta

class DoubleVoteError(Exception):
    def __init__(self, message='Already voted'):
        self.message = message
        super().__init__(message)

class VoteMapper(metaclass=SingletonMeta):

    _vote: dict[int,tuple[list[int],dict[str,int]]] = {}
    '''
    _vote :: { (game_id) -> ([username],votes) }
    votes :: { (move) -> votes_given }

    _vote has as 
        key the chat id of groups where games are on and
        value a tuple of
            a userid list, for avoid double vote
            a dictionary with
                key the move
                value number of votes received for that move
    '''


    def _getChatAndUser(self, message : types.Message) -> tuple[int,int]:
        userId = message.from_user.id
        chatId = message.chat.id
        return (chatId,userId)


    def _getChatVotes(self, message : types.Message):
        (chat,user) = self._getChatAndUser(message)

        if chat not in self._vote.keys():
            self._vote[chat] = ([],dict())

        return self._vote[chat]


    def add(self, message : types.Message, vote : str) -> None:

        """
        Add a vote to a move
        """
        (_,user) = self._getChatAndUser(message)
        (voters,votes) = self._getChatVotes(message)

        if user in voters:
            raise DoubleVoteError()

        
        voters.append(user)
        if vote not in votes.keys():
            votes[vote] = 0

        votes[vote] += 1


    def reset(self, message : types.Message):
        """
        Reset votes 
        """

        (chat,_) = self._getChatAndUser(message)
        self._vote.pop(chat)


    def mostVoted(self, message : types.Message):
        (chat,_) = self._getChatAndUser(message)

        if chat not in self._vote.keys():
            self._vote[chat] = ([],dict())

        (voters,votes) = self._getChatVotes(message)
        return max(votes, key=lambda k: votes[k])
        

