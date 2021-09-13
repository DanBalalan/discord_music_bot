class InvalidArguments(Exception): pass


class ArgChecker:

    @staticmethod
    def check(args, schema):
        if len(args) != len(schema):
            raise InvalidArguments

        for arg, schema_arg_type in zip(args, schema):
            expected_type = schema_arg_type if schema_arg_type else type(schema_arg_type)  # None
            if not isinstance(arg, expected_type):
                raise InvalidArguments
