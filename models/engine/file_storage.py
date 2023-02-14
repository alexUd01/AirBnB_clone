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
    __objects = {}

    def all(self):
        """Returns the dictionary __objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    @staticmethod
    def classes():
        """Returns a dictionary of valid classes and their references"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review
                   }
        return classes

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)
        """
        FILE_PATH = FileStorage.__file_path

        # temporary dictionary
        new_dict = FileStorage.__objects.copy()

        for key, val in new_dict.items():
            tmp_list = key.split(sep='.')
            new_dict[key] = val.to_dict()
            new_dict[key]["__class__"] = tmp_list[0]

        # Write json string to file
        with open(FILE_PATH, mode="w", encoding="utf-8") as fhand:
            json.dump(new_dict, fhand)

    def reload(self):
        """ Deserializes the JSON file to __objects (only if the JSON
        file (__file_path) exists ; otherwise, do nothing. If the
        file doesn't exist, no exception should be raised)
        """
        FILE_PATH = FileStorage.__file_path

        try:
            with open(FILE_PATH, encoding="utf-8") as fhand:
                temp = json.load(fhand)  # Store json string in temp
        except FileNotFoundError:
            pass  # File does not exist - do nothing
        else:
            new_dict = {k: self.classes()[v["__class__"]](**v)
                        for k, v in temp.items()}

            FileStorage.__objects = new_dict

    def destroy(self, class_name, obj_id):
        """A function that deletes an instance based on its
        class name and id
        """
        for key in FileStorage.__objects.keys():
            if key == class_name + '.' + obj_id:
                del FileStorage.__objects[key]
                self.save()
                return

        raise AttributeError(
            "'{}' has no instance with id '{}'".format(class_name,
                                                       obj_id))

    def validate_id(self, class_name, obj_id):
        """Check if a valid object id was provided"""
        if class_name + '.' + obj_id not in FileStorage.__objects.keys():
            return False
        return True

    def update(self, attr, val, class_name, obj_id):
        """A function that updates an instance based on its class
        name and  id
        """
        try:
            val = int(val)
        except Exception:
            pass

        for key in FileStorage.__objects.keys():
            if key == class_name + '.' + obj_id:
                # Only create new instance when there's no self.new_obj
                if getattr(self, 'new_obj', -100) == -100 or \
                   self.new_obj is None:
                    self.new_obj = self.classes()[class_name]()
                    setattr(self.new_obj, 'id', obj_id)

                # then set attr/val
                setattr(self.new_obj, attr, val)
                # set `updated_at`/`created_at`
                if not hasattr(self.new_obj, 'created_at'):
                    setattr(self.new_obj, 'created_at', datetime.now())
                    setattr(self.new_obj, 'updated_at', new_obj.created_at)
                else:
                    setattr(self.new_obj, 'updated_at', datetime.now())

                # assign new_obj to matched value
                FileStorage.__objects[key] = self.new_obj

                # Save changes
                FileStorage.save(self)
                return
