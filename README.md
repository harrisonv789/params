# Params :pencil:

Used to read and write to custom parameter files for editing scripts in the command line and through a Python interface. It can be added to any python script by importing the following module:

```
import sys
from params import Params
```

First, you must initialise the Param object by a constructor and pass in the arguments from the command line. These will include the name of the script and any other additional arguments.

```
params = Params(sys.argv)
```

To get each parameter, simply call it as a key. This will return an object from the parameters. Possible object types include **int**, **float**, **bool** and **string**.

```
value = params.get("key")
```
---
### Note :warning:
Currently, invalid ***.para*** files cannot be read or created. See the **sample.para** parameter file for more information on how to construct a new parameter file. This file can then be copied to the directory where the script is being run from with new parameters.