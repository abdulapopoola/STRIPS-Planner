import domain as dmain
import problem as prob

from copy import deepcopy
import itertools

import conditions
import actions
from parser import *

from search import *
from utils import *

def loadIntoProblem(domainFile,problemFile):
    the_domain = dmain.Domain.instantiate(domainFile)
    the_problem = prob.Problem.instantiate(problemFile)
    return Planner(the_problem,the_domain)

#______________________________________________________________________________
## Planning State representation

class PlannerState:
    def __init__(self,problem,domain):
	self.domain = domain
	self.problem = problem
	
	#Check if domain and problem match
        if(problem.domain_name == domain.domain_name):
	    self.initial_objects = problem.objects + domain.constants #initial objects made up of both
    	    self.goal = problem.goal	    
	else:
	    raise Error("The problem file file doesn't match the domain file, please check")
    
    def __str__(self):
    	return "%s %s %s" % (self.__class__.__name__, self.domain,self.problem)

    def __repr__(self):
	return str(self)

#______________________________________________________________________________
## Planner class inherits Problem

class Planner(Problem):    
    def __init__(self,problem,domain):
	try:
	    initial = PlannerState(problem,domain) #initial problem state
	    print initial
	except Error:
	    raise ("Planner cannot be created, please check both files")
	
	self.initial = initial
	Problem.__init__(self,self.initial,self.initial.goal)
    
    def successor(self,state):

    	actions  = self.getAllPossibleActions(state) #Get all the possible actions for a state
    	successors = self.getSuccessors(actions,state) #Get the successor states for all possible actions
  	
    	return successors

    def getAllPossibleActions(self,state):
    	doable_actions = []
    	actions = state.domain.actions
		
    	for action in actions:
            doable_instances_list = self.processAction(action,state)
	    doable_actions += doable_instances_list
    
    	return doable_actions

    def getSuccessors(self,actions,state):
    	def successorFor(action):
		newstate = deepcopy(state) #don't use a shallow copy as this might not copy component objects
		newstate.problem.init = [new_init_atom for new_init_atom in newstate.problem.init if new_init_atom not in action.negative_atoms]#delete negated atomic formulas
		newstate.problem.init = newstate.problem.init + action.positive_atoms #Add new positive atomic formulas
		return (action, newstate) #action-state tuple
	
	return [successorFor(act) for act in actions]		

    def processAction(self,action,state):
        #getAllObjects = memoize(self.getAllObjects())
    	parameters = action.parameters
    	
	#Get the ordering and types of parameters for the action
    	parameter_type_order = [parameter.type for parameter in parameters]
    	parameter_pairs = []
    	possible_action = [] #List of all actions possible from this action using different parameter combinations

    	for parameter_type in parameter_type_order:
            objects  = self.getAllObjects(parameter_type,state.initial_objects)
            parameter_pairs.append(objects)

   	#Get all possible input combinations of input objects
        parameter_combinations = [list(combination) for combination in itertools.product(*parameter_pairs)]
	
	"""orig_comb = []
	for comb in parameter_combinations:
	   if (len(set(comb)) == len(comb)):
		orig_comb.append(comb)
	
	parameter_combinations = orig_comb#self.uniquify(parameter_combinations)
        """		
        for combination in parameter_combinations:
            if (len(set(combination)) < len(combination)):
                continue

            parameter_mapping = dict([param.name,value.name] for param,value in zip(parameters,combination))
            #print parameter_mapping
            fluent_facts = self.fluent_generator(parameter_mapping,action)
            
            poss_action = action.instantiate(parameter_mapping,state.problem.init,fluent_facts)
            if poss_action:
	        #poss_action.debug_print()# Uncomment for verbose mode
                possible_action.append(poss_action)
    
    	return possible_action


    def getAllObjects(self,parameter_type,objects):
    #returns a list of all objects that match this parameter type
    	matches = []
    	for obj in objects:
       	    if obj.type == parameter_type:
            	matches.append(obj)
    	return matches
    
    def fluent_generator(self,parameter_map,action):
    	fluents = []
    	for effect in action.effects:
            args = [parameter_map.get(arg,arg) for arg in effect.literal.args]
            if effect.literal.negative:
                atom = conditions.NegatedAtom(effect.literal.predicate,args)
            else:
            	atom = conditions.Atom(effect.literal.predicate,args)
            #atom.debug_print() #Uncomment for verbose mode
            fluents.append(atom)
        return fluents
    
    def goal_test(self, state):
	goal_state = False
	for atom in self.goal.parts:
	    #print atom
	    if atom not in state.problem.init:
		goal_state = False        	 
		return goal_state #As soon as one of the goal atoms is not found in the init state then immediately exit as this can never be a goal
	    else:
		goal_state = True
	return goal_state

    def uniquify(self,input_list): #return the unique values in the input list ! doesn't work yet! Not so important anyway
        output = []
        for x in input_list:
	    if x not in output:
		print x
      	        output.append(x)
	#print "len in uniq",len(output)
  	return output
    
    def h(self,state):
        counter = 0
        for atom in self.goal.parts:
            if atom in self.initial.problem.init:
                counter = counter + 1
        if counter == 0:
            counter = 0.00000000001 #set counter to a very small value so that the inverse will be huge
	#h_score = len(self.goal.parts) - counter #return number of unsatisfied literals
	h_score = len(self.initial.problem.init) / counter # this is actually the weight gotten by taking the inverse of counter/no of atoms in the init state
        return h_score
        
                
if __name__ == "__main__":
    a = loadIntoProblem("zenotravelStrips.pddl","zenop.pddl")
    
    node, max_nodes_in_memory,time = breadth_first_graph_search(a) #breadth first works better for this problem than depth_first
    solution_path = node.path()
    
    for node in solution_path:
	print node
    	for atm in node.state.problem.init:
    	    print atm
    	print "\n"
    print max_nodes_in_memory
