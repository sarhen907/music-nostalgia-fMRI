# for Nostalgia fmri study, pilot scans
# Sarah 2021 B&M lab


# you need to have the gsed version of sed added to your bash profile
# can install it with brew install gnu-sed, then add to path.

#scriptshell modeled from Matt's stroop analysis (on server)

#Skull-stripping scripts are under /scripts on the server



import os,sys
import argparse
import numpy as np
import re
from datetime import datetime
from subprocess import call
from subprocess import check_output
import csv


sectionColor = "\033[94m"
sectionColor2 = "\033[96m"
groupColor = "\033[90m"
mainColor = "\033[92m"

pink = '\033[95m'
yellow = '\033[93m'
red = '\033[91m'

ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser()

parser.add_argument("--nobet",help="skip brain extraction", action="store_true")
parser.add_argument("--nofirst",help="skip first level feat", action="store_true")
parser.add_argument("--nosecond",help="skip second level feat", action="store_true")


args = parser.parse_args()

#def score(datafolder):

#parse command line arguments

datafolder = "/Volumes/MusicProject/Individual_Projects/Sarah.H/Nostalgia_fmri/pilot_analysis/all_possible/withmotion"


#set locations

genericdesign = "%s/designs/generic_firstlevel_motion.fsf" %(datafolder)
#genericdesign_noscrub = "%s/designs/generic_firstlevel_noscrub.fsf" %(datafolder)

#COME BACK TO THIS
secondleveldesign = "%s/designs/generic_secondlevel.fsf" %(datafolder)

#set analysis values
numconfounds = 8
smoothmm = 5	#smoothing sigma fwhm in mm
smoothsigma = smoothmm/2.3548	#convert to sigma
additive = 10000	#value added to distinguish brain from background
brightnessthresh = additive * .75


#logging colors



count = 0


#groupList = ['Control', 'Music','Sport']

#for group in groupList:

subjectDir = "/%s/" %(datafolder)
subjectList = [elem for elem in os.listdir(subjectDir) if "." not in elem]


