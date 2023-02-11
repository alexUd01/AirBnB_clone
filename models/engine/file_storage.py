#!/usr/bin/python3
""" A module that contains a class `FileStorage` that serializes
instances to a JSON file and deserializes a JSON file to instances:

file_storage.py -
"""
import json
from datetime import datetime


# Task 5:
class FileStorage():
    """A class that serialies instances to a JSON file and
    deserializes a JSON file to instances:
    """
    # file_path: A string - path to the JSON file (ex: file.json)
    __file_path = "file.json"

    # objects: A dictionary - that but will store all objects by:
    # <class name>.id (ex: to store a BaseModel object with id=12121212,
    # the key will be BaseModel.12121212)
    __objects = dict()

    def __init__(self):
        pass

    def all(self):
        """Returns the dictionary __objects
        """
        # Retrieve previously saved data
        type(self).reload(self)

        new_dict = dict()

        temp = type(self).__objects
        if len(temp) > 0:
            for key in temp.keys():
                tmp_list = key.split('.')
                new_dict[key] = "[{}] ({}) {}".format(tmp_list[0],
                                                      tmp_list[1],
                                                      temp[key])
        return new_dict

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id
        """
        obj_class_name = type(obj).__name__

        # If the attribute `id` is not set, this line below should
        # raise AttributeError
        obj_id = str(getattr(obj, "id"))

        # merge class name and id
        new_key = obj_class_name + "." + obj_id

        # Update dictionary `__objects`
        type(self).__objects[new_key] = obj.__dict__

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)
        """
        FILE_PATH = type(self).__file_path

        # temporary dictionary
        new_dict = self.__objects.copy()

        if len(new_dict) != 0:  # __objects isn't empty
            for key in new_dict.keys():
                new_dict[key] = type(self).to_dict(new_dict[key])
                tmp_list = key.split(sep='.')
                new_dict[key]["__class__"] = tmp_list[0]

        # Write json string to file
        with open(FILE_PATH, mode="w", encoding="utf-8") as fhand:
            json.dump(new_dict, fhand)

    def reload(self):
        """ Deserializes the JSON file to __objects (only if the JSON
        file (__file_path) exists ; otherwise, do nothing. If the
        file doesn't exist, no exception should be raised)
        """
        FILE_PATH = type(self).__file_path

        try:
            with open(FILE_PATH, encoding="utf-8") as fhand:
                temp = json.load(fhand)  # Store json string in temp
        except FileNotFoundError:
            pass  # File does not exist - do nothing
        else:
            new_dict = dict()
            for key in temp.keys():
                new_dict[key] = type(self).from_dict(temp[key])

            type(self).__objects = new_dict

    @staticmethod
    def to_dict(obj):
        """Serializes datetime objects to JSON
        """
        new_dict = obj.copy()

        new_dict["created_at"] = new_dict["created_at"].strftime(
            "%Y-%m-%dT%H:%M:%S.%f")
        new_dict["updated_at"] = new_dict["updated_at"].strftime(
            "%Y-%m-%dT%H:%M:%S.%f")

        return new_dict

    @staticmethod
    def from_dict(obj):
        """Deserializes JSON object to datetime object
        """
        new_dict = obj.copy()

        new_dict["created_at"] = datetime.strptime(new_dict["created_at"],
                                                   "%Y-%m-%dT%H:%M:%S.%f")
        new_dict["updated_at"] = datetime.strptime(new_dict["updated_at"],
                                                   "%Y-%m-%dT%H:%M:%S.%f")

        if hasattr(new_dict, "__class__"):
            del new_dict["__class__"]

        return new_dict

    def destroy(self, class_name, obj_id):
        """A function that deletes an instance based on its
        class name and id
        """
        for key in type(self).__objects.keys():
            if key == class_name + '.' + obj_id:
                del type(self).__objects[key]
                self.save()
                return

        raise AttributeError(
            "'{}' has no instance with id '{}'".format(class_name,
                                                       obj_id))

    def validate_id(self, class_name, obj_id):
        """Check if a valid object id was provided"""
        if class_name + '.' + obj_id not in type(self).__objects.keys():
            return False
        return True

    def update(self, attr, val, class_name, obj_id):
        """A function that updates an instance based on its class
        name and id
        """
        for key in type(self).__objects.keys():
            if key == class_name + '.' + obj_id:
                type(self).__objects[key][attr] = val
                type(self).__objects[key]['updated_at'] = datetime.now()
                self.save()
