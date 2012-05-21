import strip_types

class Predicate():
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def parse(pred_list):
        name = pred_list[0]
        args = strip_types.parse_typed_list(pred_list[1:])
        return Predicate(name, args)

    parse = staticmethod(parse)

    def __repr__(self):
	return str(self)    

    def __str__(self):
        return "%s(%s)" % (self.name, ", ".join(map(str, self.args)))
