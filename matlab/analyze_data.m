% Gregary C. Zweigle, 2020

% This is an initial version of Matlab to match and plot two signals.

clear;

% The chunk size is the most these signals could not overlap.
chunk = 1024;

% How many samples to correlate over.
corr_length = 2*chunk;

% Load the data.
load ..\data\note1.dat;
load ..\data\note2.dat;
datA = X___data_note1;
datB = X___data_note2;

% Normalize.
datA = datA / max(abs(datA));
datB = datB / max(abs(datB));

% Compute correlation for all possible data shifts.
start_ind = chunk; % Get past any transients.
for k = 1:chunk,
  correlation(k) = sum(datA(start_ind : start_ind + corr_length) .*
                       datB(start_ind + k : start_ind + corr_length + k));
end;

% Find the best overlap.
[max_val, max_ind] = max(correlation);
max_ind = max_ind + 1;

% Plot the results.
plot([1:length(datA)],datA,[1:length(datB)-max_ind + 1],datB(max_ind:end));
grid;
