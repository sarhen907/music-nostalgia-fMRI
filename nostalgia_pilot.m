 function nostalgia_pilot(subjectCode, run)

 % This task was written by Sarah Hennessy (hennessy.sarah907@gmail.com)
 %in October 2021. It was created for the project "neural correlates of music-evoked nostalgia".

    if run > 2
        input('You indicated an incorrect run number. \nPress enter and please try again (choose 1 or 2).\n ');
        return;
    end

    songdir = sprintf([pwd '/stimuli/%s/run%d'],subjectCode,run);
    if exist(songdir, 'dir') == 0
        error('You have not run makeruns.m for this participant.')
    end



    Screen('Preference', 'SkipSyncTests', 1)
    %stop sync
    KbName('UnifyKeyNames');                    %use unified keyboard key names (multi-OS compatibility)
    Screen('Preference','VisualDebugLevel',0);  %make sure to get errors printed
    Screen('Preference', 'Verbosity', 1)
    Screen('Preference', 'SkipSyncTests', 1)

    %randomize seed
    rng shuffle

    %CONTROL CLIP TIME, SIZE
    % NEED?
    soundvolume=1;  % 0 to 1


    %DEFINE COLORS
    black = [0 0 0];
    white = [255 255 255];
    gray  = [200 200 200];
    red = [255 0 0];
    blue = [0,200,255];
    defaultFont = 'Helvetica';
    backgroundColor = black;
    textColor = white;

    %DEFINE FIXATION CROSS
    fixationsize = 10;
    fixationlines = [-fixationsize-1 fixationsize 0 0;0 0 -fixationsize fixationsize];
    fixationwidth = 2;
    fixationcolor = white;

    %Initialize the sound drive
    InitializePsychSound

    %Set up logfile
    logfiledir = sprintf([pwd '/logfiles/%s'],subjectCode);
    mkdir(logfiledir);

    logfilename = sprintf('%s_run%d.txt',subjectCode,run) %s is subject codename

    %Check if logfiles exist
    if exist([logfiledir,logfilename], 'file') == 2
        input('That file already exists! Press ENTER and try again. ');
        return;
    end


    fprintf('Opening logfile: %s\n',logfilename); %prints to screen
    logfile = fopen(sprintf([logfiledir '/%s'], logfilename),'a');
    fprintf (logfile, 'trial\tstimname\tstimstart\tstimend\tstimlength\n');

    %OPEN THE SCREEN
    %[w,rect]=Screen('OpenWindow', max(Screen('screens')), 0);


    %%%SET UP SCREEN PARAMETERS
    screens = Screen('Screens');

    screenNumber = max(screens);


    %BRING BACK FOR REAL THING
    HideCursor;
  %  [Screen_X, Screen_Y]=Screen('WindowSize',0);

    % USE THESE LINES FOR SET SCREEN
   % screenRect = [0 0 1024 768];
  %  [w, rect] = Screen('OpenWindow', screenNumber, 0, [0 0 1024 768]);%, screenRect);

  %  [w, rect] = Screen('OpenWindow', screenNumber, 0, [0 0 600 300]);%, screenRect);



    % USE THIS FOR REAL EXPERIMENT
     [w,rect]=Screen('OpenWindow', max(Screen('screens')), 0);

    %SAVE SCREEN DIMENSIONS
    screenX = rect(3);
    screenY = rect(4);
    xcenter = screenX/2;
    ycenter = screenY/2;
    Screen('TextSize' ,w, 38);
    Screen('TextFont',w,'Helvetica');
    DrawFormattedText(w, 'we will start shortly...', 'center', 'center',textColor);
    Screen(w, 'Flip');

   fprintf('\nwaiting for scanner trigger...\n');

   %%%Experiment start time

    doneCode=KbName('5%');
    while 1
        [ keyIsDown, timeSecs, keyCode ] = KbCheck(-1);
        if keyIsDown
            index=find(keyCode);
            if (index==doneCode)
                expStart = timeSecs; %Record start time
                fprintf('trigger received\n')
                break;
            end
        end
    end

    fprintf('\ndrawing initial black screen. We will start in 5 seconds\n');

    %DRAW FIXATION
    Screen('FillRect', w,backgroundColor);
    %Screen('DrawLines',w,fixationlines,fixationwidth,fixationcolor,[xcenter ycenter]);
    Screen('Flip',w);
