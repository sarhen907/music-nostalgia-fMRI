#featquery_extractvalues


# after running featquery_batch.py, run this to extract the values from the report.txt and put into one txt file


import os,sys
import argparse
import numpy as np
import re
from datetime import datetime
from subprocess import call
from subprocess import check_output
import csv
import pandas as pd


outfilename = "/Volumes/MusicProject/Individual_Projects/Sarah.H/Nostalgia_fmri/pilot_analysis/all_possible/withmotion/total_featquery.csv"
datafolder = "/Volumes/MusicProject/Individual_Projects/Sarah.H/Nostalgia_fmri/pilot_analysis/all_possible/withmotion"
subjectDir = "%s/" %(datafolder)
subjectList = [elem for elem in os.listdir(subjectDir) if "." not in elem]

includeList = ['sub-01', 'sub-02', 'sub-03', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-10', 'sub-11', 'sub-12']
#includeList = ['sub-01', 'sub-02', 'sub-03', 'sub-05', 'sub-06', 'sub-07', 'sub-08']
subjectList = [elem for elem in subjectList if elem in includeList]
subjectList.sort()
print(subjectList)

maskfolder = "/Volumes/MusicProject/Individual_Projects/Sarah.H/Nostalgia_fmri/roi_masks"
masklist = [elem for elem in os.listdir(maskfolder) if elem.endswith('sphere.nii.gz')]
masklist.sort()
print(masklist)

cope_dict = {1:"nos_rest",2:"con_rest",3:"un_rest",4:"nost_un",5:"nost_con",6:"con_un"}

colnames = ['id','contrast','roi','mean','sd','nvox']
i = 1
newdf = pd.DataFrame(columns = colnames, index = range(6*10*(len(masklist))))

for subj in subjectList:
    subject = subj
    subjfolder = subjectDir + subject + "/"
    secondlevelfile = subjfolder + "secondlevel.gfeat"
    for cope in range(1,7):
        copepath = secondlevelfile + "/cope%d.feat" %(cope)
        print(cope_dict.get(cope))
        for mask in masklist:
            i = i+1
            roiname = mask[:-7]
            queryfile = copepath + "/featquery_%s/report.txt" %roiname
            #print(queryfile)
            data = pd.read_csv(queryfile, sep = " ", header = None)
            #print(data)
            newdf['id'][i] = subj
            newdf['contrast'][i] = cope_dict.get(cope)
            newdf['roi'][i] = roiname
            newdf['mean'][i] = data[5][0]
            newdf['sd'][i] = data[9][0]
            newdf['nvox'][i] = data[2][0]

newdf = newdf.dropna(axis=0, how='all')
newdf.to_csv(outfilename,index =False)
