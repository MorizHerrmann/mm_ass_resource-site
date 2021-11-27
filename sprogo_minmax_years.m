// %% Micrometerology - Assignment 4
// % Weibull parameters of least and most windy years
// % contains elements of sprogo_1D.m and sprogo_years of 1st assigment
//
// clear; close all; clc;
//
// %% Load Data
//
// data = load('sprog.tsv');
//
// %% Preprocess Data
//
// % Expand Time Code
// T = length(data);
// datax = zeros(T, 7);
// datax(:, 6) = data(:, 2);
//
// for t = 1:T
//     tcode = data(t, 1);
//     datax(t, 1) = round(tcode/1e8);             % year
//     datax(t, 2) = round(mod(tcode, 1e8)/1e6);   % month
//     datax(t, 3) = round(mod(tcode, 1e6)/1e4);   % day
//     datax(t, 4) = round(mod(tcode, 1e4)/1e2);   % hour
//     datax(t, 5) = mod(tcode, 1e2);              % minute
// end
//
// dir1 = data(:, 3);
// dir2 = data(:, 4);
//
// dir = zeros(T, 1);
//
// for t = 1:T
//     if dir1(t) == 999 && dir2(t) == 999
//         dir(t) = 999;
//     elseif dir1(t) == 999 && dir2(t) ~= 999
//         dir(t) = dir2(t);
//     elseif dir1(t) ~= 999 && dir2(t) == 999
//         dir(t) = dir1(t);
//     else
//         dir(t) = dir1(t);
//     end
// end
//
// datax(:, 7) = dir;
//
// % Remove Error Values
// clean = datax;
// clean(clean(:, 6)==999, :) =   [];
// clean(clean(:, 6)==99.99, :) = [];
// clean(clean(:, 7)==999, :) = [];

%% Find years

maxyear = max(clean(:, 1));
minyear = min(clean(:, 1));
years = minyear:maxyear;
n_years = length(years);

% calculate statistics
means = zeros(n_years, 1);
stds =  zeros(n_years, 1);

for year = 1:n_years
    data_of_year = clean(clean(:, 1)==years(year), 6);
    means(year) = mean(data_of_year);
    stds(year) = std(data_of_year);
end

min_u = min(means);
max_u = max(means);

min_year = years(means==min_u);
max_year = years(means==max_u);

fprintf('Minimal mean wind speed ' + string(round(min_u, 2)) + ' in ' + string(min_year));
fprintf('\nMinimal mean wind speed ' + string(round(max_u, 2)) + ' in ' + string(max_year));

% %% Directions - Minimum
% % Find the Weibull Distribution of the wind speed for all sections in the
% % year with the least wind
% 
% data_min = clean(clean(:, 1)==min_year, :);
% T_min = length(data_min);
% 
% A = 12;
% sect_angles = 0:30:360;
% dir_sections_min = zeros(T_min, A+1);
% 
% for t = 1:T_min    
%     for sect_angle = 1:A+1
%         if sect_angles(sect_angle) - 15 < data_min(t, 7) && data_min(t, 7) <= sect_angles(sect_angle) + 15
%             dir_sections_min(t, sect_angle) = data_min(t, 6);
%         end
%     end
% end
% 
% dir_sections_clean_min = cell(A+1, 1);
% for sect_angle = 1:A+1
%      dir_sections_clean_min{sect_angle} = dir_sections_min(:, sect_angle);
%      dir_sections_clean_min{sect_angle}(dir_sections_clean_min{sect_angle}==999) = [];
%      dir_sections_clean_min{sect_angle}(dir_sections_clean_min{sect_angle}==99.99) = [];
%      dir_sections_clean_min{sect_angle}(dir_sections_clean_min{sect_angle}==0) = [];
% end
% dir_sections_clean_min{1} = [dir_sections_clean_min{1}; dir_sections_clean_min{A+1}];
% dir_sections_clean_min(A+1) = [];
% len_sections_min = length(dir_sections_clean_min);
% 
% n_clean_min = 0;
% for sect = 1:A
%     n_clean_min = n_clean_min + length(dir_sections_clean_min{sect});
% end
% 
% f_sect_min = zeros(A, 1);
% for sect = 1:A
%     f_sect_min(sect) = length(dir_sections_clean_min{sect}) / n_clean_min;
% end
% 
% mu_sect_min = zeros(A, 1);
% sol_sect_min = zeros(A, 2);
% 
% for sect = 1:A    
%     % prerequesites
%     u_min = dir_sections_clean_min{sect};
%     mu_sect_min(sect) = mean(u_min);
%     
%     % find parameters
%     [cdf_y, cdf_x] = ecdf(u_min);
%     fprintf('Minimum' + string(sect));
%     sol_sect_min(sect, :) = solution_b(u_min, cdf_x, cdf_y);     
% end

%% Directions - Maximum
% % Find the Weibull Distribution of the wind speed for all sections in the
% % year with the most wind
% 
% options.MaxIterations = 5000;
% 
% data_max = clean(clean(:, 1)==max_year, :);
% T_max = length(data_max);
% 
% A = 12;
% sect_angles = 0:30:360;
% dir_sections_max = zeros(T_max, A+1);
% 
% for t = 1:T_max    
%     for sect_angle = 1:A+1
%         if sect_angles(sect_angle) - 15 < data_max(t, 7) && data_max(t, 7) <= sect_angles(sect_angle) + 15
%             dir_sections_max(t, sect_angle) = data_max(t, 6);
%         end
%     end
% end
% 
% dir_sections_clean_max = cell(A+1, 1);
% for sect_angle = 1:A+1
%      dir_sections_clean_max{sect_angle} = dir_sections_max(:, sect_angle);
%      dir_sections_clean_max{sect_angle}(dir_sections_clean_max{sect_angle}==999) = [];
%      dir_sections_clean_max{sect_angle}(dir_sections_clean_max{sect_angle}==99.99) = [];
%      dir_sections_clean_max{sect_angle}(dir_sections_clean_max{sect_angle}==0) = [];
% end
% dir_sections_clean_max{1} = [dir_sections_clean_max{1}; dir_sections_clean_max{A+1}];
% dir_sections_clean_max(A+1) = [];
% len_sections_max = length(dir_sections_clean_max);
% 
% n_clean_max = 0;
% for sect = 1:A
%     n_clean_max = n_clean_max + length(dir_sections_clean_max{sect});
% end
% 
% f_sect_max = zeros(A, 1);
% for sect = 1:A
%     f_sect_max(sect) = length(dir_sections_clean_max{sect}) / n_clean_max;
% end
% 
% mu_sect_max = zeros(A, 1);
% sol_sect_max = zeros(A, 2);
% 
% for sect = 1:A    
%     % prerequesites
%     u_max = dir_sections_clean_max{sect};
%     mu_sect_max(sect) = mean(u_max);
%     
% %     % find parameters
%     [cdf_y, cdf_x] = ecdf(u_max);
%     fprintf('Maximum' + string(sect));
%     sol_sect_max(sect, :) = solution_b(u_max, cdf_x, cdf_y);     
% end

%% Statistics over years

fig = figure(1);
fig.Position = [0 0 800 400];
plot(years, means);
yline(mean(means), 'r--');
grid()
xlabel('year')
ylabel('mean wind speed')

figure(2)
plot(years, stds);
grid()
xlabel('year')
ylabel('standard deviation of wind speed')

std(means)
std(clean(:, 6))

