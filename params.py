# Import relevant modules
from .color import Color
from .argument import Arg
from .file import ParamFile

# Class that defines getting the parameters
# This class handles all parameter data and can be used to query data
class Params:

    # Initialiser takes in a parameter on whether to use defaults at all
    # Pass in sys.argv into the arguments
    def __init__(self, args):

        # Get the name of the python script
        self.name = args[0] if len(args) > 0 else "script"

        # Load the commands
        self.commands = self.parse(args[1:]) if len(args) > 1 else {}

        # Get the file name to look for
        self.file = self.commands["para"] if "para" in self.commands.keys() else self.name.replace(".py", ".para")

        # Read the parameters file
        self.reader = ParamFile(self.file)

        # If editing the file
        if "edit" in self.commands.keys():
            self.edit(self.commands["edit"])

        # Save the file if any changes have been made
        self.reader.save_file()



    # Gets a particular argument
    def get (self, key: str):

        # Error check
        if key == "":
            raise ValueError("Missing key from .get function.")

        # Pass the lower case version
        key = key.lower()
        arg = None

        # Checks if the commands have the argument (use this one instead)
        if key in self.commands.keys():
            arg = Arg.convert(self.commands[key])

        # Read the argument value from file reader if it exists
        else:
            if self.reader.exists(key):
                arg = self.reader.arg(key)()

        # Return the argument
        return "" if arg == None else arg


    
    # Parses the arguments from the command line
    # Turns them into a series of commands for the arguments
    def parse (self, args):
        commands = {}
        com = None

        # Loop through each argument
        for arg in args:
            if com == None:
                if "-" in str(arg):
                    com = str(arg).replace("-", "").lower()
                else:
                    raise ValueError("Incorrect Series of Parameters.")
            else:
                if "-" in str(arg):
                    try:
                        f = float(arg)
                        commands[com] = arg
                        com = None
                    except:
                        commands[com] = True
                        com = str(arg).replace("-", "").lower()
                else:
                    commands[com] = arg
                    com = None

        # If still a command remaining
        if com != None:
            commands[com] = True
        
        # Returns the commands
        return commands
            


    # Asks the user for new values to edit on the files
    # It can take in a key if editing only one key, as opposed to all
    def edit (self, key = None):

        # Print out a name of the script
        print("------------------------------")
        print("%sEDITING %s%s" % (Color.HEADER, self.file, Color.END))
        print("------------------------------")

        # Loop through each value
        for arg in self.reader.args.values():
            if key == True or key == arg.key:

                # Get options list if exists
                if len(arg.values) > 0 and arg.values[0] != "":
                    options = "\n\tOptions = %s" % arg.values
                else:
                    options = ""

                # Check for using default values
                val = input("\n%sEnter value for %s%s%s (%s%s%s)%s\n\tDefault = %s%s%s: %s" % \
                    (Color.END, Color.PARAM, arg.name, Color.END,
                    Color.PARAM, arg.key, Color.END, options,
                    Color.DEFAULT, str(arg.value), Color.END, Color.INPUT))

                # Check for quit parameters
                if val.lower() == "-q":
                    break

                # Set the new argument
                arg.parse(val)

        # Make sure to reset the colours
        print(Color.RESET)
        print("------------------------------\n")