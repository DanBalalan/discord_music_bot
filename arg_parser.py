class InvalidArguments(Exception): pass


class ArgParser:

    @staticmethod
    def parse(args, args_schema):
        if len(args) != len(args_schema):
            raise InvalidArguments(f'Wrong number of arguments')

        result_args = []
        for arg, schema_arg_type in zip(args, args_schema):
            if schema_arg_type is None:
                continue
            try:
                result_args.append(schema_arg_type(arg))
            except Exception as e:
                raise InvalidArguments(e)

        return tuple(result_args)
