import random


class Color(object):
  WHITE = 0
  BLACK = 1


class Player(object):
  def __init__(self, color):
    self.color = color

  @property
  def move(self):
    move = raw_input("Please enter your move: ")
    # We need to specify this more clearly
    pass