%     expStart;

    BreakableWait(5);

    songfilelist = dir(songdir);
    songfileNames = {songfilelist(:).name};

     %remove hidden files
    for i = 1:2
       songfileNames{i} = [];
    end

    songfileNames = songfileNames(~cellfun(@isempty, songfileNames));

    group1= {songfileNames{1:3}};
    g1_ordernames = group1(randperm(3));

    group2 = {songfileNames{4:6}};
    g2_ordernames = group2(randperm(3));

    group3 = {songfileNames{7:9}};
    g3_ordernames = group3(randperm(3));

    triplet_perm = randperm(3);


    global finalorder
    finalorder = {};
    for k = 1:3
        for i = 1:3
            mygroup = eval(sprintf('g%d_ordernames',triplet_perm(i)));
            myitem = mygroup(k);
            localitems{i} = myitem;
        end

        finalorder = [finalorder, localitems];
    end


    %Save the trial order
    counter = 0;
    outfilenametest = sprintf([pwd '/trialorder_music/%s_run%d_trialorder.mat'],subjectCode,run);
    if exist(outfilenametest) == 2
        counter = 0 + 1;
        outfilename = sprintf('%s_run%d_trialorder_%d.mat',subjectCode, run, counter);
    else
        outfilename = sprintf('%s_run%d_trialorder.mat',subjectCode,run);
    end

    save([pwd '/trialorder_music/' outfilename],'finalorder');

    songOrder = finalorder;

    %% Loop through each file:
    for i = 1:length(songOrder)
        songfileName = songOrder{i}{:};
        songpath = sprintf('%s/%s',songdir, songfileName);
        fprintf('playing....%s\n',songfileName);

        %DRAW FIXATION
        Screen('FillRect', w,backgroundColor);
        Screen('DrawLines',w,fixationlines,fixationwidth,fixationcolor,[xcenter ycenter]);
        Screen('Flip',w);
        if i~= 1
            %REST between blocks
            fprintf('\n resting....')
            BreakableWait(15);
        end

        %Read in sound data from file
        [soundData,freq] = audioread(songpath);

        %prepare song data
        soundData = soundData';
        numchannels = size(soundData,1);
        if numchannels < 2
            soundData = [soundData; soundData];
            numchannels = 2;
        end


        %open the audio driver
        pahandle = PsychPortAudio('Open',[], [], 0, freq, numchannels);

        %Fill the buffer
        PsychPortAudio('Fillbuffer',pahandle,soundData);

        %play the sound
        playTime = PsychPortAudio('Start',pahandle, [], [],1);
        soundStartTime = playTime-expStart;
        fprintf('Sound started playing %.2f seconds after start of script\n',soundStartTime);

        BreakableWait(40); %CHANGE TO 30 when you are ready for real thing
        PsychPortAudio('Stop',pahandle);
        PsychPortAudio('Close');
        stimEnd = GetSecs;
        soundEndTime = stimEnd- expStart;
        totalsoundtime = soundEndTime-soundStartTime;
        fprintf('audio played for %d seconds\n',totalsoundtime)

        %WrireakableWaitte to log file
        fprintf(logfile,'%d\t%s\t%3f\t%3f\t%3f\n',i,songfileName,soundStartTime,soundEndTime,totalsoundtime);


    end

    text = 'You have completed this portion of the study.\n\n Please await further instructions.';
    Screen('FillRect',w,backgroundColor);
    wrapAt = 50;
    DrawFormattedText(w, text,'centerblock', 'center',textColor, wrapAt);
    Screen('Flip',w);
    BreakableWait(2)
    fprintf('Successfully completed RUN %d.\n\n', run);
    %close
    Screen('CloseAll');

    bigend = GetSecs;
    bigtime = bigend-expStart;
    bigtime

    PsychPortAudio('Stop',pahandle);
    PsychPortAudio('Close',pahandle);
    sca;

end
