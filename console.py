#!/usr/bin/python3
""" A module containing a command interpreter which will be used to
create objects, manage objects, update objects, store objects to a JSON file
and destroy objects.

It will be used (in conjunction with the front-end and RestAPI) to effectively
and efficiently manipulate the entire storage system.
"""
import cmd
import sys
from models.base_model import BaseModel
from models.base_model import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


# Task 6: Console 0.0.1
class HBNBCommand(cmd.Cmd):
    """The entry point of the command interpreter:
    """
    prompt = "(hbnb) "

    def do_EOF(self, line):
        """Exits the program cleanly (^D / CTRL + D).
        """
        return True

    def do_quit(self, line):
        """Quit command to exit the program
        """
        sys.exit(0)

    def emptyline(self):
        """an empty line + ENTER shouldn't execute anything
        """
        pass

    # Task 7: Update: Console 0.1
    def do_create(self, line):
        """Creates a new instance of BaseModel, saves it (to the
        JSON file) and prints the id.
            Ex: $ create BaseModel
                de2f8cb7-8841-4721-862a-7a1ab15755a5

        If the class name is missing, print ** class name missing **
            Ex: $ create
                ** class name missing **

        If the class name doesn't exist, print ** class doesn't exist **
            Ex: $ create MyModel
                ** class doesn't exist **
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return

        # --> Create Instances
        if args[0] == "BaseModel":
            self.new_base_model = BaseModel()
        # Create a User instance
        elif args[0] == "User":
            self.new_base_model = User()
        # Create a Place instance
        elif args[0] == "Place":
            self.new_base_model = Place()
        # Create a State instance
        elif args[0] == "State":
            self.new_base_model = State()
        # Create a City instance
        elif args[0] == "City":
            self.new_base_model = City()
        # Create an Amenity instance
        elif args[0] == "Amenity":
            self.new_base_model = Amenity()
        # Create a Review instance
        elif args[0] == "Review":
            self.new_base_model = Review()
        else:
            print("** class doesn't exist **")
            return

        self.new_base_model.save()
        print(self.new_base_model.id)

    def do_show(self, line):
        """Prints the string representation of an instance based on
        the class name and id.
            Ex: $ show BaseModel 49faff9a-6318-451f-87b6-910505c55907
                [BaseModel] (49faff9a-6318-451f-87b6-910505c55907)
                {'first_name': 'Betty', 'id': '49faff9a-6318-451f
                -87b6-910505c55907', 'created_at':datetime.datetime(
                2017, 10, 2, 3, 10, 25, 903293), 'updated_at': datetime
                .datetime(2017, 10, 2, 3, 11, 3, 49401)}

        If the class name is missing, print ** class name missing **
            Ex: $ show
               ** class name missing **

        If the class name doesn't exist, print ** class doesn't exist **
            Ex: $ show MyModel
               ** class doesn't exist **

        If the id is missing, print ** instance id missing **
            Ex: $ show BaseModel
                ** instance id missing **

        If the instance of the class name doesn't exist for the id,
        print ** no instance found **
            Ex: $ show BaseModel 121212
                ** no instance found **
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in ["BaseModel", "User", "Place", "State",
                           "City", "Amenity", "Review"]:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        # retrieve data from file.json
        self.all_objects = storage.all()

        for key in self.all_objects.keys():
            if key == args[0] + '.' + args[1]:
                print(self.all_objects[key])  # Print the attributes
                return

        # Has no attribute `id`
        print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
        and save the change into the JSON file.
            Ex: $ destroy BaseModel 1234-1234-1234.
                $ show BaseModel 1234-1234-1234.
                ** no instance found **
                $ destroy BaseModel 1234-1234-1234.
                ** no instance found **
        Same rule applies as it was in do_create() and do_show().
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in ["BaseModel", "User", "Place", "State",
                           "City", "Amenity", "Review"]:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        # Delete object
        try:
            # `storage.destroy()` automatically writes changes to file.json
            storage.destroy(args[0], args[1])
        except AttributeError:
            print("** no instance found **")
        else:
            # Refresh current dictionary
            self.all_objects = storage.all()

    def do_all(self, line):
        """Prints all string representation of all instances based
        or not on the class name.
            Ex: $ all BaseModel
                <some data about BaseModel is printed>
                $ all.
                <some data about BaseModel is printed>

        The printed result must be a list of strings (like the
        example below). If the class name doesn't exist, print
        ** class doesn't exist **
            Ex: $ all MyModel
                ** class doesn't exist **
        """
        args = line.split()

        # retrieve data from file.json
        self.all_objects = storage.all()

        if len(args) == 0:  # only `all` was entered
            for key in self.all_objects.keys():
                print(self.all_objects[key])
            return

        # NOTE: If checker fails, make all universal
        if len(args) >= 1:
            # I used for loop to iterate through the args because,
            # in the future, I want it to process not only args[0]
            # but others passed.
            for arg in args:
                type(self).print_class_objects(self, arg)
                break

    @staticmethod
    def print_class_objects(self, cls_name):
        """A helper method that prints all available class objects
        """
        current_classes = ["BaseModel", "User", "Place", "State",
                           "City", "Amenity", "Review"]

        if cls_name not in current_classes:
            print("** class doesn't exist **")
            return

        for key in self.all_objects.keys():
            if key.startswith(cls_name + '.'):
                print(self.all_objects[key])

    def do_update(self, line):
        """Updates an instance based on the class name and id
        by adding or updating attribute (save the change into
        the JSON file).
            Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com".

        Usage:
            update <class name> <id> <attribute name> "<attribute value>"

        - Only one attribute can be updated at the time
        - You can assume the attribute name is valid (exists for
          this model)
        - The attribute value must be casted to the attribute type
        - If the class name is missing, print ** class name missing **
            Ex: $ update

        If the class name doesn't exist, print ** class doesn't exist **
            Ex: $ update MyModel

        If the id is missing, print ** instance id missing **
            Ex: $ update BaseModel

        If the instance of the class name doesn't exist for the
        id, print ** no instance found **
            Ex: $ update BaseModel 121212

        If the attribute name is missing, print ** attribute name missing **
            Ex: $ update BaseModel existing-id

        If the value for the attribute name doesn't exist,
        print ** value missing **
            Ex: $ update BaseModel existing-id first_name

        All other arguments should not be used
            Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com" \
first_name "Betty" = $ update BaseModel 1234-1234-1234 \
email "aibnb@mail.com")

        id, created_at and updated_at can't be updated. You can assume
        they won't be passed in the update command.

        Only "simple" arguments can be updated: string, integer and
        float.
        You can assume nobody will try to update list of ids or datetime
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in ["BaseModel", "User", "Place", "State",
                           "City", "Amenity", "Review"]:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        if storage.validate_id(args[0], args[1]) is False:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        # group quoted values
        val = ""
        if args[3].startswith('"'):
            for arg in args[3:]:
                val = val + ' ' + arg
                if arg.endswith('"'):
                    break
        # If the last arg has no closing quote, then val = args[3] only
        if not val.endswith('"'):
            val = args[3]
        else:
            val = val.strip(' ')
            val = val.strip('"')

        # Update object
        storage.update(args[2], val, args[0], args[1])
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
