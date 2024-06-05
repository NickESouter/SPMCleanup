#Imports relevant modules.
import os
import sys
import argparse
import shutil

#This function is used to delete the simulation folder if it is found to be empty when the script finishes running, to avoid issues with overwriting.
def delete_sim():
	if 'sim' in method:
		if not os.listdir(retained_dir) and not os.listdir(deleted_dir):
			shutil.rmtree(sim_dir)

#This function is used to exit the script at relevant points.
def abort_script():
	print("Exiting.")
	delete_sim()
	sys.exit()


# ------------------------------------- COMMAND LINE ARGUMENTS -------------------------------------


#Create ArgumentParser object
parser = argparse.ArgumentParser(description='Process input path, preprocessing label, and relative path.')

# Add arguments
parser.add_argument('-input_path', help = 'Input path', required = True)
parser.add_argument('-preproc_label', help = 'Preprocessing label present at the front of final preprocessed files', required = True)
parser.add_argument('-method', help = "Can be 'delete' to remove files, 'sim_link' to simulate deleting files through symbolic links, or 'sim_copy' to simulate deleting files with copies", required = True)
parser.add_argument('-rel_path', help = "Relative path to functional data located within each subject's folder, if relevant", required = False)
parser.add_argument('-also_keep', help = 'List of additional target strings to not delete, separated by commas with no spaces', required = False)
parser.add_argument('-out_path', help = 'Output folder for linked/copied files to be stored in', required = False)

#Parse the arguments
args = parser.parse_args()

#Assign values to variables
input_path = args.input_path
preproc_label = args.preproc_label
rel_path = args.rel_path
also_keep = args.also_keep
method = args.method
out_path = args.out_path

#Verifies that a valid method has been specified, quits if not.
if method not in ['delete', 'sim_link', 'sim_copy']:
	print("The 'method' entered ({}) is not valid. Please request either 'delete', 'sim_link', or 'sim_copy'.".format(method))
	abort_script()

#A list of strings appended to the front of a raw data file that we'll want to keep.
to_keep = [preproc_label, 'rp_', 'mean']

#If the user has specified 'also_keep', the relevant strings are added to the above list.
if also_keep:
	also_keep = also_keep.split(',')
	for keep_string in also_keep:
		to_keep.append(keep_string)

#If using one of the simulation methods...
if 'sim' in method:

	#An output folder for simulated data is created. Either in the current working directory,
	#or in a new directory if specified.
	if out_path:
		sim_dir = os.path.join(out_path, 'SPMCleanup_Simulation_{}'.format(method[-4:]))
	else:
		sim_dir = os.path.join(os.getcwd(), 'SPMCleanup_Simulation_{}'.format(method[-4:]))

	#Defines subfolders for data that woudl be retained and deleted. These are then created.
	retained_dir = os.path.join(sim_dir, 'Retained')
	deleted_dir = os.path.join(sim_dir, 'Deleted')

	if not os.path.exists(sim_dir):
		os.mkdir(sim_dir)
		os.mkdir(retained_dir)
		os.mkdir(deleted_dir)

	#Script quits if the simulation directory already exists. We don't want to risk overwriting something important.
	else:
		print("Simulation directory already exists. Please delete it and its contents before proceeding.")
		abort_script()


# ------------------------------------- SCRIPT INTRODUCTION -------------------------------------


#Text is printed to inform the user of what is about to happen. The input path provided is printed back to the user.
print("""\n*** Welcome to SPMCleanup! This script is intended to help you delete intetermediate files generated during the preprocessing of fMRI data in SPM. \n \nWe strongly advise that you only use this script in cases where you have a standard structure to your data (e.g., using BIDS or your own consistent file naming convention). \n \nBased on the information you provided in the command line, we will target data located in '{}'. This folder is assumed to contain subject-specific subfolders.""".format(input_path))

#Using the relative path, if relevant, prints out exactly where we'd expect raw data to be located.
if rel_path:
	print("Final preprocessed functional data is expected to be in the form '{}/<SUBJECT ID>/{}/{}<RAW FILE NAME>'.".format(input_path, rel_path, preproc_label))
else:
	print("Final preprocessed functional data is expected to be in the form '{}/<SUBJECT ID>/{}<RAW FILE NAME>'.".format(input_path, preproc_label))

#Prints the method that has been specified, which conveys the relative level of risk.
if method == 'delete':
	print("You have selected DELETION mode. All files marked for deletion will be deleted. Proceed with caution.")
elif method == 'sim_link':
	print("You have selected SIMULATION LINK mode. Symbolic links will be created to simulate how your SPM data would look after cleanup, but no files will be deleted.")
