import conditions
import strip_types

def parse_effects(effect_list, result):
    """Parse a STRIPS effect
       
	The Effect class
       
 	ConjunctionEffects are effects containing conjunctions
	LiteralEffects are normal effects
    """

    token = effect_list[0]    
    args = effect_list[1:]

    def parse_effect(eff_list): #anonymous worker function
    	conjunct = eff_list[0]
    	if conjunct == "and":
    	    return ConjunctionEffect([parse_effect(eff) for eff in eff_list[1:]])
    	else:
    	    return Literal_Effect(conditions.parse_literal(eff_list))
    
    if token == "and":
        eff = ConjunctionEffect([parse_effect(eff) for eff in args])
    else:
        eff = Literal_Effect(conditions.parse_literal(effect_list))
    
    add_effect(eff, result)

def add_effect(tmp_effect, result):

    if isinstance(tmp_effect, ConjunctionEffect):
        for effect in tmp_effect.effects:
            add_effect(effect, result)
        return
    else:
        parameters = []
        condition = conditions.Truth()

        assert isinstance(tmp_effect, Literal_Effect)
        effect = tmp_effect.effect
        
	assert isinstance(effect, conditions.Literal)
	        
	# Look for effects that are the opposite of this effect in the result list
        new_effect = Effect(parameters, condition, effect)
        opposite_effect = Effect(parameters, condition, effect.negate())
        if not opposite_effect in result: #None exists in the result list
            result.append(new_effect)
        else:
            if isinstance(opposite_effect, conditions.NegatedAtom): #if opposite effect is negative; remove it and add the new one; else don't the new one
                result.remove(opposite_effect)
                result.append(new_effect)

class Effect():
    def __init__(self, parameters, condition, literal):
        self.parameters = parameters
        self.condition = condition
        self.literal = literal
    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.parameters == other.parameters and
                self.condition == other.condition and
                self.literal == other.literal)
    def debug_print(self):
        indent = "  "
        if self.parameters:
            print "%sforall %s" % (indent, ", ".join(map(str, self.parameters)))
            indent += "  "
        if self.condition != conditions.Truth():
            print "%sif" % indent
            self.condition.debug_print(indent + "  ")
            print "%sthen" % indent
            indent += "  "
        print "%s%s" % (indent, self.literal)
    def instantiate(self, var_mapping, init_facts, fluent_facts,result):
        self._instantiate(var_mapping, init_facts, fluent_facts, result)
    def _instantiate(self, var_mapping, init_facts, fluent_facts, result):
        condition = []
        try:
            self.condition.instantiate(var_mapping, init_facts, fluent_facts, condition)
        except conditions.Impossible:
            return
        effects = []
        self.literal.instantiate(var_mapping, init_facts, fluent_facts, effects)
        assert len(effects) <= 1
        if effects:
            result.append((condition, effects[0]))

class ConjunctionEffect():
    def __init__(self, effects):
        flattened_effects = []
        for effect in effects:
            if isinstance(effect, ConjunctionEffect):
                flattened_effects += effect.effects
            else:
                flattened_effects.append(effect)
        self.effects = flattened_effects
    def debug_print(self, indent="  "):
        print "%sand" % (indent)
        for eff in self.effects:
            eff.debug_print(indent + "  ")

class Literal_Effect():
    def __init__(self, effect):
        self.effect = effect
    def debug_print(self, indent="  "):
        print "%s%s" % (indent, self.effect)
