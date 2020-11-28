%% Program for Importing Data for Topographic Correction of Landsat 8 Images
% Program Written by Sharad Kumar Gupta

function importdata()
%% Cleaning Up and Setting Format
clear;
close;
clc;
format short
format compact

%% Input Data
metafilename = uigetfile({'*.txt;*.xml;','Open Metadata'});
metafile = fopen(metafilename,'r');
textdata = textscan(metafile,'%s','Delimiter','','endofline','');
textdata = textdata{1}{1};
metafile  = fclose(metafile);

% Parsing Metadata for Azimuth and Sun Elevation
Azimuth = regexp(textdata,'SUN_AZIMUTH[\s\.=]+(\d+.\d+)','tokens');
Azimuth = str2double(Azimuth{1});
Sun_Elev = regexp(textdata,'SUN_ELEVATION[\s\.=]+(\d+.\d+)','tokens');
Sun_Elev = str2double(Sun_Elev{1});
Zenith = (90 - Sun_Elev);

% Importing Satellite Image for Correction
imgfile = uigetfile({'*.jpg;*.tif;*.png;','Select Image'});
[image,r] = geotiffread(imgfile);
worldfile = getworldfilename(imgfile);
gtinfo = geotiffinfo(imgfile);
[rows,cols,bands] = size(image);
utm_zone = gtinfo.Zone;
image = double(image);
% image (image <= 0) = nan;

% Importing DEM
demfile = uigetfile({'*.jpg;*.tif;*.png;','Select DEM'});
[dem,~] = geotiffread(demfile);
dem = double(dem);
dem(dem>8850) = nan;
dem(dem<0) = nan;

% Importing Aspect
aspfile = uigetfile({'*.jpg;*.tif;*.png;','Select Aspect'});
[asp,~] = geotiffread(aspfile);
asp = double(asp);
asp (asp < -1) = nan;

% Importing Slope
slpfile = uigetfile({'*.jpg;*.tif;*.png;','Select Slope'});
[slp,~] = geotiffread(slpfile);
slp = double(slp);
slp (slp < 0) = nan;

clearvars metafilename metafile demfile aspfile slpfile textdata imgfile worldfile
save('data_topocorrection')
fprintf('Data Imported. \n');
clearvars
end