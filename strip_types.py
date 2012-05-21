import itertools

class Type(object):
    def __init__(self, name, basetype_name=None):
        self.name = name
        self.basetype_name = basetype_name
    def __str__(self):
        return self.name
    def __repr__(self):
        return "Type(%s, %s)" % (self.name, self.basetype_name)

class TypedObject(object):
    def __init__(self, name, type):
	self.name = name
        self.type = type
    def __eq__(self, other):
        return (self.name == other.name or self.name == '?'+other.name or other.name == "?"+self.name) and self.type == other.type
    def __ne__(self, other):
        return not self == other
    def __str__(self):
        return "%s: %s" % (self.name, self.type)
    def __repr__(self):
	return str(self)

def parse_typed_list(pred_list, constructor=TypedObject):
    result = []
    while pred_list:
        try:
            divider_index = pred_list.index("-")#Find the divider separating objects/constants values
        except ValueError:
            items = pred_list #The predicate list only contains objects of the type object so set it to empty and get all items in it
            pred_list = [] 
	    obj_type = "object"    
        else:
            items = pred_list[:divider_index] #Get all the objects before the divider. divider == '-'
            obj_type = pred_list[divider_index + 1] #Get the object type; comes after the divider
            pred_list = pred_list[divider_index + 2:] #Point it to the next object group after the divider in the list
        for item in items:
	    entry = constructor(item, obj_type)
            result.append(entry)
    return result
