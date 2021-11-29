function makeruns_mp(subj)

%this script will make folders for each run (two per participant)

%1. take all the songs, put them in triplets as variables
%2. shuffle the triplets
%3. choose 3 triplets, put them in one folder
%4. put the other triplets in the other folder

%input is the subject ID. which MUST MATCH THE NAME OF THE FOLDER that
%their stimuli are in. 

%this script should be run PRIOR to starting the scan. 

stimpath = sprintf([pwd '/stimuli/%s'],subj);

if isempty(stimpath) == 1
    error('there are no stimuli in this folder! please add songs.')
end


run1path = [stimpath '/run1'];

run2path = [stimpath '/run2'];

% make empty folders
if not(isfolder(run1path))
    mkdir(run1path)
else
    ow1 = input('you already have a run1 folder for this participant. are you sure you want to overwrite? y n \n','s');
    if ow1 == 'n'
        return;
    end  
end

if not(isfolder(run2path))
    mkdir(run2path)
else
    ow2 = input('you already have a run2 folder for this participant. are you sure you want to overwrite? y n \n','s');
    if ow2 == 'n'
        return;
    end  
end


% get songs
songfilelist = dir(stimpath);
songfileNames = {songfilelist(:).name};
%remove hidden files
for i = 1:3
    songfileNames{i} = [];
end

songfileNames = songfileNames(~cellfun(@isempty, songfileNames));



% set up pairs of songs in variables
Pair1 = {'N1.m4a';'C1.m4a';'U1.m4a'};
Pair2 = {'N2.m4a';'C2.m4a';'U2.m4a'};
Pair3 = {'N3.m4a';'C3.m4a';'U3.m4a'};
Pair4 = {'N4.m4a';'C4.m4a';'U4.m4a'};
Pair5 = {'N5.m4a';'C5.m4a';'U5.m4a'};
Pair6 = {'N6.m4a';'C6.m4a';'U6.m4a'};

mypairs = strings(1,6);
for j=1:6
    mypairs(j) = sprintf('Pair%d',j);
end

% shuffle var names
pair_rand = randperm(6); %assigns random numbers
pairorder = mypairs(pair_rand); % .m4a titles randomized


%put songs in the folders 

for i = 1:6
    pairname = eval(pairorder(i));
    fromfile1 = sprintf([stimpath '/%s'],pairname{1});
    fromfile2 = sprintf([stimpath '/%s'],pairname{2});
    fromfile3 = sprintf([stimpath '/%s'],pairname{3});
    %do things with it.
    if i < 4
        movefile(fromfile1, run1path)
        movefile(fromfile2, run1path)
        movefile(fromfile3, run1path)
    end
    if i > 3
        movefile(fromfile1, run2path)
        movefile(fromfile2, run2path)
        movefile(fromfile3, run2path)
    end
end

fprintf('done!\n')

end