##### if you need to run one subject at a time #####
includeList = ['sub-01', 'sub-02', 'sub-03', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-10', 'sub-11', 'sub-12']
subjectList = [elem for elem in subjectList if elem in includeList]

subjectList.sort()

print(subjectList)

for subj in subjectList:
	subject = subj

	subjfolder = subjectDir + subject + "/"
	#print sectionColor2 + 'Starting on %s group %s %s' %(group,subject,mainColor)
	logfile = subjfolder + "analysis_log.txt"
	evfolder_sub = datafolder + "/EVs/%s" %subject
	checkevfile = evfolder_sub + "/N_run1.txt"
	finalfile = subjfolder + "secondlevel.gfeat/cope1.feat"

	if os.path.exists(finalfile):
		count = count + 1
		print(count,subject,finalfile)

	#Skip this subject if they do not have ev files
	if not os.path.exists(checkevfile):
		print(sectionColor + "The subject %s has no EV Files. Moving on%s") %(subject,mainColor)
		continue

	mprage = subjfolder + "mprage.nii.gz"
	t1image = subjfolder + "mprage_brain.nii.gz"
	fieldmap_rad = subjfolder + "fieldmap_phase_rad.nii.gz"



	print("###############################")
	print("BRAIN EXTRACTION, COMMENCING")


	if not args.nobet:

		if not os.path.exists(t1image):
			print("Skull Stripping mprage for %s" %subj)
			command = "%s/scripts/skullstrip.py %s" %(datafolder,subjfolder)
			print(command)
			call(command,shell = True)


		else:
			print("skull stripping already done!")


	print("###############################")
	print("FIELDMAP PREP, COMMENCING")


	if not os.path.exists(fieldmap_rad):
		print("Preparing fieldmap for %s" %subj)

		print("Skull Stripping fieldmap for %s" %subj)
		command = "%s/scripts/skullstrip_field.py %s" %(datafolder,subjfolder)
		print(command)
		call(command,shell = True)


		phase =subjfolder + "fieldmap_phase.nii.gz"
		magbrain = subjfolder + "fieldmap_mag_brain.nii.gz"
		radout = subjfolder + "fieldmap_phase_rad.nii.gz"

		command = "fsl_prepare_fieldmap SIEMENS %s %s %s 2.5" %(phase,magbrain,radout)
		print(command)
		call(command, shell = True)
	else:
		print("fieldmap prep already done!")



		####################
		# First level analysis
		####################

	if not args.nofirst:

			for run in range(1,3):
				print("we are on run...%d" %run)

				firstlevel_featfolder = subjfolder + "firstlevel_nostalgia_run%d.feat" %(run)
				inputfile = subjfolder + "run%d.nii.gz" %(run)

				designOutput = subjfolder + "firstlevel_nostalgia_design_run%d.fsf" %(run)

				checkfile = firstlevel_featfolder + "/rendered_thresh_zstat5.nii.gz" #check this




				print("###############################")
				print("SCRUB-A-DUB DUBBING")

				# DVARS Scrubbing Motion Correction
				scrubout = subjfolder + "scrub_confounds_stop_run%d" %(run)
				command = "fsl_motion_outliers -i %s -o %s" %(inputfile, scrubout)

				if not args.nobet:
					if not os.path.exists(scrubout):
						print("scrubbing for %s run %d" %(subj, run))
						#command = "%sscripts/skullstrip.py %s" %(datafolder,subjfolder)
						print(command)
						call(command,shell = True)
						print("i completed scrubbing for %s run %d" %(subj, run))

					else:
						print("scrubbing already done for this one! moving on.")
				print("###############################")

				print("FIRST LEVEL FEAT, COMMENCING")

				print("First level FEAT Analysis for: %s, run: %d" %(subject,run))


				if not os.path.exists(inputfile):
					print("Run %s for subject %s does not exist or is not in folder. Moving on.%s" %(run,subject))
					continue

				# Get number of volumes:
				if os.path.exists(checkfile):
					print(checkfile)
					print("First level feat analysis already completed for %s, run %d. Moving on." %(subject,run))
					continue
				else:

					command = 'fslinfo %s' %(inputfile)
					results = check_output(command,shell=True)
					numtimepoints_1 = results.split()[9]

					numtimepoints = numtimepoints_1.decode()
					print("Number of volumes: %s" %(numtimepoints))

					#set up evfiles

					evfile1 = evfolder_sub + "/C_run%d.txt" %(run)
					evfile2 = evfolder_sub + "/N_run%d.txt" %(run)
					evfile3 = evfolder_sub + "/U_run%d.txt" %(run)

					# define fieldmaps

					fm_phase = subjfolder + "fieldmap_phase_rad.nii.gz"
					fm_mag = subjfolder + "fieldmap_mag_brain.nii.gz"


					command = 'gsed -e "s|DEFINEINPUT|%s|g" -e "s|DEFINEOUTPUT|%s|g" -e "s|DEFINESCRUB|%s|g" -e "s|DEFINEFIELDMAP_PHASERAD|%s|g" -e "s|DEFINEFIELDMAP_MAG|%s|g" -e "s|DEFINESTRUCT|%s|g" -e "s|DEFINEVOLUME|%s|g" -e "s|DEFINEEVFILE1|%s|g" -e "s|DEFINEEVFILE2|%s|g" -e "s|DEFINEEVFILE3|%s|g" %s>%s' %(re.escape(inputfile),re.escape(firstlevel_featfolder), re.escape(scrubout), re.escape(fm_phase),re.escape(fm_mag), re.escape(t1image), numtimepoints,re.escape(evfile1),re.escape(evfile2), re.escape(evfile3), genericdesign,designOutput)
					#print(command)
					call(command, shell = True)

					print(designOutput)
					command = "feat %s" %designOutput
					call(command, shell = True)

					print('i have finished first level feating for %s run: %d' %(subject, run))

	####################
	# Second level analysis
	####################

	if not args.nosecond:

		secondlevel_folder = subjfolder + "secondlevel.gfeat"
		feat1 = subjfolder + 'firstlevel_nostalgia_run1.feat'
		feat2 = subjfolder + 'firstlevel_nostalgia_run2.feat'

		if not os.path.exists(feat1) or not os.path.exists(feat2):
				print (sectionColor + "One or more first level feat folders did not complete correctly or does not exist for subject %s. Moving on.%s" %(subject,mainColor))
				continue

		checkcopefolder = secondlevel_folder + "/cope5.feat/rendered_thresh_zstat1.nii.gz"

		print (sectionColor2 + "Second Level Analysis for: %s%s"  %(subject,mainColor))

		if not os.path.exists(checkcopefolder):
			designOutput2 = subjfolder + "secondlevel_nostalgia_design.fsf"
			command = "gsed -e 's|DEFINEOUTPUT|%s|g' -e 's|DEFINEFEAT1|%s|g' -e 's|DEFINEFEAT2|%s|g' %s > %s" %(re.escape(secondlevel_folder),re.escape(feat1), re.escape(feat2),secondleveldesign,designOutput2)

			call(command, shell = True)
			command = "feat %s" % designOutput2
			call(command, shell= True)
			print('i have finished second level feating for %s' %subject)

		else:

			#print checkcopefolder
			print(sectionColor + "Second level for %s already completed, moving on %s\n"  %(subject,mainColor))


print("################")
print("ALL DONE! GO TAKE A LOOK @ YOUR DATA!!!!")
print("################")