elif method == 'sim_copy':
	print("You have selected SIMULATION COPY mode. Copies of files will be created to simulate how your SPM data would look after cleanup, but no files will be deleted.")

#Asks the user to confirm they're happy to proceed.
response = input("\n \nIs all of this correct? Enter 'y' to continue, or 'n' to exit.".format(input_path, input_path, rel_path, preproc_label)).strip().lower()

#If yes, prints out the list of target strings that we'll use to retain files.
if response == 'y':

	print("\n*** Using the provided preprocessed file naming convention, this script will identify the raw file name, and delete or simulate deleting any files that contain this same string, except for the raw file and any file beginning with one of the following:\n")

	for keep_string in to_keep:
		print("- ", keep_string)
	print("\n")

#Exits script if no, or quits if invalid response is given.
elif response == 'n':
	abort_script()
else:
	print("Invalid response.")
	abort_script()


# ------------------------------------- FINDING RAW DATA -------------------------------------


#This statement will be used to track whethe a template for raw data within the input directory been specified and confirmed by the user.
raw_confirmed = False

#A dictionary to contain the raw data file name for each subject.
raw_files = {}

#Iterates over the first level of folders within the input directory, which should be subject folders containing preprocessed data.
for subject in sorted(os.listdir(input_path)):

	#Defines the full file path, using the input path, subject ID, and relative location of preprocessed functional data, if relevant.
	if rel_path:
		full_path = os.path.join(input_path, subject, rel_path)
	else:
		full_path = os.path.join(input_path, subject)

	#If the specified full path of this subject is not found, the user is informed that raw data will not be found for this folder.
	if not os.path.exists(full_path):
		print("The specified path does not exist for {}. Cannot look for raw data...".format(subject))	

	#An empty list is added to the raw files dictionary for this subject
	raw_files[subject] = []

	#Sets a counter for the number of final preprocessed files found for this subject.
	preproc_found = 0

	#Iterates over each file in the identified folder.
	for preproc_file in os.listdir(full_path):

		#Finds each file that appears to be fully preprocessed.
		if preproc_file.startswith(preproc_label):

			#Increases the above counter by 1.
			preproc_found += 1
		
			#Saves out a variable that should be the raw version of this file, both the name and full path.
			raw_file = preproc_file[len(preproc_label):]
			raw_path = os.path.join(full_path, raw_file)

			#If this file does exist, it's added to the raw data dictionary for this subject.
			if os.path.isfile(raw_path):
				raw_files[subject].append(raw_file)

	#If no preprocessed data was found for this subject, lets the user know and aborts the rest of this loop for them.
	if preproc_found == 0:
		print("No preprocessed data found in the specified path for {}. Please check the input directory and any relevant relative path has been specified correctly.".format(subject))
		continue

	#Unless the user has already confirmed the convention of raw data naming...
	while raw_confirmed == False:

		#If at least one raw file has been found for this subject...
		if len(raw_files[subject]) > 0:

			#Here, we want users to confirm that the first file suspected to be raw data is in fact raw data. If so, we'll assume it's safe to
			#apply the logic sued here to each subject's folder. The text printed is slightly different depending
			#on whether one or multiple raw files have been found.
			if len(raw_files[subject]) == 1:
				response = input("It appears that the first subject identified has 1 raw file, in the form '{}'. Is this correct? If so, press 'y' to proceed, and this logic will be applied to other subjects. If incorrect, enter 'n' to exit.".format(raw_files[subject][0])).strip().lower()
		
			if len(raw_files[subject]) > 1:
				response = input("It appears that the first subject identified has {} raw files, one of which is in the form '{}'. Is this correct? If so, press 'y' to proceed, and this logic will be applied to other subjects. If incorrect, enter 'n' to exit.".format(len(raw_files[subject]), raw_files[subject][0])).strip().lower()

			#If the user confirms, we'll proceed, and update the above condition so we don't need to repeated this loop.
			if response == 'y':
				print("Proceeding...")
				raw_confirmed = True
				
			#If not, we decide it's not safe to proceed, since we might not have a conventional SPM data structure.
			elif response == 'n':
				print("It may be that your data is not conventionally structured for preprocesed SPM output, or that the provided preprocessed prefix is not correct. This script will not proceed.")
				abort_script()

			#Also exits if we get an invalid key press.
			else:
				print("Invalid response entered.")
				abort_script()


# ------------------------------------- PREPARING FOR EXECTUION -------------------------------------


#These statements is used to tracker whether any files are deleted over the course of the script,
#and whether raw data has been processed for any subjects.
nothing_deleted = True
raw_found = 0

