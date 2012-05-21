from parser import *

import random

class Problem():
    def __init__(self, problem_definition_list):
        self.problem_name = problem_definition_list[0]
	self.domain_name = problem_definition_list[1]
        #self.requirements = problem_definition_list[2]
        self.objects = problem_definition_list[2]
        self.init = problem_definition_list[3]
        self.goal = problem_definition_list[4]

    def instantiate(strips_problem_file):
	parsed_strips_file = parse_strips_file(file(strips_problem_file)) #Parse the file
        problem_generator = parse_problem(parsed_strips_file) #get the problem class generator
	prob_def = list(problem_generator)        

	return Problem(prob_def)
    instantiate = staticmethod(instantiate)

    def __str__(self):
	return "<Problem: %s>" %(self.problem_name)

    def __repr__(self):
	return str(self)

    def debug_print(self):
        print "Problem %s: Domain %s Requirements [%s]" % (self.problem_name, self.domain_name, self.requirements)
        
	print "Objects:"
        for obj in self.objects:
            print "  %s" % obj

	print "Init:"
        for init_cond in self.init:
            print "  %s" % init_cond

        print "Goals:"
        print self.goal.debug_print()
    
    def __repr__(self):
	return "Problem %s: " % (self.problem_name)

    def get_object_type_count(self, object_type):
	count = 0
	for obj in self.objects:
	    if obj.type == object_type:
	    	count = count + 1
	return count	

    def pddl_write(self,prob_name,objects_to_vary,number_to_create):
	problem_name = "(%s %s)\n" %("problem",prob_name)
	problem_domain = "(%s %s)\n" %(":domain",self.domain_name)                
	
	object_type = objects_to_vary
	number = number_to_create
	
	existing_objects = ""
	for obj in self.objects:
	    obj = '\t' + obj.name + " - " + obj.type + '\n'
	    existing_objects = existing_objects + obj
	
	count = 1
	generated_objects = ""
	while (count <= number):
	    obj_id = object_type + str(count+2) #Starting at 3 since I am only passing in cities
	    obj = '\t' + obj_id + " - " + object_type + '\n'
	    generated_objects = generated_objects + obj
	    count = count + 1

	init_objects = existing_objects + generated_objects
	
	init_objects_section = "(%s\n %s)\n" %(":objects",init_objects)
	
	init_literals = ""
    	
	for literal in self.init:
            init_literals = init_literals + literal.pddl_write()
        init_section = "(%s\n %s)\n" %(":init",init_literals)
	
	if number > 10:
	    number = 10
	plane_destination = random.randint(1,number)
	plane_goal = "(at plane1 city" + str(plane_destination) + ")"

	goal_literals = "\t(at person1 city0)\n\t(at person2 city2)\n\t"+plane_goal+"\n"
	goal_conjunction = "(%s\n %s)" %("and",goal_literals)

        goal_section = "(%s\n %s)\n" %(":goal",goal_conjunction) #self.goal.pddl_write()

	prob_body = problem_name + problem_domain + init_objects_section + init_section + goal_section
	
	complete_prob = "(%s %s)" %("define ",prob_body)
	
	return complete_prob


if __name__ == "__main__":
    a = Problem.instantiate("task.pddl") #test
