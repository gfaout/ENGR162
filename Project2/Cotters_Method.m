clearvars
%% Prompt User for Inputs

test = 1;
while test == 1
    np = input('Enter the number of parameters being considered: ');
    if (np >= 3 && np <= 10)
        test = 0;
    else
        disp(['This program only works with simulations of 3 to 10 ' ... 
        'parameters.']);
    end
end
% Store parameters in a structure
x = struct;
for i = 1:np
    x(i).parameter = input('Parameter: ', 's');
    x(i).low = input('Parameter Low Value: ');
    x(i).high = input('Parameter High Value: ');
end
num_trials = 2*np + 2;  %calculate number of trials

%% Create Matrix of Trials - Nothing Wrong with this Section, DO NOT EDIT
% 1 Represents a High Value and 0 Represents a Low Value

%initially set up matrix as all 0's
Sims = zeros(np, num_trials);      %Sims stands for simulations, this represents the matrix of highs and lows for each simulation
j = num_trials; 
%fill right half of matrix with 1's
while j > (num_trials / 2) 
    Sims(:, j) = 1;
    j = j - 1;
end
%Complete left half of matrix by placing necessary 0's
while j > 1 
    Sims(j - 1, j) = 1;
    j = j - 1;
end
j = num_trials - 1;
%Complete right half of matrix by placing necessary 1's
while j > (num_trials / 2) 
    Sims(j - (np + 1), j) = 0;
    j = j - 1;
end

%% Calculate y values
% Utilize function cottersfunction to calculate y values and store them to 
% structure x

for i = 1:num_trials
    for j = 1:np
        if Sims(j,i) == 1
            highlowX(j) = x(j).high;
        else
            highlowX(j) = x(j).low;
        end
    end
    x(i).output = cottersfunction(highlowX);
end

%% Calculate Even and Odd Contrasts

Co = zeros(np); %Odd contrast
Ce = zeros(np); %Even contrast
for i = 1:np
    Co(i) = 0.25*((x(2*np+2).output - x(i+np+1).output)+(x(i+1).output ...
    - x(1).output));
    Ce(i) = 0.25*((x(2*np+2).output - x(i+np+1).output)-(x(i+1).output ...
    - x(1).output));
end

%% Calculate Measure and Sensitivity

M = zeros(np); %Measure
S = zeros(np); %Sensitivity
M_total = 0; %sum of measures
for i = 1:np
    M(i) = abs(Co(i)) + abs(Ce(i));
    M_total = M_total + M(i);
end

for i = 1:np
    S(i) = M(i) / M_total;
end

%% Plot Sensitivity - No errors in this section - DO NOT EDIT

bar(S(:,1));
ylim([0 1]); %set y axis height to 1
switch np %switch statement to know how many parameters to list on x-axis
    case 3
        set(gca, 'xticklabel',{x(1).parameter, x(2).parameter, ...
            x(3).parameter});
    case 4
        set(gca, 'xticklabel',{x(1).parameter, x(2).parameter, ...
            x(3).parameter, x(4).parameter});
    case 5
        set(gca, 'xticklabel',{x(1).parameter, x(2).parameter, ...
            x(3).parameter, x(4).parameter, x(5).parameter});
    case 6
        set(gca, 'xticklabel',{x(1).parameter, x(2).parameter, ...
            x(3).parameter, x(4).parameter, x(5).parameter, ...
            x(6).parameter});
    case 7
        set(gca, 'xticklabel',{x(1).parameter, x(2).parameter, ...
            x(3).parameter, x(4).parameter, x(5).parameter, ...
            x(6).parameter, x(7).parameter});
    case 8
        set(gca, 'xticklabel',{x(1).parameter, x(2).parameter, ...
            x(3).parameter, x(4).parameter, x(5).parameter, ...
            x(6).parameter, x(7).parameter, x(8).parameter});
    case 9
        set(gca, 'xticklabel',{x(1).parameter, x(2).parameter, ...
            x(3).parameter, x(4).parameter, x(5).parameter, ...
            x(6).parameter, x(7).parameter, x(8).parameter, ...
            x(9).parameter});
    case 10
        set(gca, 'xticklabel',{x(1).parameter, x(2).parameter, ...
            x(3).parameter, x(4).parameter, x(5).parameter, ...
            x(6).parameter, x(7).parameter, x(8).parameter, ...
            x(9).parameter, x(10).paramter});
end

title('Sensitivity');
hold on
plot(xlim, [1/np 1/np], 'r'); %plot "sensitivity" line (1/# paramters)
