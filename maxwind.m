%% Micrometeorology - Assignment 4 - Analysis Years

clear
close all
clc

%% Input

filename = 'sprog.tsv';

%% Load Data

data = load(filename);
data_direction = data(:,3:4);
data = data(:, 1:2);

%% Preprocess Data

% Expand Time Code
T = length(data);
datax = zeros(T, 6);
datax(:, 6) = data(:, 2);

for t = 1:T
    tcode = data(t, 1);
    datax(t, 1) = round(tcode/1e8);
    datax(t, 2) = round(mod(tcode, 1e8)/1e6);
    datax(t, 3) = round(mod(tcode, 1e6)/1e4);
    datax(t, 4) = round(mod(tcode, 1e4)/1e2);
    datax(t, 5) = mod(tcode, 1e2);
end

% Remove Error Values
clean = datax;
data_direction(clean(:, 6)==999, :) =   [];
data_direction(clean(:, 6)==99.99, :) = [];
clean(clean(:, 6)==999, :) =   [];
clean(clean(:, 6)==99.99, :) = [];


% find years
maxyear = max(clean(:, 1));
minyear = min(clean(:, 1));
years = minyear:maxyear;
n_years = length(years);
max_wind_list = zeros(1,n_years);
%%
sector = 30:30:360; 

idx = findsec(data_direction,sector(1));
sec1 = clean(idx,:);

idx = findsec(data_direction,sector(2));
sec2 = clean(idx,:);

idx = findsec(data_direction,sector(3));
sec3 = clean(idx,:);

idx = findsec(data_direction,sector(4));
sec4 = clean(idx,:);

idx = findsec(data_direction,sector(5));
sec5 = clean(idx,:);

idx = findsec(data_direction,sector(6));
sec6 = clean(idx,:);

idx = findsec(data_direction,sector(7));
sec7 = clean(idx,:);

idx = findsec(data_direction,sector(8));
sec8 = clean(idx,:);

idx = findsec(data_direction,sector(9));
sec9 = clean(idx,:);

idx = findsec(data_direction,sector(10));
sec10 = clean(idx,:);

idx = findsec(data_direction,sector(11));
sec11 = clean(idx,:);

idx = findsec(data_direction,sector(12));
sec12 = clean(idx,:);


%%
max_sec = zeros(length(years),12); %each column is a sector of the wind, row is the max wind speed for each year
max_sec(:,1) = maxwind_year(years,sec1);
max_sec(:,2) = maxwind_year(years,sec2);
max_sec(:,3) = maxwind_year(years,sec3);
max_sec(:,4) = maxwind_year(years,sec4);
max_sec(:,5) = maxwind_year(years,sec5);
max_sec(:,6) = maxwind_year(years,sec6);
max_sec(:,7) = maxwind_year(years,sec7);
max_sec(:,8) = maxwind_year(years,sec8);
max_sec(:,9) = maxwind_year(years,sec9);
max_sec(:,10) = maxwind_year(years,sec10);
max_sec(:,11) = maxwind_year(years,sec11);
max_sec(:,12) = maxwind_year(years,sec12);


%%
%find U 50 
[cdf_x,cdf_y] = ecdf(max_wind_list); 
plot(cdf_x,cdf_y)
hold on 
x = [0.98,0.98]; 
y = [22,31.7]; 
plot(x,y)

y = [31.7,31.7];
x = [0,0.98]; 
plot(x,y)

hold off 

%U_50 = 31.7 m/s 

%%
%fit max wind to Gumbel Distribution using Gumbel fitting method
%Assign each wind speed CDF probability by ordering it first
%then each wind speed has probability ascending from 0 - 1
%Find alpha and beta by fitting linear line of best fit
%between -log(-log(F)) and U

alpha_gumbelfit = zeros(12,1);
beta_gumbelfit = zeros(12,1);
U50_gumbelfit = zeros(12,1); 

