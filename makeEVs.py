#This program will make EV files from the logfile collected during nostalgia pilot fmri task

#this was edited in 2021 to run specifically before fmri analysis of pilots )
#Sarah Hennessy, 2021


import os
import sys
import csv
import pandas as pd
import numpy as np

#reload(sys)

def score(datafolder, subject_outpath):


    #where are your log files located?

    #subjectlist = [elem for elem in os.listdir(datafolder) if "run" in elem]
    subjectlist = [elem for elem in os.listdir(datafolder) if ".DS_Store" not in elem]
    #subjectlist = [elem for elem in os.listdir(datafolder)]

    print ('your subject list is:',subjectlist)

    #change this for each group.
    #subject_outpath = "/Volumes/MusicProject/Longitudinal_study/Functional/Year7/Y7_blocks/Control"


    for subject in subjectlist:
         #subject = indiv file
        subj = subject
        #run = subject[-5]
        subjectfolder = datafolder + "/%s" %(subject)
        evfolder = subject_outpath + '/%s' %(subj)


        #log = datafolder + '/%s_emo_gonogo_run%s.txt' %(subj,run)

        #where do you want evs to go (change for each group)
        #evpath = "/Volumes/MusicProject/Longitudinal_study/Functional/Year7/Y7_2.3/Control"

        #evfolder = evpath + '/%s_%s_evs' %(subj, run)
        if os.path.exists(evfolder):
            print('Subject %s already has ev folder' %subj)
        else:
            os.makedirs(evfolder)

            evlist = [elem for elem in os.listdir(subjectfolder) if "run" in elem]
            for log in evlist:
                run = log[-5]
                print("you are working on %s, run: %s" %(subj, run))
                log_path_full = subjectfolder + "/%s" %(log)
                data = pd.read_csv(log_path_full, delim_whitespace = True, comment = "#", header = "infer", skip_blank_lines = True, engine = "python")
                maxlen = data.shape[0]




        #
        #
        # #read in the text file
        #
        # data = pd.read_csv(log, delim_whitespace = True, comment = "#", header = "infer", skip_blank_lines = True, engine = "python")
        #
        #
        # print('you are on run:',run)
        # print('you are on subject:',subj)
        #
        # maxlen = data.shape[0]

                for index, row in data.iterrows():


                    #RED
                        if row.stimname.startswith("N") == 1:
                             devfilename = evfolder + '/N_run%s.txt' %(run)
                             devfile = open(devfilename, 'a')
                             #triallength = row.stimend - row.stimstart
                             devfile.write('%0.4f\t%0.4f\t1\n' %(row.stimstart, row.stimlength))
                             devfile.close()


                        elif row.stimname.startswith("C") == 1:

                             hevfilename = evfolder + '/C_run%s.txt' %(run)
                             hevfile = open(hevfilename, 'a')
                            # triallength = row.stimend - row.stimstart
                             hevfile.write('%0.4f\t%0.4f\t1\n' %(row.stimstart, row.stimlength))
                             hevfile.close()

                        elif row.stimname.startswith("U") == 1:

                             mevfilename = evfolder + '/U_run%s.txt' %(run)
                             mevfile = open(mevfilename, 'a')
                            # triallength = row.stimend - row.stimstart
                             mevfile.write('%0.4f\t%0.4f\t1\n' %(row.stimstart, row.stimlength))
                             mevfile.close()
if __name__ == '__main__':
 try:
     score(*sys.argv[1:])
 except:
     print(red + "you have run this incorrectly!To run, type:\n \
     'python3.7 [name of script].py [full path of DATA FOLDER] [full path of OUTPUT folder]'")
