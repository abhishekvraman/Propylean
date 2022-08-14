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
        if not isinstance(value, correct_types):
            raise Exception("""Incorrect type '{0}' provided to '{1}'. Should be '{2}'.
            """.format(type(value), arg_prop_name, str(correct_types)))