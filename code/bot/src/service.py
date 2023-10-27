"""
This file implements all the service functions that the bot should have.

TODO: Later this should be refactored into a directory with __init__.py so that it can be imported as a module.
TODO: Define the return types of ALL the functions
"""

from singleton import SingletonMeta

class GameMapper(metaclass=SingletonMeta):
    """class used to track all the games that are being played with the bot
    
    This should map something like
    User -> Game
    Game -> User/Channels
    So that the system knows where to send the updates.
    """

    def add(self, game):
        """Adds a game to the list of games

        TODO: define the type of the game

        Args:
            game (Game): the game to add
        """
        pass

    def get(self, game_id: str):
        """Gets a game by its id

        Args:
            game_id (str): the id of the game

        Returns:
            Game: the game that has that id
        """
        pass

    def remove(self, game_id: str):
        """Removes a game from the list of games

        Args:
            game_id (str): the id of the game
        """
        pass

    def get_games_by_user(self, user_id: str):
        """Gets the game that the user is playing

        Args:
            user_id (str): the id of the user

        Returns:
            Game: the list of games that the user is playing
        """
        pass

    def get_user_by_game(self, game_id: str):
        """Gets the user that is playing the game

        Args:
            game_id (str): the id of the game

        Returns:
            User: the user that is playing the game
            Or None if the game is not being played
        """
        pass

def start_game():
    """This function starts a game against a bot

    """

    # 1. Make a request to the backend with the game state
    # 2. Create the game object with the information returned
    # 3. Add the game to the game mapper