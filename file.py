import os
from .argument import Arg

# Reads a file and creates a list of parameters based on the file
class ParamFile:

    # Constructor for reading the file
    # Takes in a para file
    def __init__ (self, file = "input.para"):

        # Get the file from the directory
        self.path = self.find_file(file)

        # Initialise the arguments and the lines dictionary
        self.args = {}
        self.lines = {}
        
        # Load the file
        self.load_file()



    # Finds a file if it does not exist in the directory
    # Reurns a 'str' if the file is found with the directory to he file
    # Raises an error if no file found.
    def find_file (self, file) -> str:

        # Make sure there is a .para extension if no extension
        if "." not in file:
            file = file + ".para"

        # Walk through the files in the directory looking for the filename
        for subdir, dirs, files in os.walk("."):
            for f in files:
                # If the file exists, return the path
                if f == file:
                    return subdir + "/" + f

        # If no files found, return None and raise an error
        raise FileNotFoundError("No parameter file '%s' exists in root directories." % file)



    # Loads the file and creates the arguments
    def load_file (self):
        with open(self.path) as file:
            for idx, line in enumerate(file.readlines()):
                line = line.strip()

                # Ignore empty lines and comments
                if len(line) < 2:
                    continue
                if line[0] == "#":
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


    # Writes to the file with the current arguments
    def save_file (self):
        filedata = open(self.path, 'r').readlines()

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

            # Update the line
            filedata[line] = new_line

        # Write the lines
        out = open(self.path, 'w')
        out.writelines(filedata)
        out.close()


    # Checks if argument exists
    def exists (self, key):
        return key in self.args.keys()


    # Gets the value of a key
    def arg (self, key):
        if self.exists(key):
            return self.args[key]
        return None


    # Prints all the arguments
    def __str__ (self):
        output = ""
        for arg in self.args.values():
            output += str(arg) + "\n"
        return output