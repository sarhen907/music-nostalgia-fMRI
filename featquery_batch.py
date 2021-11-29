

#FEAT QUERY



import os,sys
import argparse
import numpy as np
import re
from datetime import datetime
from subprocess import call
from subprocess import check_output
import csv




datafolder = "/Volumes/MusicProject/Individual_Projects/Sarah.H/Nostalgia_fmri/pilot_analysis/all_possible/withmotion"
subjectDir = "%s/" %(datafolder)
subjectList = [elem for elem in os.listdir(subjectDir) if "." not in elem]

includeList = ['sub-01', 'sub-02', 'sub-03', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-10', 'sub-11', 'sub-12']
subjectList = [elem for elem in subjectList if elem in includeList]
subjectList.sort()
print(subjectList)

maskfolder = "/Volumes/MusicProject/Individual_Projects/Sarah.H/Nostalgia_fmri/roi_masks"
masklist = [elem for elem in os.listdir(maskfolder) if elem.endswith('sphere.nii.gz')]
masklist.sort()
print(masklist)




for subj in subjectList:
    subject = subj
    subjfolder = subjectDir + subject + "/"
    secondlevelfile = subjfolder + "secondlevel.gfeat"
    #print("we are on subject..... %s" %subject)

    for cope in range(1,7):
    #    print("we are on cope ...%d" %cope)
        copepath = secondlevelfile + "/cope%d.feat" %(cope)

        for mask in masklist:
            roiname = mask[:-7]
            print("we are on participant: %s, cope: %d, mask: %s" %(subject, cope,roiname))
            maskpath = maskfolder + "/" +mask
            #print(maskpath)

            print("our command is....")
            command = "/usr/local/fsl/bin/featquery 2 %s %s 1 stats/pe1 featquery_%s -p -s %s" %(copepath, copepath, roiname, maskpath)
            call(command, shell = True)
