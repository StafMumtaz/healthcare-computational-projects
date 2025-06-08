%Mustafa Mumtaz
%Behzad Zareian
%Damisah Lab
%Nov 2023

%Render Screen Open
PsychDefaultSetup(2);  
Screen('Preference', 'SkipSyncTests', 2);
S.kbNum = GetKeyboardIndices();
S.screenNumber = 0;
[S.Window, S.myRect] = Screen(S.screenNumber, 'OpenWindow');
S.white = WhiteIndex(S.Window);
black = BlackIndex(S.Window);
S.screenColor = black;
S.textColor = S.white;
Screen('TextSize', S.Window, 24);
S.on = 1;
Screen(S.Window, 'FillRect', black);
S.xcenter = S.myRect(3)/2;
S.ycenter = S.myRect(4)/2;
win=S.Window;

%Runway Dimensions
Runway_Start_x = S.myRect(3)/8;
Runway_End_x = (S.myRect(3)*7)/8;
Runway_Start_y = (S.myRect(4)*8)/16;
Runway_End_y = (S.myRect(4)*9)/16;
Runway_Height = Runway_End_y - Runway_Start_y;
Safety_Start_x = Runway_End_x - ((Runway_End_x - Runway_Start_x)/10);
Safety_End_x = Runway_End_x;
Half_Safety_Width = (Safety_End_x - Safety_Start_x)/2;
Safety_Start_y = S.ycenter - Half_Safety_Width;
Safety_End_y = S.ycenter + Half_Safety_Width;
R_Unit = (Runway_End_x - Runway_Start_x)/10;
Safety_End = Safety_Start_x+(R_Unit/2);

%Line Dimensions
lineColor = [200 200 200];
lineWidth = 4;
lineHeight = Runway_End_y - Runway_Start_y;
lineStartY = Runway_Start_y;
lineEndY = Runway_End_y; 
linesX = zeros(1,9);
for i = 1:9
    linesX(i) = Runway_Start_x + (R_Unit*i);
end

%Player Dimensions
participantXInitial = Runway_End_x - (2.5*R_Unit);
participantX = participantXInitial;
R_participant = participantX + ((.4*R_Unit)/2);
L_participant = participantX - ((.4*R_Unit)/2);
T_participant = Runway_Start_y + (.15*Runway_Height);
B_participant = Runway_End_y - (.15*Runway_Height);
participantColor = [240 220 0];
participantVertices = [participantX T_participant; L_participant B_participant; R_participant B_participant];

%Predator Distribution Math
SwitchDistanceDomain = participantXInitial - Runway_Start_x;
SwitchDistanceUnits = SwitchDistanceDomain/6;
SwitchFastMean = Runway_Start_x+SwitchDistanceUnits;
SwitchSlowMean = Runway_Start_x + (4*SwitchDistanceUnits);
SwitchTutorialMean = Runway_Start_x + (2.5*SwitchDistanceUnits);
SwitchSD = (3*SwitchDistanceUnits)/12;
Tutorial_Distribution = normrnd(SwitchTutorialMean, SwitchSD, 1, 10);
Fast_Distribution = normrnd(SwitchFastMean, SwitchSD, 1, 100);
Slow_Distribution = normrnd(SwitchSlowMean, SwitchSD, 1, 100);

%Interim Jitter Distribution
InterimMean = 2.5;
InterimSD = .1;
Interim_Distribution = normrnd(InterimMean, InterimSD, 1, 500);

%Predator Dimensions
predatorXInitial = Runway_Start_x - ((0.4*R_Unit)/2);
Radius_Predator = (.9*R_Unit)/2;
predatorColor = [140 140 140];
predatorColorR = [190 75 75];
predatorColorB = [75 110 190];
predatorX = predatorXInitial;
L_predator = predatorX - ((.37*R_Unit)/2);
R_predator = predatorX + ((.37*R_Unit)/2);

