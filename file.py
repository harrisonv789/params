import os
from .argument import Arg
from .color import Color

# Class that reads a file and creates a list of parameters based on the file
class ParamFile:


    ############################################################
    # DEFINED CONSTANTS

    # Ignored characters for the param file
    # These are the starting character for a comment line
    IGNORED_CHARS = ('#', '/')
    FILE_ENDING = ".para"



    ############################################################

    # Constructor for reading the file
    # Takes in a para file
    def __init__ (self, file = "input" + FILE_ENDING):

        # Get the file from the directory
        self.path = self.find_file(file)

        # Initialise the arguments and the lines dictionary
        self.args = {}
        self.lines = {}
        
        # Reads the file and parses it into the arguments
        self.read_file(self.path)



    ############################################################

    # Finds a file if it does not exist in the directory
    # Returns a 'str' if the file is found with the directory to he file
    # Raises an error if no file found.
    def find_file (self, file) -> str:

        # Make sure there is a .para extension if no extension
        if "." not in file:
            file = file + self.FILE_ENDING

        # Walk through the files in the directory looking for the filename
        for subdir, dirs, files in os.walk("."):
            for f in files:
                # If the file exists, return the path
                if f == file:
                    return subdir + "/" + f

        # If no files found, ask the user if they want to create a file
        c_in = input("%sWARNING: Unable to find parameter file. Would you like to create one? y/n:%s " % (Color.WARNING, Color.END)).lower()[0]

        # If needing to create a new file
        if c_in == "y":
            self.create_file(file)
            return file

        # Otherwise cancel the script
        else:
            exit()



    ############################################################

    # Reads the file and creates the arguments
    # Takes in a valid path to the file
    # Returns the argyment dictionary created
    def read_file (self, path) -> dict:

        # Make sure the path exists, otherwise raise an error
        if not os.path.exists(path):
            raise FileNotFoundError("File path '%s' does not exist." % path)

        # Opens the file from the current path
        with open(path) as file:

            # Attempt to read the file
            try:
                # Read each of the lines and strip the spaces from the lines
                for idx, line in enumerate(file.readlines()):
                    line = line.strip()

                    # Ignore empty lines and comment lines
                    if len(line) < 2:
                        continue
                    if line[0] in self.IGNORED_CHARS:
                        continue

                    # Read the para
                    info = line.split("|")

                    # Check for invalid lines
                    if len(info) != 5:
                        continue

                    # Remove the spaces in the information
                    info = [i.strip() for i in info]

                    # Create the options list for info [4]
                    opts = [o.strip() for o in info[4].split(",")]

                    # Create the argument
                    arg = Arg(info[0], info[1], info[2], info[3], opts)

                    # Add the argument
                    self.args[arg.key] = arg

                    # Store the line
                    self.lines[idx] = arg.key
            
            # Raise an exception if an invalid file
            except:
                raise Exception("Failed to Parse parameter file.")

        # Returns the argument dictionary
        return self.args



    ############################################################

    # Writes to the file with the current arguments
    def write_file (self, file = None):

        # Check for empty file
        if file == None:
            file = self.path

        # Opens up the current data and create an array of the lines
        filedata = open(file, 'r').readlines()

        # Create the list of data
        data = {}
        for d in self.args.keys():
            data[d] = self.args[d].information

        # Find the length of each column
        lengths = [0] * len(data[d])
        for d in data.values():
            for idx, c in enumerate(d):
                if len(c) > lengths[idx]:
                    lengths[idx] = len(c)
        
        # Format the line
        for line in self.lines.keys():
            arg = self.args[self.lines[line]]

            new_line = ""
            for i in range(0, len(lengths)):
                new_line += arg.information[i] + (" " * (lengths[i] - len(arg.information[i]) + 1)) + "| "

            # Remove the final |
            new_line = new_line[:-2] + "\n"

            # Check if this line is missing (for new files)
            if line >= len(filedata):
                filedata.append(new_line)

            # Update the line
            else:
                filedata[line] = new_line

        # Write the lines to the ouput file
        out = open(file, 'w')
        out.writelines(filedata)
        out.close()



    ############################################################

    # Creates a new parameter file with a list of empty parameters
    def create_file (self, file):

        # Make sure it is a para file
        if "." not in file:
            file = file + self.FILE_ENDING

        # Reset the arguments
        self.args = {}
        self.lines = {}
            
        # Count the lines
        line = 1

        # Ask the user for a new parameter
        while True:
            arg_key = input("\n%sPlease enter a parameter name (%s-q%s to stop): %s" % (Color.END, Color.INPUT, Color.END, Color.INPUT)).lower()

            # Check if quitting the argument
            if arg_key == "-q":
                break

            # Get the default value
            arg_val = input("\t%sEnter value for %s%s%s: %s" % \
                    (Color.END, Color.PARAM, arg_key, Color.END, Color.INPUT))

            # Determine if it is a flag
            arg_flag = str(arg_val.lower()) in ("true", "false")

            # Create the argument
            self.args[arg_key] = Arg(arg_key, arg_key, arg_val, arg_flag, [])
            self.lines[line] = arg_key

            # Increment the line
            line += 1

        # Create an empty file
        with open(file, "w") as f:
            f.write("# New parameter file with some default parameters\n")

        # Write to a new file
        self.write_file(file)

        # Print the parameter file update
        print("\n%sCreated a new parameter file %s%s%s. Please edit all parameters before continuing." % (Color.END, Color.PARAM, file, Color.END))
        exit()



    ############################################################

    # Checks if argument exists
    def exists (self, key) -> bool:
        return key in self.args.keys()



    ############################################################

    # Gets the value of a key
    def arg (self, key):
        if self.exists(key):
            return self.args[key]
        return None



    ############################################################

    # Prints all the arguments
    def __str__ (self):
        output = ""
        for arg in self.args.values():
            output += str(arg) + "\n"
        return output



    ############################################################