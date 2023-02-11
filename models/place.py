#!/usr/bin/python3
"""A module that contains a class Place that inherits from BaseModel

Public class attribute:
    city_id: string - empty string: it will be the City.id
    user_id: string - empty string: it will be the User.id
    name: string - empty string
    description: string - empty string
    number_rooms: integer - 0
    number_bathrooms: integer - 0
    max_guest: integer - 0
    price_by_night: integer - 0
    latitude: float - 0.0
    longitude: float - 0.0
    amenity_ids: list of string - empty list: it will be the list of
                 Amenity.id later
"""
from models.base_model import BaseModel
from models.__init__ import storage


# Task 9
class Place(BaseModel):
    """A class Place that inherits from BaseModel
    """
    city_id = ''
    user_id = ''
    name = ''
    description = ''
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = list()

    def __init__(self):
        """Initialization is passed to BaseModel."""
        super().__init__(self)
