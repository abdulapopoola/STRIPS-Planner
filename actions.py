import strip_types
import conditions
import effects

class Action():
    def __init__(self, name, parameters, precondition, effects):
        self.name = name
        self.parameters = parameters
        self.precondition = precondition
        self.effects = effects
        
    def __repr__(self):
        return "<Action %r>" % (self.name)

    def parse(action_list):
        iterator = iter(action_list)

        if (iterator.next() != ":action"):
	    raise Error("STRIPS file does not contain actions")

        name = iterator.next()
        params = iterator.next()
        if params == ":parameters":
            parameters = strip_types.parse_typed_list(iterator.next())
            precond = iterator.next()
        else:
            parameters = []
            precond = params
        if precond == ":precondition":
            precondition = conditions.parse_condition(iterator.next())
            effect_iter = iterator.next()
        else:
            precondition = conditions.Conjunction([])
            effect_iter = precond
        assert effect_iter == ":effect"
        effect_list = iterator.next()
        eff = []
        cost = effects.parse_effects(effect_list, eff)
        for rest in iterator:
            assert False, rest
        return Action(name, parameters, precondition, eff)
    parse = staticmethod(parse)
    
    def debug_print(self):
        print "%s(%s)" % (self.name, ", ".join(map(str, self.parameters)))
        print "Precondition:"
        self.precondition.debug_print()
        print "Effects:"
        for eff in self.effects:
            eff.debug_print()        
    
    def instantiate(self, parameter_map, init_facts, fluent_facts):
        """Core method
        Returns None if the parameter combination does not lead to an action that 
	can fire. This will happen if the preconditions are contradicted
	"""	        
	arg_list = [parameter_map[parameter.name] for parameter in self.parameters]
        name = "(%s %s)" % (self.name, " ".join(arg_list))
	
        precondition = []
        try:
            self.precondition.instantiate(parameter_map, init_facts,fluent_facts, precondition)
        except conditions.Impossible:
            return None
        effects = []
        for eff in self.effects:
            eff.instantiate(parameter_map, init_facts, fluent_facts, effects)
        if effects:
            return ActionEffect(name, precondition, effects)
        else:
            return None

class ActionEffect:
    def __init__(self, name, precondition, effects):
        self.name = name
        self.precondition = precondition
        self.positive_atoms = []
        self.negative_atoms = []
        
	for condition,atom in effects:
            if not atom.negative:
		self.positive_atoms.append(atom)
	    else:
		self.negative_atoms.append(atom)

    #def __call__(self,name,precondition,effects):
     #   return self # ActionEffect.__init__(self,name,precondition,effects)
       
	"""Check for contradictions; i.e. an effect and its negation existing 
	   simultaneously in the effects list.
	   If contradictions exist, remove the negative effect
	""" 
	contradictions = []
	for atom in self.negative_atoms:
		if atom.negate in self.positive_atoms:
			contradictions.append(atom)
	
	"""Delete contradictions and negate the remaining atoms so that the 
	   negative_atoms can be used to ensure proper deletion from the init
	   conditions of the starting state
	"""
	self.negative_atoms = [atom.negate() for atom in self.negative_atoms if atom not in contradictions]
 
    def __repr__(self):
	    return "%s" %(self.name)
        
    def debug_print(self):
        print "<Action: %s>" %(self.name)
        for cond in self.precondition:
            print "Preconditions: %s" % cond
	print "Effects:"
        for atom in self.positive_atoms:
            print "\tPositive atom: %s" %(atom)
        for atom in self.negative_atoms:
            print "\tNegated atom: %s" %(atom)
	print "\n"
