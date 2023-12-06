from .singleton import SingletonMeta


class BallotBoxCollection(metaclass=SingletonMeta):
    _vote: dict[int, dict[str, list[int]]] = {}
    """
    _vote :: { (chat_id) -> { (move) -> ([user_id]) } }
    votes :: { (move) -> votes_given }  #TO CHANGE

    _vote has as 
        key the chat id of groups where games are on and
        value a dictionary with
            key the move
            value a userid list of users that voted that move
    """

    def _getBallotBox(self, ballotbox: int):
        """
        Get the ballotbox of a chat
        """

        if ballotbox not in self._vote.keys():
            self._vote[ballotbox] = dict()

        return self._vote[ballotbox]

    def add_vote(self, ballotbox: int, user: int, vote: str) -> None:
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

    def reset_box(self, ballotbox: int):
        """
        Reset votes
        """
        if ballotbox in self._vote:
            self._vote.pop(ballotbox)

    def mostVoted(self, ballotbox: int):
        """
        Get the most voted moves
        """

        votes = self._getBallotBox(ballotbox)

        if len(votes) == 0:
            return None
        
        max_vote = 0
        most_voted: list[str]= []

<<<<<<< Updated upstream
        for elemento in votes:
            conteggio[elemento] = len(votes[elemento])



        max_freq = max(conteggio.values())
        max_freq_arr: list[str] = [elemento for elemento, frequenza in conteggio.items() if frequenza == max_freq]
=======
        for move in votes.keys():
            if len(votes[move]) > max_vote:
                max_vote = len(votes[move])
                most_voted = [move]
            elif len(votes[move]) == max_vote:
                most_voted.append(move)
>>>>>>> Stashed changes

        else:
            return most_voted
