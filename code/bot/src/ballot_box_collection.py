from telebot import types

from utils import getUserAndChatFromMessage
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

    def _getBallotBox(self, ballotbox : int):
        chat = ballotbox

        if chat not in self._vote.keys():
            self._vote[chat] = dict()

        return self._vote[chat]


    def add_vote(self, ballotbox : int, user : int, vote : str) -> None:
        """
        Add a vote to a move
        """

        votes = self._getBallotBox(ballotbox)

        for move in votes:
            if user in votes[move]:
                votes[move].remove(user)

        if vote not in votes.keys():
            votes[vote] = []

        votes[vote].append(user)


    def reset_box(self, ballotbox : int):
        """
        Reset votes 
        """
        self._vote.pop(ballotbox)


    def mostVoted(self, ballotbox : int):

        if ballotbox not in self._vote.keys():
            self._vote[ballotbox] = dict()

        votes = self._getBallotBox(ballotbox)
        return max(votes, key=lambda k: len(votes[k]))
