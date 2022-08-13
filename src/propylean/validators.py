class _Validators(object):
    def validate_arg_prop_value_type(self, arg_prop_name, value, correct_types):
        """
        DESCRIPTION:
            Function to validate values passed to properties or args is of
            of correct types.
        PARAMETERS:    
            arg_prop_name:
                Required: No
                Type: String  
                Description: Minimum flow requirement of the pump
        """
        if not isinstance(value, correct_types):
            raise Exception("""Incorrect type '{0}' of value provided to '{1}'. Should be '{2}'.
            """.format(str(type(value)), arg_prop_name, str(correct_types)))