%% Program for Topographic Correction for Landsat 8
% Program written by Sharad Kumar Gupta
%% Cleaning Up and Setting Format
clear;
close;
clc
format short
format compact

%% Input Data
load('data_topocorrection.mat')
fprintf('Process Starting...\n\n');
tic;

%% Illumination Condition (IL)
IL = (cosd(Zenith).*cosd(slp))+((sind(Zenith).*sind(slp)).*cosd(Azimuth - asp));
IL_min = min(min(IL));
IL_max = max(max(IL));
IL(IL<0) = nan;

%% NDVI
ndvi = (image(:,:,4) - image(:,:,3))./(image(:,:,4) + image(:,:,3));

%% Flat Region Calculation
mult = ndvi .* slp;
mult(mult>=1)=1;
mult(mult<1)=nan;

%% Image with No flat Region (Excluding flat region from processing)
image = image .* mult;
IL = IL .* mult;

%% Relation b/w Original Image and IL for Parameter 'C'
x = reshape(IL,[],1);
C = zeros(bands,1);
m = zeros(bands,1);
b = zeros(bands,1);
x = x(ndvi>0.40);

for i = 1:bands
    y = image(:,:,i);
    y = reshape(y,[],1);
    y = y(ndvi>0.40);
    ind = x(~isnan(x)); ind1 = y(~isnan(x));
    fits = polyfit(ind,ind1,1);
    m(i) = fits(1); b(i) = fits(2);
    C(i) = b(i)/m(i);
end

%% Methods for Topographic Correction
fprintf('The below mentioned methods are being implemented \n');
used_methods = {'Cosine Correction','C-HuangWei Correction','VECA Correction','C Correction','SCS + C Correction'};
noMethods = length(used_methods);
corrected = zeros(rows,cols,bands,noMethods);
fcc_corr_comb = zeros(rows,cols,3,noMethods);
uncorr_stats = zeros(bands,3);
corr_stats = zeros(bands,3,noMethods);
for i = 1:noMethods
    method = strcat(num2str(i),'.',' ',used_methods{i});
    fprintf('\n');
    fprintf(method);
end
fprintf('\n');

%% Statistics before Correction
% Mean, Standard Deviation, Coefficient of Variation
for i = 1:bands
    mean_a =  nanmean(reshape(image(:,:,i),[],1));
    std_a =  nanstd(reshape(image(:,:,i),[],1));
    cv_a = (std_a/mean_a)*100;
    uncorr_stats(i,:) = [mean_a std_a cv_a];
end

%% Implementation of Methods
% ****************************

%% Cosine Correction (Teillet et al. 1982)
% Formula: p_h = p_t*(cos(theta_z)/IL)
for i = 1:bands
    corrected(:,:,i,1) = (cosd(Zenith)./IL).*image(:,:,i);
end
fprintf('\nCosine Correction implemented \n');

%% C-HuangWei Correction (HuangWei et al. 2005)
% Formula : p_h=(p-p_min)*((cos(theta_z)-IL_min)/(IL-IL_min))+p_min
for i = 1:bands
    corrected(:,:,i,2) = (((cosd(Zenith) - IL_min)./(IL - IL_min)).*(image(:,:,i) - min(min(image(:,:,i))))) + min(min(image(:,:,i)));
end
fprintf('\nC-Huang Wei Correction implemented \n');

%% VECA Correction (Gao et al. 2009)
for i = 1:bands
    mean_a =  nanmean(reshape(image(:,:,i),[],1));
    corrected(:,:,i,3) = (mean_a./(m(i).*IL + b(i))).*image(:,:,i);
end
fprintf('\nVECA Correction implemented \n');

%% C Correction (Teillet et al. 1982)
% Formula C = b/m, p_h = p_t*((cos(theta_z)+C)/(IL+C))
for i = 1:bands
    corrected(:,:,i,4) = ((cosd(Zenith) + C(i))./(IL + C(i))).*image(:,:,i);
end
fprintf('\nC Correction implemented \n');

%% SCS + C Correction (Soenen et al. 2005)
% Formula C = b/m, p_h = p_t*((cos(theta_z)*cos(slope)+C)/(IL+C))
for i = 1:bands
    corrected(:,:,i,5) = ((cosd(Zenith).*cosd(slp) + C(i))./(IL + C(i))).*image(:,:,i);