%Tutorial Predator Dimensions
tPredator1 = Runway_Start_x+(4*R_Unit);
tPredator2 = Runway_Start_x+(6*R_Unit);
L_predatort1 = tPredator1 - ((.37*R_Unit)/2);
R_predatort1 = tPredator1 + ((.37*R_Unit)/2);
L_predatort2 = tPredator2 - ((.37*R_Unit)/2);
R_predatort2 = tPredator2 + ((.37*R_Unit)/2);

%Speeds
participantSpeed = (3*R_Unit)/50;
fastPredatorSpeed = (3*R_Unit)/20;
slowPredatorSpeed = (.5*R_Unit)/50;

%Monetary Values
accruedMoney = 0;
totalMoney = 0;
rateMoney = .001;

%Trial Structure
Predator_Matrix = zeros(2,200);
Predator_Matrix(1, randperm(200, 100)) = 1;
Predator_Matrix(2,:) = Predator_Matrix(1,:);
zero_indices = find(Predator_Matrix(1,:) == 0);
one_indices = find(Predator_Matrix(1,:) == 1);
Predator_Matrix(2, zero_indices(randperm(numel(zero_indices), 25))) = 1;
Predator_Matrix(2, one_indices(randperm(numel(one_indices), 25))) = 0; %Created a matrix that will define predator movement and color

%Predator Distribution
Gameplay_Distribution = zeros(1,200);
fast_counter = 1;
slow_counter = 1;
for i = 1:200
    if Predator_Matrix(1,i) == 1
        Gameplay_Distribution(i) = Fast_Distribution(fast_counter);
        fast_counter = fast_counter + 1;
    else
        Gameplay_Distribution(i) = Slow_Distribution(slow_counter);
        slow_counter = slow_counter + 1;
    end
end

%{
This seems to be creating a matrix called Gameplay_Distribution which
contains the positioning along the x axis the predator speeds up at for the
duration of the trial
%}

%Loop Switching
Loop_Switch = 1;
Game_Counter = 1;
participantSwitch = 0;
predatorSwitch = 0;
Tutorial_Counter = 1;
Gameplay_Counter = 1;
trialStartSwitch = 0;
endflag = 0;

%Initializing Data Table 1: Behavior
pretable1Behavior = [];

            %TTL PULSE CODE DEPRECATED
            %Testing latency (Can be commented out if not hooked up to Labjack)
            %latencyBenchmark = datetime;
            %latencyTimer = tic;
            %latencyTable = [];
            %test_trigger;
            %latencyTable = [latencyTable; toc(latencyTimer)];
            %test_trigger_bnc;
            %latencyTable(end, 2) = toc(latencyTimer);

%TTL PULSE CODE (Updated)
latencyBenchmark = datetime;
trialTimer = tic;
%{
table3TTL = table(zeros(250, 1), zeros(250, 1), zeros(250, 1), zeros(250, 1), zeros(250, 1), zeros(250, 1), ...
                 'VariableNames', {'GameCounter', 'TrialNumber', 'BeforeTTL', 'AfterTTL', 'BeforeTTL_BNC', 'AfterTTL_BNC'});
table3TTL.BeforeTTL(1) = toc(trialTimer);
test_trigger;
table3TTL.AfterTTL(1) = toc(trialTimer);
table3TTL.BeforeTTL_BNC(1) = toc(trialTimer);
test_trigger_bnc;
table3TTL.AfterTTL_BNC(1) = toc(trialTimer);
%}

%Initializing Data Table 2: FID
%table2FID = zeros(250, 5);
%table2FID = num2cell(table2FID);

table2FID = table(zeros(250, 1), zeros(250, 1), zeros(250, 1), strings(250, 1), strings(250, 1), ...
                  'VariableNames', {'GameplayCounter', 'TrialStart', 'FID', 'Speed', 'Color'});

%{
DEBUGGING
Game_Counter = 420;
Gameplay_Counter = 195;
%}



