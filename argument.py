# This is a class that stores information about a particular argument
class Arg:

    ############################################################

    # Constructor for initialising the constructor
    # Takes in a key, name, a default value and a list of possible values (optional)
    def __init__ (self, key, name, default, flag = False, values=[]):
        self.key = str(key).lower()
        self.name = name
        self.default = Arg.convert(default)
        self.flag = flag != "" and flag != False
        self.values = values
        self.options = len(values) > 0 and values[0] != ""
        self.value = self.default



    ############################################################

    # Parses a value for the parameter and returns the value
    def parse (self, value):

        # Checks if there are possible values
        if self.options:
            # Makes sure the value exists
            if value in self.values:
                self.value = value
            else:
                self.value = self.default

            return self.value

        # Determine the return based on type
        if value == "":
            self.value = self.default
        elif value.lower() in ("t", "f", "true", "false"):
            self.value = value.lower()[0] == "t"
        elif type(self.default) is int:
            self.value = int(value)
        elif type(self.default) is float:
            self.value = float(value)
        else:
            self.value = value
        
        # Returns the value
        return self.value



    ############################################################
    
    # Gets the value from the argument call
    def __call__ (self, *args, **kwds):
        return self.value



    ############################################################

    # Converts the argument to a string
    def __str__ (self):
        return "Key: %s   Name: %s   Default: %s   Flag: %s    Options: %s   Value: %s" \
            % (self.key, self.name, self.default, self.flag, self.values, self.value)


    ############################################################

    # Converts the argument to file
    @property
    def information (self):
        flag = "flag" if self.flag else ""

        # Format the options
        options = ""
        for idx, o in enumerate(self.values):
            if idx < len(self.values) - 1:
                options += o + ", "
            else:
                options += o
        
        return [str(self.key), str(self.name), str(self.value), flag, options]



    ############################################################

    # Reads a value and stores it of the correct type
    @staticmethod
    def convert (value):
        # For float nad integers
        if str(value).isnumeric():
            if "." in value:
                return float(value)
            else:
                return int(value)

        # Try to convert a float
        try:
            return float(value)
        except:
            pass
        
        # For booleans
        if str(value).lower() in ("t", "f", "true", "false"):
            return str(value).lower()[0] == "t"

        # For strings
        return value


    
    ############################################################