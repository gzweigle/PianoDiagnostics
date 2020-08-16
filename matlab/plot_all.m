% Gregary C. Zweigle, 2020
%
% Loop through all files in the directory_name/ location
% and display the L/R data and the L/R FFT.
function plot_all(directory_name)

sample_rate = 44100;

% Get the files in the data folder.
full_path_directory = sprintf("../%s", directory_name);
files = dir(full_path_directory);
% Subtract 2 because first two files are . and ..
num_data = (length(files)-2)/2;

% Loop over the left/right channel pairs.
for k = [1:num_data],

  % Add 2 because first two files are . and ..
  left = sprintf("../test/%s",files(k+2).name);
  right = sprintf("../test/%s",files(k+2+num_data).name);

  tmp = load(left);
  m = min(find(abs(tmp) > 10));  % start when signal starts
  x = tmp(m:length(tmp));
  x = x / max(abs(x));

  max_left = max(abs(tmp));

  tmp = load(right);
  m = min(find(abs(tmp) > 10));  % start when signal starts
  y = tmp(m:length(tmp));
  y = y / max(abs(y));

  % Plot the time-domain results.
  subplot(2,1,1);
  plot([1:length(x)]/sample_rate,x,[1:length(y)]/sample_rate,y);
  grid;

  % Plot the frequency domain results.
  subplot(2,1,2);
  N=32768;
  L = min(length(x), 6000);
  frange = [0:1/N:1-1/N]*sample_rate;
  x_fft = 20*log10(abs(fft(x(1:L),N)));
  y_fft = 20*log10(abs(fft(y(1:L),N)));
  max_ind = max(find(frange <= 10000));
  plot(frange(1:max_ind),x_fft(1:max_ind),...
       frange(1:max_ind),y_fft(1:max_ind));
  grid;

  wait_string = sprintf("Plotted file %d, max value=%f\n",k,max_left);
  printf(wait_string);
  pause(0.5);

end;
