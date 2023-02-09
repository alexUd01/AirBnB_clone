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
        if args[0] != "BaseModel":
            print("** class doesn't exist **")
            return

        # Create BaseModule Object
        self.new_base_model = BaseModel()
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
        if args[0] != "BaseModel":
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        # retrieve data from file.json
        self.all_objects = storage.all()

        for key in self.all_objects.keys():
            tmp_list = key.split('.')
            if args[1] == tmp_list[1]:
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
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] != "BaseModel":
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        # Delete object
        try:
            storage.__del__(args[0], args[1])
        except AttributeError:
            print("** no instance found **")
        self.all_objects = storage.all()


        


if __name__ == '__main__':
    HBNBCommand().cmdloop()
