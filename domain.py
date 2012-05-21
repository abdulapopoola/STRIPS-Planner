from parser import *

class Domain():
    def __init__(self, domain_definition_list):
        self.domain_name = domain_definition_list[0]
        self.requirements = domain_definition_list[1]
        self.types = domain_definition_list[2]
        self.constants = domain_definition_list[3]
        self.predicates = domain_definition_list[4]
        self.actions = domain_definition_list[5]

    def instantiate(strips_domain_file):
	parsed_strips_file = parse_strips_file(file(strips_domain_file)) #Parse the file
        domain_generator = parse_domain(parsed_strips_file) #Get the domain class generator
	domain_def = list(domain_generator)
        
	return Domain(domain_def)
    instantiate = staticmethod(instantiate)

    def __str__(self):
	return "<Domain: %s>" %(self.domain_name)

    def __repr__(self):
	return str(self)

    def debug_print(self):
        print "Domain %s: Requirements [%s]" % (self.domain_name, self.requirements)
        
	print "Types:"
        for type in self.types:
            print "  %s" % type

	print "Constants:"
        for constant in self.constants:
            print "  %s" % constant

        print "Predicates:"
        for pred in self.predicates:
            print "  %s" % pred

        print "Actions:"
        for action in self.actions:
            action.debug_print()

if __name__ == "__main__":
    a = Domain.instantiate("domain.pddl") #test
