__all__ = ["Error", "parse_strips_file", "parse_domain", "parse_problem"]

import strip_types
import predicates
import actions
import conditions

class Error(BaseException):
    pass

def parse_strips_file(input_file): #pass in a strips file object
    tokens = tokenize(input_file)
    first_token = tokens.next()
    if first_token != "(":
        raise Error("Expected '(', got %s. Please ensure input is a valid STRIPS file" % first_token)
    result = list(parse_list(tokens))
    for token in tokens:  # Ensure no more tokens are left
        raise Error("Unexpected token: %s." % token)
    return result

def tokenize(input):
    for line in input:
        line = line.split(";", 1)[0]  # Remove comments by deleting all lines starting with ;
        line = line.replace("(", " ( ").replace(")", " ) ").replace("?", " ?") #process file so that parsing can work
        for token in line.split():
            yield token.lower()

def parse_list(token_generator):
    # First "(" already removed by iterator so don't bother
    while True:
        try:
            token = token_generator.next()
        except StopIteration:
            raise Error("End of list")
        if token == ")":
            return
        elif token == "(":
            yield list(parse_list(token_generator))
        else:
            yield token

def parse_domain(domain_strips_generator):# domain generator rename?
    iterator = iter(domain_strips_generator)

    if (iterator.next() != "define"):
	raise Error("STRIPS domain file does not contain define")
    domain_definition = iterator.next()

    #Check for errors in the domain file
    if (domain_definition[0] == "domain" and len(domain_definition) == 2):
	yield domain_definition[1]
    else:
	raise Error("STRIPS domain file is not structured properly")

    requirements = iterator.next()
    if requirements[0] == ":requirements":
        yield requirements[1]  #contains :typing
        types = iterator.next()
    else:
	types = requirements
    
    the_types = [strip_types.Type("object")]
    if types[0] == ":types":
        the_types.extend(strip_types.parse_typed_list(types[1:],
                                                     constructor=strip_types.Type))
        constants = iterator.next()
    else:
        constants = types
    yield the_types

    if constants[0] == ":constants":
        yield strip_types.parse_typed_list(constants[1:])
        pred = iterator.next()
    else:
        yield []
        pred = constants

    if (pred[0] != ":predicates"):
	raise Error("STRIPS domain file does not contain predicates")
    yield ([predicates.Predicate.parse(entry) for entry in pred[1:]]
	    +
           [predicates.Predicate("=",
                                 [strip_types.TypedObject("?x", "object"),
                                  strip_types.TypedObject("?y", "object")])]) #Equality predicate; thanks to Walid 

    #Only actions left if it is a STRIPS file; read all the remaining entries in the generator
    remaining_entries = [action for action in iterator]

    the_actions = []
    for act in remaining_entries:
        action = actions.Action.parse(act)
        the_actions.append(action)
    yield the_actions

def parse_problem(problem_strips_generator):
    iterator = iter(problem_strips_generator)

    if (iterator.next() != "define"):
	raise Error("STRIPS problem file does not contain define")

    problem_definition = iterator.next()
    #Check for errors in the problem file
    if (problem_definition[0] == "problem" and len(problem_definition) == 2):
	yield problem_definition[1]
    else:
	raise Error("STRIPS problem file is not structured properly")
    
    domain_description = iterator.next()
    #Check for issues in the problem's domain description
    if (domain_description[0] == ":domain" and len(domain_description) == 2):
	yield domain_description[1]
    else:
	raise Error("STRIPS problem file does not contain a domain description")   	

    objects = iterator.next()
    """if requirements[0] == ":requirements":
        yield requirements[1] #contains :typing
        objects = iterator.next()
    else:
	objects = requirements	"""

    if objects[0] == ":objects":
        yield strip_types.parse_typed_list(objects[1:])
        init = iterator.next()
    else:
        yield []
        init = objects

    if (init[0] != ":init"):
	raise Error("STRIPS problem contains no init state")

    initial = []
    for fact in init[1:]:
        initial.append(conditions.Atom(fact[0], fact[1:]))
    yield initial

    goal = iterator.next()

    if (goal[0] == ":goal" and len(goal) == 2):
	yield conditions.parse_condition(goal[1])
    else:
	raise Error("STRIPS problem contains no goal state")

if __name__ == "__main__":
    a = parse_strips_file(file('task.pddl'))
    y = parse_problem(a)
    for x in y:
	print x
	
 
