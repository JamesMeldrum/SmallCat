"""

  TODO: Clean up duplication of GAME_STATES lists between Game and GameStateDelegator

"""


#from menu import 
from gameobjects.engine import GameDataIFace, GamePreferencesIFace
from game_states import Menu, CutScene, Level
import datetime

class Game(GameDataIFace):
  def __init__(self):
    GameDataIFace.__init__(self)
    self.FPS = 60
    self.title = "Small Cat"
    self.date_started = datetime.date(2013,1,5)
    self.GAME_STATES = [('MENU', Menu),('LEVEL', Level),('CUTSCENE', CutScene)]
    self.game_state_delegator = GameStateDelegator(self)

  def start(self):
    super(Game,self).start()
    self.current_state = self.GAME_STATES[0]
    self.game_state_delegator.new_state(self.GAME_STATES[0][1])

  def tick(self,game_data_object):
    super(Game,self).tick(game_data_object)
    self.game_state_delegator.tick(game_data_object)

    """

    Game Loop:
      * Move object on stage
      * Read game data object

    """

class GameStateDelegator(object):
  """
    Manages instantiating and deconstructing the game states
  """

  def __init__(self,game_ref):
    self.GAME_STATES = [('MENU', Menu),('LEVEL', Level),('CUTSCENE', CutScene)]
    self.current_state = None
    self.game_ref = game_ref

  def tick(self, game_data_object):
    self.current_state.tick(game_data_object)

  def new_state(self, state):
    if self.current_state is not None:
      self.del_state(self.current_state) # Deletes itself
    self.current_state = state(self.game_ref,self)

  def del_state(self,state):
    state.deconstruct()

  def prev_state(self, CURRENT_STATE):
    self.new_state(self.GAME_STATES[CURRENT_STATE-1][1])

  def next_state(self, CURRENT_STATE):
    self.new_state(self.GAME_STATES[CURRENT_STATE+1][1])

class GamePreferences(GamePreferencesIFace):
  def __init__(self):
    GamePreferencesIFace.__init__(self)
    self.game_log.write("Game Log Handled by subclass")
