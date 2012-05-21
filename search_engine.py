import sys
import strips_engine
from search import *
import utils

def execute():
    if len(sys.argv) != 7:
            raise SystemExit("Please input seven arguments\n")
        
    domain_file = sys.argv[2]
    problem_file = sys.argv[4]
    search_algorithm = sys.argv[6]
    
    problem = strips_engine.loadIntoProblem(domain_file, problem_file)
    node = plan_search(search_algorithm, problem)
    write_solution(search_algorithm, node)
    print "Success!"

def plan_search(search_algorithm,problem):
    if search_algorithm == "bfs":
        return breadth_first_graph_search(problem)
    elif search_algorithm == "dfs":
        return depth_first_graph_search(problem)
    elif search_algorithm == "ids":
        return iterative_deepening_search(problem)
    elif search_algorithm == "ucs":
        return uniform_cost_search(problem)
    elif search_algorithm == "bfgs":
        return best_first_graph_search(problem, problem.h)
    elif search_algorithm == "astar":
        return astar_search(problem)
    else:
	raise SystemExit("Please only use one of the following algorithms (bfs|dfs|ids|ucs|bfgs|astar)")

def write_solution(search_algorithm, node):   
    file_handle = open('solution.txt','w')
    file_handle.writelines("Search algorithm used: %s\n" %search_algorithm.upper())
    file_handle.writelines("\n")
	
    solution_path = node.path()
        
    for node in solution_path:
        file_handle.writelines("Action: %s \n" % node.action)
	file_handle.writelines("State: \n")
	for atom in node.state.problem.init:
	    file_handle.writelines("\t%s" %(atom))
	    file_handle.writelines("\n")

	file_handle.writelines("\n")
	file_handle.writelines("\n")
        
    file_handle.close()
    
    
if __name__ == "__main__":   
    execute()    
