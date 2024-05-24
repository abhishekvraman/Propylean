class _Validators(object):
    @classmethod
    def validate_arg_prop_value_type(cls, arg_prop_name, value, correct_types):
        """
        DESCRIPTION:
            Function to validate values passed to properties or args is of
            of correct types.
        PARAMETERS:    
            arg_prop_name:
                Required: Yes
                Type: String  
                Description: Name of the argument or property.
            value:
                Required: Yes
                Type: Any 
                Description: Value of the argument or property.
            correct_types:
                Required: Yes
                Type: Tuple
                Description: Correct types of the argument or property.
        """
        if value is not None and not isinstance(value, correct_types):
            if isinstance(correct_types, tuple):
                correct_types = tuple(c_type.__name__ for c_type in correct_types)
                errmsg = "Can be any one from"
            else:
                correct_types = correct_types.__name__
                errmsg = "Should be"
    
            raise Exception("Incorrect type '{0}' provided to '{1}'. {2} '{3}'."\
                            .format(value.__class__.__name__, arg_prop_name, errmsg, correct_types))
        return True
    
    @classmethod
    def validate_arg_prop_value_list(cls, arg_prop_name, value, correct_values):
        """
        DESCRIPTION:
            Function to validate values passed to properties or args is 
            correct from list of values.
        PARAMETERS:    
            arg_prop_name:
                Required: Yes
                Type: String  
                Description: Name of the argument or property.
            value:
                Required: Yes
                Type: Any 
                Description: Value of the argument or property.
            correct_values:
                Required: Yes
                Type: Tuple or list
                Description: Correct values of the argument or property.
        """
        if isinstance(value, str):
            value = value.lower()
        if value not in correct_values:
            errmsg = "Can be any one from" if len(correct_values) > 1 else "Should be"
            raise Exception("""Incorrect value '{0}' provided to '{1}'. {2} '{3}'.
            """.format(str(value), arg_prop_name, errmsg, str(correct_values)))
        return True

    @classmethod
    def validate_arg_prop_value_range(cls, arg_prop_name, value, range, exclude=None):
        """
        DESCRIPTION:
            Function to validate values passed to properties or args is 
            correct from range of values.
        PARAMETERS:    
            arg_prop_name:
                Required: Yes
                Type: String  
                Description: Name of the argument or property.
            value:
                Required: Yes
                Type: Any 
                Description: Value of the argument or property.
            range:
                Required: Yes
                Type: Tuple or list of length
                Description: Correct range values of the argument or property.
                             If Tuple provided, ends are not included.
                             If list is provided, ends are included.  
            exclude:
                Required: No
                Type: strig
                Description: Specifies the side of the value in the range provided as list.                             
        """
        if len(range) != 2:
            raise Exception("Provide start and end value. For e.g (3, 5) or [3, 5]")
        if isinstance(range, tuple) and (value <= range[0] or value >= range[1]):
            raise Exception("""Incorrect value '{0}' provided to '{1}'. Should be between '{2}' exculding the boundaries.
            """.format(str(value), arg_prop_name, str(range))) 
        if isinstance(range, list):
            if exclude is None and (value < range[0] or value > range[1]):
                raise Exception("""Incorrect value '{0}' provided to '{1}'. Should be between '{2}' inculding the boundaries.
                """.format(str(value), arg_prop_name, str(range))) 
            elif exclude == "left" and (value <= range[0] or value > range[1]):
                raise Exception("""Incorrect value '{0}' provided to '{1}'. Should be between '{2}' exculding the left boundary.
                """.format(str(value), arg_prop_name, str(range)))   
            elif exclude == "right" and (value < range[0] or value >= range[1]):
                raise Exception("""Incorrect value '{0}' provided to '{1}'. Should be between '{2}' exculding the right boundary.
                """.format(str(value), arg_prop_name, str(range)))
        return True                   

    @classmethod
    def validate_non_negative_value(self, arg_prop_name, value):
        """
        DESCRIPTION:
            Function to validate values passed to properties or args is 
            non-negative. That is greater than or equal to Zero.
            .
        PARAMETERS:    
            arg_prop_name:
                Required: Yes
                Type: String  
                Description: Name of the argument or property.
            value:
                Required: Yes
                Type: Any 
                Description: Value of the argument or property.
        """
        if not isinstance(value, (int, float, tuple)):
            value = value.value
        elif isinstance(value, tuple):
            value = value[0]
        if value < 0:
            raise Exception("""Value passed to '{0}' should be greater than or equal to 0.
            Value provided is {1}.""".format(arg_prop_name, value))
        return True

    @classmethod
    def validate_positive_value(self, arg_prop_name, value):
        """
        DESCRIPTION:
            Function to validate values passed to properties or args is 
            Positive. That is greater than Zero.
            .
        PARAMETERS:    
            arg_prop_name:
                Required: Yes
                Type: String  
                Description: Name of the argument or property.
            value:
                Required: Yes
                Type: Any 
                Description: Value of the argument or property.
        """
        if not isinstance(value, (int, float, tuple)):
            value = value.value
        elif isinstance(value, tuple):
            value = value[0]
        if value <= 0:
            raise Exception("""Value passed to '{0}' should be greater than 0.
            Value provided is {1}.""".format(arg_prop_name, value))
        return True

    @classmethod
    def validate_child_class(self, arg_prop_name, child_class, parent_class, class_type):
        """
        DESCRIPTION:
            Function to validate values passed by user is a child class
            of parent class.
        PARAMETERS:
            arg_prop_name:
                Required: Yes
                Type: String  
                Description: Name of the argument or property.
            child_class:
                Required: Yes
                Type: propylean class  
                Description: Final class passed by user as input.
            parent_class:
                Required: Yes
                Type: propylean parent class
                Description: Parent class which are not exposed to end user.
            class_type:
                Required: Yes
                Type: String
                Description: Type of parent class in language of chemical industry
                             Example: "vessel" for _Vessels class.
        """
        if not isinstance(child_class, type):
            raise Exception(f"Value of {arg_prop_name} should be a propylean class used to declare property or objects.")

        if not issubclass(child_class, parent_class):
            raise Exception(f"Invalid type provided for '{arg_prop_name}'. Should be a class of type {class_type}.")