#!/usr/bin/python3
""" A module containing a command interpreter which will be used to
create objects, manage objects, update objects, store objects to a JSON file
and destroy objects.

It will be used (in conjunction with the front-end and RestAPI) to effectively
and efficiently manipulate the entire storage system.
"""
import cmd
import sys


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


if __name__ == '__main__':
    HBNBCommand().cmdloop()
