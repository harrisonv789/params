# Import relevant modules
import sys
from .color import Color
from .argument import Arg
from .file import ParamFile

# Class that defines getting the parameters
# This class handles all parameter data and can be used to query data
class Params:


    ############################################################

    '''
    Initialises the class
    @param  kwargs          A list of additional arguments to parse
    '''
    def __init__(self, **kwargs):

        # Load the arguments from the system arguments
        args = sys.argv

        # Get the name of the python script if exists
        self.name = args[0] if len(args) > 0 else "script.py"

        # Load the commands
        self.commands = self.__parse(args[1:]) if len(args) > 1 else {}

        # Update the commands with the kwargs
        for k in kwargs.keys():
            self.commands[k.lower()] = kwargs[k]

        # Get the parameter file to look for
        self.paramfile = self.commands["para"] if "para" in self.commands.keys() else self.name.replace(".py", ".para")

        # Read the parameters file
        self.reader = ParamFile(self.paramfile)

        # If editing the file, edit the commands
        if "edit" in self.commands.keys():
            self.__edit(self.commands["edit"])

        # If saving the file to the system, save all the changes
        if "save" in self.commands and self.commands["save"] == True:
            for com in self.commands.keys():
                # If the command exists, update the value to the one in the commands
                if self.reader.exists(com):
                    self.reader.args[com].value = Arg.convert(self.commands[com])

        # Update the write file
        self.reader.write_file()



    ############################################################

    '''
    Returns the value of a parameter from the system.
    @param  key: str        The key of the parameter to look for
    @param  default         The default value if no key has been found
    @returns                The value from the parameter (as an object)
    '''
    def get (self, key: str, default = None) -> object:

        # Error check
        if key == "":
            raise ValueError("Missing key input from .get function.")

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

        # Returns the default value if missing
        if arg == None and default != None:
            return default

        # Return the argument otherwise
        return "" if arg == None else arg



    ############################################################

    '''
    Returns a list structure from the values of the data. This assumes data is seperated by ,
    @param  key: str        The key of the parameter to look for
    @param  default         The default value if no key has been found
    @param  type            The type to hard cast the values to. Only use if known.
    @returns                The list of values
    '''
    def get_array (self, key: str, default = None, strings = False) -> list:

        # Get the value
        value = self.get(key, default)

        # Check if the type is not a string
        if not strings:

            # Returns the new list of values stripped of white space
            return [Arg.convert(x.strip()) for x in str(value).split(",")]

        # Otherwise return the casted type
        return [str(x.strip()) for x in str(value).split(",")]



    ############################################################

    '''
    Returns a dictionary of all of the values, as passed with a key
    @returns                The dictionary of values
    '''
    def get_all (self) -> dict:

        # Store a dictionary of values
        arg_vals = {}

        # Loop through all of the keys and set the value
        for key in self.reader.args.keys():
            arg_vals[key] = self.reader.arg(key)()

        # Returns the new list
        return arg_vals


    
    ############################################################

    '''
    Returns a list of all parameter keywords that can be usedd
    @returns                The list of key words
    '''
    @property
    def list (self) -> list:
        # Returns the list of keys
        return list(self.reader.args.keys())


    
    ############################################################

    '''
    Parses a list of commands from the system arguments
    @param  args: list      The list of all arguments to parse
    @returns                A dictionary of the commands
    '''
    def __parse (self, args: list) -> dict:
        commands = {}
        com = None

        # Loop through each argument
        for arg in args:

            # Check if current command does not exist
            if com == None:
                if str(arg)[0] == "-":
                    com = str(arg)[1:].lower()
                else:
                    continue
            else:
                if str(arg)[0] == "-":
                    # Attempt to parse a negative number
                    try:
                        float(arg)
                        commands[com] = arg
                        com = None
                    
                    # If failed to turn to number
                    except:
                        # Check for array of values
                        if "," in str(arg):
                            commands[com] = arg
                            com = None

                        # Assume it is a flag
                        else:
                            commands[com] = True
                            com = str(arg)[1:].lower()
                else:
                    commands[com] = arg
                    com = None

        # If still a command remaining
        if com != None:
            commands[com] = True
        
        # Returns the commands
        return commands
            


    ############################################################

    '''
    Displays an interface to edit a parameter file.
    @param  key: str        The key of the parameter to edit. If None, then it will edit all
    '''
    def __edit (self, key = None):

        # Print out a name of the script
        print("------------------------------------------------------------")
        print("%sEDITING %s%s PARAMETER FILE" % (Color.HEADER, self.paramfile, Color.END))
        print("------------------------------------------------------------")

        # Print out the information about skipping
        print("\nHit 'enter' to use default, %s-q%s to stop editing." % (Color.INPUT, Color.END))

        # Loop through each value
        for arg in self.reader.args.values():

            # Check if this is the key needing to edit or if it is editing all keys
            if key == True or key == arg.key:

                # Get options list if exists
                if len(arg.values) > 0 and arg.values[0] != "":
                    options = "\n\tOptions = %s%s%s" % (Color.OPTIONS, arg.values, Color.END)
                else:
                    options = ""

                # Check for using default values
                val = input("\n%sEnter value for %s%s%s (%s%s%s)%s\n\tDefault = %s%s%s: %s" % \
                    (Color.END, Color.PARAM, arg.name, Color.END,
                    Color.PARAM, arg.key, Color.END, options,
                    Color.DEFAULT, str(arg.value), Color.END, Color.INPUT))

                # Check for quit parameters
                if val.lower() in ("-q", "\\"):
                    break

                # Set the new argument
                arg.parse(val)

        # Make sure to reset the colours
        print(Color.RESET)
        print("------------------------------------------------------------\n")



    ############################################################