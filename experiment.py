import random
import os, errno

import sys
import strips_engine
import problem_generator as gen

from search import *
import utils

def execute():
    if len(sys.argv) != 9:
        print len(sys.argv)
        raise SystemExit("Please use the following pattern\n")

    no_of_pddl_files = int(sys.argv[2])
    objects_to_vary = sys.argv[4]
    range_of_variation = int(sys.argv[6])
    search_algorithm = sys.argv[8]

    domain_file = "zenotravelStrips.pddl"
    problem_template = "pfile1zeno"
    folder_for_generated_files = "Simple astar_mod 50/"
    
    """
    Check here if folder already exists to avoid regenerating new problems for new searches
    try:
        os.makedirs(folder)
    except OSError, e:
	if e.errno == errno.EEXIST: #Folder already exists so delete all its contents
	    pass #cleanUpDirectory(folder) no need to wipe off gen files
	else:
	    raise 
    """

    """
    no_of_pddl_files = 5
    range_of_variation = 20 #FIXME; if it is city; subtract 3 from this number as there are 3 initial cities;
    objects_to_vary = "city"
    """
    

    #Generate samples
    gen.generator(problem_template, folder_for_generated_files, no_of_pddl_files, objects_to_vary, range_of_variation)
    
    #Get data from  generated samples
    gen_dir = os.getcwd() + "/" + folder_for_generated_files
    
    processed_count = len([filename for filename in os.listdir(gen_dir) if not filename in [".",".."]])
    data = []
    counter = 0
    for filename in [filename for filename in os.listdir(gen_dir) if not filename in [".",".."]]:
	problem_file = os.path.join(gen_dir,filename)
	problem = strips_engine.loadIntoProblem(domain_file, problem_file)

	count = problem.initial.problem.get_object_type_count(objects_to_vary)
        node, max_nodes_in_memory, nodes_traversed = search(search_algorithm,problem)
	
	space = max_nodes_in_memory
	time = nodes_traversed

	result = [count,space,time]
	data.append(result)
	counter = counter + 1
	left = processed_count - counter
	print "(%s %s %s %s)" %(str(counter), "pddl files processed ",str(left), "files left")
    
    write_results(objects_to_vary,no_of_pddl_files,search_algorithm,range_of_variation,data)

def search(search_algorithm,problem):
    if search_algorithm == "bfs":
        return breadth_first_graph_search(problem)
    elif search_algorithm == "ids":
        return iterative_deepening_search(problem)
    elif search_algorithm == "ucs":
        return uniform_cost_search(problem)
    elif search_algorithm == "bfgs":
        return best_first_graph_search(problem, problem.h)
    elif search_algorithm == "astar":
        return astar_search(problem)
    else:
	raise SystemExit("Please only use one of the following algorithms (bfs|ids|ucs|bfgs|astar)")

def write_results(object_varied,amount_generated,search_used,range_of_variation,results_list):
    results_file = "%s %s copies of %s_ %s" %("results_",amount_generated,object_varied,search_used)
    filehandle = open(results_file, 'w')
    
    file_description = "%s \t\t\t %s \n" %("Object varied",object_varied)
    file_description = file_description + "%s \t\t %s \n" %("No of files generated",amount_generated)
    file_description = file_description + "%s \t\t %s \n" %("Range of variation",range_of_variation)
    file_description = file_description + "%s \t\t %s \n\n" %("Search algorithm used",search_used)

    filehandle.write(file_description)

    header = "%s\t %s\t %s\n" %("COUNT","SPACE","TIME")
    filehandle.write(header)
    for data in results_list:
	for rslt in data:
	    filehandle.write(str(rslt))
    	    filehandle.write('\t')
    	filehandle.write('\n')
    filehandle.close()
    

if __name__ == "__main__":
    execute()
