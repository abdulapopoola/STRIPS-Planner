import strip_types

def parse_condition(condition_list, negated=False):
    """Parse a STRIPS condition : the Condition class is the superclass of Literals
	and the Literal class is the superclass of Atoms
       If identifier token is NOT, return a negated atom
       else if it is an AND, return a conjunction of the component atoms
       through a recursive call to the same function	
    """
    
    token = condition_list[0]
    
    args = condition_list[1:]
    
    if token == "and":  
	 parts = [parse_condition(part) for part in args]
         return Conjunction(parts)
        
    if token == "not":
         assert len(args) == 1 #Assert that condition is properly structured
         return parse_condition(args[0], not negated)
    
    if negated:
	return NegatedAtom(condition_list[0], condition_list[1:])        
    else:
	return Atom(condition_list[0], condition_list[1:])        

def parse_literal(condition_list):
    if condition_list[0] == "not":
        assert len(condition_list) == 2    #Assert that literal is properly structured
        condition_list = condition_list[1] #removes the 'not' identifier token at the start of the list
	
	predicate = condition_list[0]
	terms = condition_list[1:]
	
        return NegatedAtom(predicate, terms)
    else:
	predicate = condition_list[0]
	terms = condition_list[1:]
	
        return Atom(predicate, terms)        

class Condition():
    def __init__(self, parts):
        self.parts = tuple(parts)  
    def __ne__(self, other):
        return not self == other

    def debug_print(self, indent="  "):
        print "%s%s" % (indent, self._debug_print())
        for part in self.parts:
            part.debug_print(indent + "  ")

    def pddl_write(self):
	string_representation = ""
	for part in self.parts:
	    string_representation = string_representation + part.pddl_write()
	
	if self.__class__.__name__ == "Conjunction":
	    tag = "and"
	
	return "(%s\n %s)" %(tag,string_representation)	
	    
        #return string_representation

    def _debug_print(self):
        return self.__class__.__name__
    def instantiate(self, parameter_map, initial_conditions, fluents, result):
        raise ValueError("Condition cannot be created")

class Impossible(Exception):
    pass

class Falsity(Condition):
    def __init__(self):
	pass
    def instantiate(self, parameter_map, initial_conditions, fluents, result):
        raise Impossible()
    def negate(self):
        return Truth()
    def __eq__(self, other):
        return self.__class__ is other.__class__

class Truth(Condition):
    def __init__(self):
	pass
    def instantiate(self, parameter_map, initial_conditions, fluents, result):
        pass
    def negate(self):
        return Falsity()
    def __eq__(self, other):
        return self.__class__ is other.__class__

class Conjunction(Condition):
    def instantiate(self, parameter_map, initial_conditions, fluents, result):
        for part in self.parts:
            part.instantiate(parameter_map, initial_conditions, fluents, result)
    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.parts == other.parts)

class Literal(Condition):
    parts = []
    
    def __init__(self, predicate, args):
        self.predicate = predicate
        self.args = tuple(args)    

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.predicate == other.predicate and
                self.args == other.args)
    
    def __repr__(self):   
	return str(self)

    def __str__(self):
        return "%s %s (%s)" % (self.__class__.__name__, self.predicate,
                              ", ".join(map(repr, self.args)))

    def pddl_write(self):
        return "\t(%s %s)\n" % (self.predicate," ".join(self.args)) #add tab spacing in front and a new line afterwards
class Atom(Literal):
    negative = False
    
    def instantiate(self, parameter_map, initial_conditions, fluents, result):
        args = [parameter_map.get(arg, arg) for arg in self.args]
        atom = Atom(self.predicate, args)
        if atom in fluents:
            result.append(atom)
        elif atom not in initial_conditions:
            raise Impossible()
    def negate(self):
        return NegatedAtom(self.predicate, self.args)
    def positive(self):
        return self

class NegatedAtom(Literal):
    negative = True

    def instantiate(self, parameter_map, initial_conditions, fluents, result):
        args = [parameter_map.get(arg, arg) for arg in self.args]
        atom = NegatedAtom(self.predicate, args)
        if atom in fluents:
            result.append(NegatedAtom(self.predicate, args))
        elif atom in initial_conditions:
            raise Impossible()
    def negate(self):
        return Atom(self.predicate, self.args)
    positive = negate