for i = 1:12
    [alpha_gumbel,beta_gumbel,U50] = GumbelFit(max_sec(:,i)); 
    alpha_gumbelfit(i,1) = alpha_gumbel;
    beta_gumbelfit(i,1) = beta_gumbel;
    U50_gumbelfit(i,1) = U50; 
end


%%

%Probability weighted moment method
%Unbiased estimate of PWM can be obtained 
%from this alpha and beta could be derived 
%best available estimate, drawback: large number of data needed for
%accurate results 
alpha_PWMfit = zeros(12,1);
beta_PWMfit = zeros(12,1);
U50_PWMfit = zeros(12,1); 

for i = 1:12
    [alpha_PWM,beta_PWM,U50] = PWM_fit(max_sec(:,i)); 
    alpha_PWMfit(i,1) = alpha_PWM;
    beta_PWMfit(i,1) = beta_PWM;
    U50_PWMfit(i,1) = U50; 
end

%%

csvwrite('U_sec1.csv',sec1(:,6));
csvwrite('U_sec2.csv',sec2(:,6));
csvwrite('U_sec3.csv',sec3(:,6));
csvwrite('U_sec4.csv',sec4(:,6));
csvwrite('U_sec5.csv',sec5(:,6));
csvwrite('U_sec6.csv',sec6(:,6));
csvwrite('U_sec7.csv',sec7(:,6));
csvwrite('U_sec8.csv',sec8(:,6));
csvwrite('U_sec9.csv',sec9(:,6));
csvwrite('U_sec10.csv',sec10(:,6));
csvwrite('U_sec11.csv',sec11(:,6));
csvwrite('U_sec12.csv',sec12(:,6));


%%
function F = root2d(x,b0,b1,alpha)

F(1) = b0 - alpha*x(1) - x(2); 
F(2) = b1 - 0.5*((x(1)+log(2))*alpha + x(2));

end

%%
function idx = findsec(direction,sector)
N = length(direction);
direction = reshape(direction,1,[]);
idx = find(direction<=sector & direction>=(sector-30));
temp = find(idx==N);
temp2 = find(idx==2*N);

idx = mod(idx,N);
idx(temp) = N;
idx(temp2) = N;
end

%%
function max_wind_list = maxwind_year(years,sec)
i = 1;
max_wind_list = zeros(length(years),1);
for year = years
    max_wind = max(sec(find(sec(:,1)==year),6));
    max_wind_list(i,1) = max_wind; 
    i = i + 1;
end
end
%%
function [alpha_gumbel,beta_gumbel,U50] = GumbelFit(U)
U = sort(U); 
N = length(U) + 1; 
F = zeros(length(U),1);
for i = 1:length(U)
    F(i,1) = i/N
end 

Gumbel_y = -log(-log(F)); 
plot(U,Gumbel_y);
hold on
coefficients = polyfit(U, Gumbel_y, 1);

x = min(U):.1:max(U); 
a = coefficients(1);
b = coefficients(2);
y = a*x + b;
plot(x,y)
grid()
title('Gumbel Fit')
xlabel('X [m/s]')
ylabel('-log(-log(F(X))')
hold off
%find alpha and beta from linear line of best fit

alpha_gumbel = 1/a; 
beta_gumbel = -alpha_gumbel*b; 

%Find U50 

U50 = alpha_gumbel*log(50) + beta_gumbel;

end

%%

function [alpha_PWM,beta_PWM,U50_PWM] = PWM_fit(U)
U = sort(U); 
N = length(U);
gamma = 0.577; 
temp = 1:N; 
temp = temp - 1;
temp = temp';
b0 = mean(U);
b1 = (sum(temp.*U))/(N * (N-1)) ;
alpha_PWM = (2*b1 - b0)/(log(2));
beta_PWM = b0 - gamma*alpha_PWM; 

U50_PWM = alpha_PWM*log(50) + beta_PWM; 

end