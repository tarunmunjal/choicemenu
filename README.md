# Class Choice Menu
## Description

This packages can be used to provide a choice menu so that the executing user can select from a list of options provided to them.

Incoming object can be a list, tuple or a dictionary object. Once the choice is made, a list or dict object will be returned, based upon input object. The script will create and show a menu for user to choose, from the items in the input object. User has the option to choose all by selecting 0 or they can specify one or more comma separated `int` values `e.g 1,3,5,7,9`. The option to select multiple values or all values is setup by default. To prevent users from selecting multiple items you can set multichoice to false.

## Arguments
The Class takes following three arguments: 
- input_object (REQUIRED) python list, tuple or dict object containing items to choose from.
- multichoice (OPTIONAL) Default is `True`. Set it to `False` if only one item is allowed from the choice.
- maxtries (OPTIONAL) Default is 10. Keep asking the user for valid input for this manu times before raising exception.

## Example
Please see class module.

# Choice Menu in action screenshot
![placehoder text](images/choicemenudemo.png)
