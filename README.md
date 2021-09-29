# Params :pencil:

This module is used to read and write parameters to a custom parameter file. It can be used by a script to store parameters of a run that are recorded by a user. It is also able to create and edit parameter files parsed by the script. This module can be interfaced via a python script using the following:

```
from params import Params
```

---

### Intialising :star2:

An instance of the `Params` object must be created at the top of the script, prior to loading the values from the file.

```
params = Params()
```

Any number of arguments can be passed into the constructor. By default, the system will look for a `.para` file within the directory and sub-directories that has the name [FILE].para, where [FILE] is the name of the script being executed. To change the targeted parameter file, use the following argument:

```
params = Params(para = mypara)
```

If no parameter file is found, the module will prompt the user to create a new parameter file with that name, located in the root directory of the script. This will have some default values, but will not provide descriptions or options. Following creating the parameters file, please edit the file for any further options. Alternatively, checkout the [Sample Parameter File](sample.para) provided on how to construct a parameter file. Currently, the `.para` extension must be used.

---

### Getting Values :package:

##### Specific Parameters

To get each parameter, it must be called by the parameter key. This will return an object from the parameters. Current possible object types include **int**, **float**, **bool** and **str**.

```
value = params.get("key")
```

If it is not known whether a parameter has a value in the file yet, a default value can be entered into the command to get the default should it not be registered. The default can be any object type.

```
value = params.get("key", "default")
```
</br>

##### Arrays

Some parameters may have multiple values in the value data. These values must be separated by commas (,) in the parameter file. If this is the case, the values can be parsed by the module using the following function.

```
value = params.get_array("key")
```

This will return a list of all the objects from the value parsed in their correct format. If wanting a list of data that is converted as a string and no other type, use:

```
value = params.get_array("key", strings = True)
```

For data that is not being split by a comma, a different delimiter can be used instead. This parameter can be passed into the function:

```
value = params.get_array("key", delim = ',')
```

A dictionary of all parameters by their key, that returns the value of the parameters, can be fetched using the following function:

</br>

##### All Values

```
all_values = params.get_all()
```

If the params are requested from a class, the parameters can be appended to the class variables by:

```
self.__dict__.update(params.get_all())
```

To get a list of all valid parameters from the file, use the **list** property.

```
keys = params.list
```

---

### Command Line :computer:

Additional commands are able to be entered from the command line. The **-list** flag will display the list of all values from the parameter file in an ordered list.

```
python3 [code].py -list
```

Using the **-edit** flag will open the terminal UI for editing parameter file values. To run this, run the following bash script:

```
python3 [code].py -edit
```

To change the parameter file being referenced by the system, use the **-para** flag:

```
python3 [code].py -para [PARA FILE]
```

Additional changes to parameters can also be appended to the system arguments, which will override the parameters for this run instance. These values will NOT be saved to the parameter file by default, but will be returned from the **get** function.

```
python3 [code].py -key_0 val_0 -key_1 val_1 -key_2 val_2 ...
```

To save the additional parameters from the system arguments to the parameter file, use the **-save** flag:

```
python3 [code].py -key_0 val_0 -key_1 val_1 ... -save
```