#This function is used to verify that the user is happy to delete the first target file identified.
def check_delete():
	global nothing_deleted
	response = input("The first file to be deleted will be {}/{}. Does this look right? Enter 'y' to proceed with deletion, or 'n' to exit.".format(full_path, preproc_file)).strip().lower()

	#If yes, the file is deleted and we update the above condition so this loop won't be repeated.
	if response == 'y':
		print("\n Proceeding...")
		nothing_deleted = False

		os.remove(string_path)
		print("DELETING {}".format(preproc_file))
					
	#If not, the script is aborted.	
	elif response == 'n':
		abort_script()

	#We also quit if there's an invalid key press.
	else:
		print("Invalid input.")
		abort_script()

#This function is used to delete or simulate deleting files.
def deletion_process(input_file, in_full):

	#If it's the first file that will be actually deleted, we apply the above function.
	if nothing_deleted and method == 'delete':
		check_delete()

	#Otherwise, the file is just deleted.
	elif method == 'delete':
		print("DELETING {}".format(input_file))
		os.remove(in_full)

	#If using a simulation method, the relevant simulation path is defined, and the file is
	#either given a symbolic link or copied into the 'deleted' subfolder.
	elif 'sim' in method:

		print("SIMULATING DELETION FOR {}".format(input_file))
		sim_path = os.path.join(subject_deleted, input_file)

		if 'link' in method:
			os.symlink(in_full, sim_path)

		elif 'copy' in method:
			shutil.copy(in_full, sim_path)

#This function is used for the simulation of files that would be retained.
def retention_process(input_file, in_full):

	#Regardless of the specific simulation method, the simulation path will be the same.
	sim_path = os.path.join(subject_retained, input_file)
	print("SIMULATING RETENTION FOR {}".format(input_file))

	#Depending on the method, the file is either given a symbolic link or copied into the 'retained' subfolder.
	if method == 'sim_link':
		os.symlink(in_full, sim_path)

	elif method == 'sim_copy':
		shutil.copy(in_full, sim_path)


# ------------------------------------- EXECUTING DELETION/SIMULATED DELETION -------------------------------------



#Proceeds with the deletion/simulated deltion of files, iterating over all subjects for whom raw data has been found.
for subject in raw_files:

	#Defines the list of raw files for a given subject (may just be one file).
	raw_list = raw_files[subject]

	#Increases our above counter by 1 if this subject has raw data identified. If not, skips the rest of the loop for this subject.
	if len(raw_list) > 0:
		raw_found += 1
	else:
		continue

	#The full path we're interested in for this subject is defined, based on whether a relative path is provided or not.
	if rel_path:
		full_path = os.path.join(input_path, subject, rel_path)
	else:
		full_path = os.path.join(input_path, subject)

	#If a simulation method is defined, defines and creates subfolders for this subject within both the 'retained' and 'deleted' folders.
	if 'sim' in method:
		subject_retained = os.path.join(retained_dir, subject)
		subject_deleted = os.path.join(deleted_dir, subject)
		os.mkdir(subject_retained)
		os.mkdir(subject_deleted)

	#Iterates over each of these subject's files, and defines a file path for it.
	for preproc_file in os.listdir(full_path):
		string_path = os.path.join(full_path, preproc_file)

		#If a given string contains the name of a raw data file...
		if any(item in preproc_file for item in raw_list):

			#We judge whether we want to keep it. This is based on whether they start with any of the 'to keep' strings,
			#or if it is itself a raw file, or the corresponding .mat file.
			should_keep = any(preproc_file.startswith(keep_string) for keep_string in to_keep) or preproc_file in raw_list
			
			#If the file meets one of these conditions...
			if should_keep:

				#It's just skipped over if using the delete method.
				if method == 'delete':
					continue

				#If using a simulation method, we simulate retaining it using the above function.
				else:
					retention_process(preproc_file, string_path)

			#Otherwise, we proceed with deletion/simulated deletion.
			else:
				deletion_process(preproc_file, string_path)

		#If the file doesn't contain a raw data string, we still need to retain it if using a simulation method.
		elif 'sim' in method:
			retention_process(preproc_file, string_path)

#If no raw files were found for any subjects, we inform the user that no files were marked as appropriate for deletion. They may need to revise their command line.
if raw_found == 0:
	print("\n*** No raw files were found, and no therefore no files were marked appropriate for deletion. Please check that the correct input path structure was specified, and provide an additional relative path (-rel_path) if needed, to reflect subfolders in subjects' folder that contain relevant files. \n")

#We also tell the user if raw files were identified but nothing was deleted (in deletion mode).
elif nothing_deleted and method == 'delete':
	print("\n*** Raw files were identified, but no files were found to be appropriate for deletion... \n")

#Using the function at the top of this script, the simulation folder is deleted if it's empty by the end of the script.
delete_sim()
