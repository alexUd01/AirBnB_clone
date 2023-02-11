#!/usr/bin/python3
"""A module that contains a class `Review` that inherits from BaseModel

Public class attribute:
    place_id: string - empty string: it will be the Place.id
    user_id: string - empty string: it will be the User.id
    text: string - empty string
"""
from models.base_model import BaseModel
from models.__init__ import storage


# Task 9
class Review(BaseModel):
    """A class Review that inherits from BaseModel
    """
    place_id = ''
    user_id = ''
    text = ''

    def __init__(self):
        """Initialization is passed to BaseModel."""
        super().__init__(self)