end
fprintf('\nSCS+C Correction implemented \n');
        
%% False Color Composite of Original Image
org = image(:,:,4:-1:2);

%% False Color Composite of Corrected Image
for i = 1:noMethods
    fcc_corr_comb(:,:,:,i) = corrected(:,:,4:-1:2,i);
end

%% Statistics after Correction
% Mean, Standard Deviation, Coefficient of Variation
cv_diff = zeros(bands,noMethods);
for i = 1:noMethods
    for j = 1:bands
        mean_a =  nanmean(reshape(corrected(:,:,j,i),[],1));
        std_a =  nanstd(reshape(corrected(:,:,j,i),[],1));
        cv_a = (std_a/mean_a)*100;
        corr_stats(j,:,i) = [mean_a std_a cv_a];
        cv_diff(j,i) = uncorr_stats(j,3) - corr_stats(j,3,i);
    end
end

%% Plot Between IL and Reflectance for Band 4 After All Corrections
% For Original Image Band 4
x = reshape(IL,[],1);
y = image(:,:,4);
y = reshape(y,[],1);
x = x(ndvi>0.40); y = y(ndvi>0.40);
ind = x(~isnan(x));ind1 = y(~isnan(x));
fits = polyfit(ind, ind1, 1);
mOrg = fits(1); bOrg = fits(2);
ynew = mOrg * ind + bOrg;
Equation_Parameters = [mOrg bOrg];
gcf = figure('units','normalized','outerposition',[0 0 1 1]);
subplot(2,4,1), scatter(ind,ind1,'r.') 
hold on, plot(ind,ynew,'b-'),title('Original Image')
eq = sprintf('y = %f * x + %f',mOrg,bOrg);
legend({eq},'FontSize',8);
xlim([0 1]); ylim([0 1]);
xlabel('Band 4'); ylabel('IL');
box on
corrected (corrected < 0) = nan;
mCorr = zeros(noMethods,1);
bCorr = zeros(noMethods,1);

% For Corrected Image Band 4
for i = 1:noMethods
    y = corrected(:,:,4,i);
    y = reshape(y,[],1);
    y = y(ndvi>0.40);
    ind1 = y(~isnan(x));
    fits = polyfit(ind, ind1, 1);
    mCorr(i) = fits(1); bCorr(i) = fits(2);
    ynew = mCorr(i) * ind + bCorr(i);
    subplot(2,4,i+1), scatter(ind,ind1,'r.')
    hold on
    plot(ind,ynew,'b-'),title(used_methods{i})
    eq = sprintf('y = %f * x + %f',mCorr(i),bCorr(i));
    legend({eq},'FontSize',8);
    xlim([0 1]); ylim([0 1]);
    xlabel('Band 4'); ylabel('IL');
    box on
end
% print(gcf,'Plot','-djpeg','-r600');
fprintf('\n');
Equation_Parameters = [Equation_Parameters; mCorr bCorr];
xlswrite('Slope_Intercept.xlsx',Equation_Parameters);

%% Saving All the Results in Seperate Folder
fprintf('\nSaving Results \n');
old_dir = pwd();
new_dir = fullfile(pwd(),'Corrected_Images');
if ~exist(new_dir, 'dir')
    mkdir(new_dir)
end
cd(new_dir);
for i = 1:noMethods
    filename = strcat(used_methods{i}, '.tif');
    worldfilename = strcat(used_methods{i}, '.tfw');
    coordRefCode = 32600 + utm_zone;
    geotiffwrite(filename,corrected(:,:,:,i),r,'CoordRefSysCode',coordRefCode);
    worldfilewrite(r,worldfilename);
end
geotiffwrite('IL.tif',IL,r,'CoordRefSysCode',coordRefCode);
worldfilewrite(r,'IL.tfw')
coordRefCode = 32600 + utm_zone;
geotiffwrite('Image_NoFlat_Region.tif',image,r,'CoordRefSysCode',coordRefCode);
worldfilewrite(r,'Image_NoFlat_Region.tfw')
cd(old_dir)
fprintf('\nProcess Completed.\n');
Execution_Time = toc
clearvars -except dem asp slp image corrected Equation_Parameters corr_stats uncorr_stats fcc_corr_comb org K C r IL cv_diff