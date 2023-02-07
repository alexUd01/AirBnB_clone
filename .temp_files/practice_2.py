#!/usr/bin/python3
import cmd
import sys

class AClass(cmd.Cmd):

    prompt = "(practice2) "
    cmdqueue = ["ls", "adsf", "faddsf"]

    def preloop(self):
        print("Don't stop")
    def postloop(self):
        print("Loop exitted.")

    def do_quit(self, x=0):               # Handles `quit` command
        """Exits from the program.
        """
        print("--> Program Exitted...")
        self.postloop()
        sys.exit(x)

    def help_quit(self):
        print("Exit")

    def do_shell(self, line):         # Handles `!` character
        """Handles `!` character (which runs shell commands)
        """
        print("--> Executing shell command", line)
        import os
        output = os.popen(line).read()  # pass `!clear` to the shell to see the magic
        print(output)

    def emptyline(self):
        pass

    def default(self, line):
        print("You made an error at line: <line_num>.",
              "Unrecognized command {}".format(line))

    def do_displayrandomnumbers(self, start=None):
        """Displays 20 `1`s 
        """
        print("1" * 20)

    def do_echo(self, *args):
        """does almost the same as echo in bash.
        """
        print(*args)

    def complete_echo(self, text, line, begidx, endidx):
        """completes echo command.
        """
        LIST = ["Name", "Age", "Sex", "Occupation", "Tribe", "Nationality", "etc"]
        if not text:
            completions = LIST[:]
        else:
            completions = [item for item in LIST if item.startswith(text)]

        return completions

    def do_EOF(self, line):  # Very important (It handles infinite loop error)
        """Exit from the program.
        """
        return True

x = AClass()
x.cmdloop(intro="Hello, Welcome once again.")
