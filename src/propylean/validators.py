class _Validators(object):
    def validate_arg_prop_value_type(self, arg_prop_name, value, correct_type):
        if not isinstance(value, correct_type):
            raise Exception("""Incorrect type '{0}' of value provided to '{1}'. Should be '{2}'.
            """.format(str(type(value)), arg_prop_name, str(correct_type)))