#!/usr/bin/python3
"""A module that contains the base class `BaseModel` of all other models.

It contains common elements:
    attributes: `id`, `created_at` and `updated_at`
    methods: `save()` and `to_json()`

All other classes that would be created will inherit from is base module.
"""
import uuid
from datetime import datetime
from models.__init__ import storage


class BaseModel():
    """ class BaseModel that defines all common attributes/methods
    for other classes:
    """

    def __init__(self, *args, **kwargs):
        """Initializes an instance's attributes."""
        # -> Task 4:
        if len(kwargs) > 0:  # If kwargs is not empty
            for key, val in kwargs.items():
                if key != "__class__":
                    # convert date string value to datetime object
                    if key in ["created_at", "updated_at"] and \
                       type(kwargs[key]) is not datetime:
                        val = datetime.strptime(val, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, val)
        else:  # kwargs is empty
            # -> Task 3:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

            # -> Task 5:
            storage.new(self)

    def __str__(self):
        """Returns a formated string"""
        return "[{}] ({}) {}".format(type(self).__name__, self.id,
                                     self.__dict__)

    def save(self):
        """Updates the public instance attribute updated_at with
        the current datetime
        """
        self.updated_at = datetime.now()

        # Update (Task 5): link BaseModel to FileStorage by using
        # the imported variable `storage`
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of
        __dict__ of the instance.
        """
        new_dict = self.__dict__.copy()

        new_dict["__class__"] = type(self).__name__
        new_dict["created_at"] = datetime.isoformat(new_dict["created_at"])
        new_dict["updated_at"] = datetime.isoformat(new_dict["updated_at"])

        return new_dict
