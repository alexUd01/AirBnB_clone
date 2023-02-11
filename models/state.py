#!/usr/bin/python3
"""A module that contains a class `State` that inherits from BaseModel

Public class attribute:
    name (string) - empty string
"""
from models.base_model import BaseModel
from models.__init__ import storage


# Task 9
class State(BaseModel):
    """A class State that inherits from BaseModel
    """
    name = ''

    def __init__(self):
        """Initialization is passed to BaseModel."""
        super().__init__(self)