%%
while 1
pretable1Behavior(end+1, :) = [Game_Counter, Loop_Switch, toc(trialTimer), participantX, predatorX, accruedMoney, totalMoney, Gameplay_Counter];
%--------------------------------------------------------------------------------------------------------------------------------------------    
    %Loop 1
    if Loop_Switch == 1
        
        %Resets
        participantSwitch = 0;
        predatorSwitch = 0;
        trialStartSwitch = 0;
        participantX = participantXInitial;
        predatorX = predatorXInitial;
        R_participant = participantX + ((.4*R_Unit)/2);
        L_participant = participantX - ((.4*R_Unit)/2);
        T_participant = Runway_Start_y + (.15*Runway_Height);
        B_participant = Runway_End_y - (.15*Runway_Height);
        participantVertices = [participantX T_participant; L_participant B_participant; R_participant B_participant];

        %Interim Trial Number
        if Game_Counter == 1
            message = sprintf('You are entering the tutorial to a game. \n\n Press d to continue.'); 
        elseif Gameplay_Counter == 200 && endflag == 0
            message = sprintf('Game over. \n\n You made %.2f dollars total.', totalMoney);
        elseif Gameplay_Counter == 200 && endflag == 1
            message = sprintf(['Thank you for playing this game. \n\n and contributing to research on the brain. \n\n - Damisah Lab']);
        elseif Gameplay_Counter == 200 
            message = sprintf(['You may return the laptop to the researcher']);
        elseif accruedMoney > 0.01 && Game_Counter > 25
            message = sprintf('You have escaped and earned %.2f dollars. \n\n You have %.2f dollars total.', accruedMoney, totalMoney);
        elseif accruedMoney > 0.01 && Game_Counter < 25
            message = sprintf('You have escaped and would have earned %.2f dollars in the game. \n\n You would have %.2f dollars total.', accruedMoney, totalMoney);
        elseif Game_Counter > 25
            message = sprintf('You were caught and made no money this trial. \n\n You have %.2f dollars total.', totalMoney);
        else
            message = sprintf('You were caught and would have made no money this trial. \n\n You would have %.2f dollars total.', totalMoney);
        end
        
        %{
        DEBUGGING
        DrawFormattedText(S.Window, ['Game_Counter: ' num2str(Game_Counter)], S.myRect(3)-300, 40, S.textColor);
        DrawFormattedText(S.Window, ['Tutorial_Counter: ' num2str(Tutorial_Counter)], S.myRect(3)-300, 65, S.textColor);
        DrawFormattedText(S.Window, ['Gameplay_Counter: ' num2str(Gameplay_Counter)], S.myRect(3)-300, 90, S.textColor);
        %}
        DrawFormattedText(S.Window,message,'center','center',S.textColor);
        Screen(S.Window,'Flip');

        KeyIsDown=0
        if Game_Counter == 1 || Gameplay_Counter == 200
            while 1 
                [KeyIsDown, ~, keyCode] = KbCheck(S.kbNum);
                if keyCode(KbName('d'))
                    if Game_Counter == 1
                        Loop_Switch = 2;
                    end
                    Game_Counter = Game_Counter+1;
                    accruedMoney = 0;
                    if Gameplay_Counter == 200
                        endflag = endflag +1;
                    end
                    break;
                elseif keyCode(KbName('space'))
                    sca;
                    return;
                end
            end
            while KeyIsDown
                [KeyIsDown, ~, ~] = KbCheck(S.kbNum);
            end
        else
            pause(Interim_Distribution(Game_Counter));
            message='+';
            DrawFormattedText(win,message,'center','center',S.textColor);
            Screen(S.Window,'Flip');
            
                            %TTL CODE DEPRECATED
                            %test_trigger;
                            %latencyTable = [latencyTable; toc(latencyTimer), 0];
                            %test_trigger_bnc;
                            %latencyTable(end, 2) = toc(latencyTimer);


            %Storing Data
            table1Behavior = array2table(pretable1Behavior, 'VariableNames', ...
            {'Game_Counter', 'Loop_Switch', 'Trial_Duration', 'Participant_X', ...
            'Predator_X', 'Accrued_Money', 'Total_Money', 'Gameplay_Counter'});

            
            pause(.7); %remember to change this back to .5 seconds when running the real game
            predatorX = predatorXInitial;
            Loop_Switch = 2;
            Game_Counter = Game_Counter+1;
            accruedMoney = 0;

            %Saving Desired Data
        end
