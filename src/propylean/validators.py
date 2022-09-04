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
            raise Exception("""Incorrect type '{0}' provided to '{1}'. Should be '{2}'.
            """.format(type(value), arg_prop_name, str(correct_types)))
    
    @classmethod
    def validate_arg_prop_value_list(cls, arg_prop_name, value, correct_values):
        """
        DESCRIPTION:
            Function to validate values passed to properties or args is 
            correct from list of values.
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
            correct_values:
                Required: Yes
                Type: Tuple or list
                Description: Correct values of the argument or property.
        """
        if isinstance(value, str):
            value = value.lower()
        if value not in correct_values:
            raise Exception("""Incorrect value '{0}' provided to '{1}'. Should be among '{2}'.
            """.format(str(value), arg_prop_name, str(correct_values)))

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