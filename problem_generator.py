import random
import os, errno

from parser import *
from problem import *

def instantiate(strips_problem_file):
    parsed_strips_file = parse_strips_file(file(strips_problem_file)) #Parse the file
    problem_generator = parse_problem(parsed_strips_file) #get the problem class generator
    prob_def = list(problem_generator)
    return prob_def

def generator(problem_template, folder_for_generated_files, no_of_pddl_files,objects_to_vary,range_of_variation):
    problem_template = Problem.instantiate(problem_template) #Get the template to use in producing new problem template instances;am using this template
    count = 1
    folder = folder_for_generated_files #Folder for storing all generated instances
 
    try:
        os.makedirs(folder)
    except OSError, e:
	if e.errno == errno.EEXIST: #Folder already exists so delete all its contents
	    print folder + " already exists so not regenerating files"
	    return
	else:
	    raise 
    
    while (count <= no_of_pddl_files):
	filename = "zeno" + str(count) + ".pddl"	
	problem_name = "zeno" + str(count)

	number_of_objects_to_create = random.randint(1,range_of_variation) #count
	print number_of_objects_to_create
	pddlfile = problem_template.pddl_write(problem_name,objects_to_vary,number_of_objects_to_create)
	writer(folder+filename,pddlfile)
	count = count+1
    print str(no_of_pddl_files) + " problem files successfully generated!"

def writer(filename,problem):
    filehandle = open(filename, 'w')
    filehandle.write(problem)
    filehandle.close()

def cleanUpDirectory(dir_name):
    gen_dir_path = os.getcwd() + "/" + dir_name
    for filename in [filename for filename in os.listdir(gen_dir_path) if not filename in [".",".."]]:
	os.unlink(os.path.join(gen_dir_path,filename))


if __name__ == "__main__":
    generator("pfile1zeno","Gendda/",50,"city",50)