%--------------------------------------------------------------------------------------------------------------------------------------------    
    %Loop 2
    elseif Loop_Switch == 2
        
        %Time trial start 
        if trialStartSwitch == 0
            trialStart = toc(trialTimer);
            %{
            TTL PULSE RECORDING CODE
            table3TTL.GameCounter(Gameplay_Counter+1) = Game_Counter;
            table3TTL.TrialNumber(Gameplay_Counter+1) = Gameplay_Counter;
            table3TTL.BeforeTTL(Gameplay_Counter+1) = toc(trialTimer);
            test_trigger;
            table3TTL.AfterTTL(Gameplay_Counter+1) = toc(trialTimer);
            table3TTL.BeforeTTL_BNC(Gameplay_Counter+1) = toc(trialTimer);
            test_trigger_bnc;
            table3TTL.AfterTTL_BNC(Gameplay_Counter+1) = toc(trialTimer);
            %}
            trialStartSwitch = 1;
        end

        %Rendering
        if Game_Counter == 25
            Screen('FillOval', win, predatorColorR, [L_predatort1 T_participant R_predatort1 B_participant]);
            Screen('FillOval', win, predatorColorB, [L_predatort2 T_participant R_predatort2 B_participant]);
        else
            Screen('TextSize', win, 24);
            Screen('FillRect', win, [255 255 255], [Runway_Start_x Runway_Start_y Runway_End_x Runway_End_y]);
            Screen('FillRect', win, [50 50 50], [(Runway_Start_x-(0.4*R_Unit)) Runway_Start_y Runway_Start_x Runway_End_y]);
            Screen('FillRect', win, [95 150 90], [Safety_Start_x Runway_Start_y Runway_End_x Runway_End_y]);
            for i = 1:9
            Screen('DrawLine', win, lineColor, linesX(i), lineStartY, linesX(i),lineEndY, lineWidth);
            end
            Screen('FillPoly', win, participantColor, participantVertices);
            if Game_Counter < 25
                Screen('FillOval', win, predatorColor, [L_predator T_participant R_predator B_participant]);
            elseif Game_Counter >24 && Predator_Matrix(2,Gameplay_Counter) == 1
                Screen('FillOval', win, predatorColorR, [L_predator T_participant R_predator B_participant]);
            else
                Screen('FillOval', win, predatorColorB, [L_predator T_participant R_predator B_participant]);
            end
            Screen('FillRect', win, [0 0 0], [(Runway_Start_x-(0.4*R_Unit)) Runway_Start_y Runway_Start_x Runway_End_y]);
            %Screen('FillOval', win, predatorColor, [SwitchFastMean-10-(3*SwitchSD) T_participant SwitchFastMean+10-(3*SwitchSD) B_participant]);
            %Screen('FillOval', win, predatorColor, [SwitchFastMean-10 T_participant SwitchFastMean+10 B_participant]);
            %Screen('FillOval', win, predatorColor, [SwitchSlowMean-10 T_participant SwitchSlowMean+10 B_participant]);
            %Screen('FillOval', win, predatorColor, [SwitchTutorialMean-10 T_participant SwitchTutorialMean+10 B_participant]);
        end
        

        %{
        DEBUGGING
        %TocTest = toc;
        %DrawFormattedText(S.Window, ['Current Time: ' num2str(TocTest)], S.myRect(3)-300, 115, S.textColor);
        DrawFormattedText(S.Window, ['Game_Counter: ' num2str(Game_Counter)], S.myRect(3)-300, 40, S.textColor);
        DrawFormattedText(S.Window, ['Tutorial_Counter: ' num2str(Tutorial_Counter)], S.myRect(3)-300, 65, S.textColor);
        DrawFormattedText(S.Window, ['Gameplay_Counter: ' num2str(Gameplay_Counter)], S.myRect(3)-300, 90, S.textColor);
        %DrawFormattedText(S.Window, ['participantSwitch: ' num2str(participantSwitch)], S.myRect(3)-200, 60, S.textColor);
        %DrawFormattedText(S.Window, ['Tutorial_Counter: ' num2str(Tutorial_Counter)], S.myRect(3)-200, 80, S.textColor);
        %DrawFormattedText(S.Window, ['Accrued Money: $' num2str(accruedMoney)], S.myRect(3)-200, 100, S.textColor);
        %DrawFormattedText(S.Window, ['Total Money: $' num2str(totalMoney)], S.myRect(3)-200, 120, S.textColor);
        %}



        if Game_Counter == 2
            DrawFormattedText(win, ['\n \n \n \n  \n \n \n \n  \n The yellow triangle is your avatar.'], 'center', 20, [255 255 255]);
            DrawFormattedText(win, ['\n \n \n \n  \n \n \n \n  \n \n \n The circle is the predator.'], 'center', 20, [255 255 255]);
            DrawFormattedText(win, ['\n \n \n \n  \n \n \n \n  \n \n \n \n \n Press d when you understand.'], 'center', 20, [255 255 255]);
        elseif Game_Counter == 3
            DrawFormattedText(win, ['\n \n \n \n  \n \n \n \n  \n Your job is to escape the predator.'], 'center', 20, [255 255 255]);
            DrawFormattedText(win, ['\n \n \n \n  \n \n \n \n  \n \n \n But you make money by staying as long as you can.'], 'center', 20, [255 255 255]);
            DrawFormattedText(win, ['\n \n \n \n  \n \n \n \n  \n \n \n \n \n Press d when you understand.'], 'center', 20, [255 255 255]);
        elseif Game_Counter == 4
            DrawFormattedText(win, ['\n \n \n \n  \n \n \n \n  \n You lose money from each trial when caught.'], 'center', 20, [255 255 255]);
            DrawFormattedText(win, ['\n \n \n \n  \n \n \n \n  \n \n \n The predator can speed up at any time.'], 'center', 20, [255 255 255]);
            DrawFormattedText(win, ['\n \n \n \n  \n \n \n \n  \n \n \n \n \n Press d to begin.'], 'center', 20, [255 255 255]);
        elseif Game_Counter == 25
            DrawFormattedText(win, ['\n \n \n \n  \n \n \n \n  \n The red predator is usually faster than the blue predator.'], 'center', 20, [255 255 255]);
            DrawFormattedText(win, ['\n \n \n \n  \n \n \n \n  \n \n \n You will earn real money for each trial going forward.'], 'center', 20, [255 255 255]);
            DrawFormattedText(win, ['\n \n \n \n  \n \n \n \n  \n \n \n \n \n Press d to begin.'], 'center', 20, [255 255 255]);
        end
        Screen(S.Window,'Flip');
        
        %Tutorial Predator Movement Mechanics
            if Game_Counter >4 && Game_Counter < 25
            if predatorX < Tutorial_Distribution(Tutorial_Counter)  
                predatorX = predatorX + slowPredatorSpeed;
                L_predator = predatorX - ((.37*R_Unit)/2);
                R_predator = predatorX + ((.37*R_Unit)/2);
            elseif predatorX < Safety_Start_x
                predatorX = predatorX + fastPredatorSpeed;
                L_predator = predatorX - ((.37*R_Unit)/2);
                R_predator = predatorX + ((.37*R_Unit)/2);
            end
            end
        %Real Game Predator Movement Mechanics
            if Game_Counter >25 
            if predatorX < Gameplay_Distribution(Gameplay_Counter)  
                predatorX = predatorX + slowPredatorSpeed;
                L_predator = predatorX - ((.37*R_Unit)/2);
                R_predator = predatorX + ((.37*R_Unit)/2);
            elseif predatorX < Safety_Start_x
                predatorX = predatorX + fastPredatorSpeed;
                L_predator = predatorX - ((.37*R_Unit)/2);
                R_predator = predatorX + ((.37*R_Unit)/2);
            end
            end
        
        %Predator Game Termination    
        if predatorX >= Safety_Start_x
            Loop_Switch = 1;
            Game_Counter = Game_Counter+1;
            totalMoney = accruedMoney + totalMoney;
                if Game_Counter < 25
                Tutorial_Counter = Tutorial_Counter+1;
                else
                Gameplay_Counter = Gameplay_Counter+1;
                end
        end

        %Participant Movement Mechanics & Tutorial Exception
        if participantSwitch == 1 && participantX < Safety_End
            participantX = participantX + participantSpeed;
            R_participant = participantX + ((.4*R_Unit)/2);
            L_participant = participantX - ((.4*R_Unit)/2);
            participantVertices = [participantX T_participant; L_participant B_participant; R_participant B_participant];
        end

        %Capture Mechanics
        if predatorX >= participantX - (.1*R_Unit)
            Loop_Switch = 1;
            Game_Counter = Game_Counter+1;
            if participantX < Safety_Start_x
                accruedMoney = 0;
                if Game_Counter < 25
                Tutorial_Counter = Tutorial_Counter+1;
                else
                Gameplay_Counter = Gameplay_Counter+1;
                end
            end
            pause(.1);
        end
        
        KeyIsDown=0
        while participantSwitch == 0
            
            %Money Mechanics
            if Game_Counter > 4
                accruedMoney = accruedMoney + rateMoney;
            end
            
            [KeyIsDown, ~, keyCode] = KbCheck(S.kbNum);
            if keyCode(KbName('d')) && Game_Counter >1 && Game_Counter <5
                Game_Counter = Game_Counter+1;
                while KeyIsDown
                    [KeyIsDown, ~, ~] = KbCheck(S.kbNum);
                end
                break;
            elseif keyCode(KbName('d')) && Game_Counter == 25
                totalMoney = 0;
                Game_Counter = Game_Counter+1;
                predatorX = predatorXInitial;
                while KeyIsDown
                    [KeyIsDown, ~, ~] = KbCheck(S.kbNum);
                end
                break;
            %Temporary Skip Key {
            elseif keyCode(KbName('p')) && Game_Counter >3 && Game_Counter <24
                Game_Counter = Game_Counter+1;
                Loop_Switch = 1;
                while KeyIsDown
                    [KeyIsDown, ~, ~] = KbCheck(S.kbNum);
                end
                break;          
            elseif keyCode(KbName('d'))
                participantSwitch = 1;

                %Recording data on prey escape
                table2FID.GameplayCounter(Gameplay_Counter) = Gameplay_Counter;
                table2FID.TrialStart(Gameplay_Counter) = trialStart;
                table2FID.FID(Gameplay_Counter) = toc(trialTimer);
                if Game_Counter > 24 && Predator_Matrix(1, Gameplay_Counter) == 1
                    table2FID.Speed{Gameplay_Counter} = 'Fast';
                    elseif Game_Counter > 24 && Predator_Matrix(1, Gameplay_Counter) == 0
                    table2FID.Speed{Gameplay_Counter} = 'Slow';
                    else
                    table2FID.Speed{Gameplay_Counter} = 'Tutorial';
                    end
                if Game_Counter > 24 && Predator_Matrix(2, Gameplay_Counter) == 1
                    table2FID.Color{Gameplay_Counter} = 'Red';
                    elseif Game_Counter > 24 && Predator_Matrix(2, Gameplay_Counter) == 0
                    table2FID.Color{Gameplay_Counter} = 'Blue';
                    else
                    table2FID.Color{Gameplay_Counter} = 'Grey';
                    end
                %while KeyIsDown
                %    [KeyIsDown, ~, ~] = KbCheck(S.kbNum);
                %end
                break;
            elseif keyCode(KbName('space'))
                sca;
            else
                break;
            end
        end
        
    end
end
