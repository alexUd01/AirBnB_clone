#!/usr/bin/python3
"""A module that contains a class `User` that inherits from BaseModel

Public class attributes:
    email (string) - empty string
    password (string) - empty string
    first_name (string) - empty string
    last_name (string) - empty string
"""
from models.base_model import BaseModel
from models.__init__ import storage


# Task 8
class User(BaseModel):
    """A class User that inherits from BaseModel
    """
    email = ''
    password = ''
    first_name = ''
    last_name = ''

    def __init__(self):
        """Initialization is passed to BaseModel."""
        super().__init__(self)
