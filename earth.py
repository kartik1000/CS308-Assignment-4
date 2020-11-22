import ee
import datetime

# ee.Authenticate()

# ee.Initialise()

present_date = (datetime.date.today())

# Landsat Data processing
# By default coordinates is an n-dimensional list of 2D lists
def earthLandsat(coordinates):
	# Load a raw Landsat
	# 'LANDSAT/LC08/C01/T1/LC08_044034_20140318'
	raw = ee.Image(coordinates);
	Map.centerObject(raw, 10);
	Map.addLayer(raw, {bands: ['B4', 'B3', 'B2'], min: 6000, max: 12000}, 'raw');

	# Convert raw data to radiance.
	radiance = ee.Algorithms.Landsat.calibratedRadiance(raw);
	Map.addLayer(radiance, {bands: ['B4', 'B3', 'B2'], max: 90}, 'radiance');

	# Convert  to top-of-atmosphere reflectance.
	toa = ee.Algorithms.Landsat.TOA(raw);
	Map.addLayer(toa, {bands: ['B4', 'B3', 'B2'], max: 0.2}, 'toa reflectance');

	# Load cloudy Landsat
	cloudy_scene = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140926');
	Map.centerObject(cloudy_scene);
	Map.addLayer(cloudy_scene, {bands: ['B4', 'B3', 'B2'], max: 0.4}, 'TOA', false);

	scored = ee.Algorithms.Landsat.simpleCloudScore(cloudy_scene); # Add cloud score band

	mask = scored.select(['cloud']).lte(20); # Create a mask from the cloud score, combine it with the image mask
	
	masked = cloudy_scene.updateMask(mask); # Apply mask
	Map.addLayer(masked, {bands: ['B4', 'B3', 'B2'], max: 0.4}, 'masked');

	# Load Landsat composite, set the SENSOR_ID property.
	mosaic = ee.Image(ee.ImageCollection('LANDSAT/LC8_L1T_8DAY_TOA').first()).set('SENSOR_ID', 'OLI_TIRS');

	scored_mosaic = ee.Algorithms.Landsat.simpleCloudScore(mosaic);
	Map.addLayer(scored_mosaic, {bands: ['B4', 'B3', 'B2'], max: 0.4}, 'TOA mosaic', false);

	#Display simple composites
	collection = ee.ImageCollection('LANDSAT/LT05/C01/T1').filterDate('2010-01-01', '2010-12-31');

	composite = ee.Algorithms.Landsat.simpleComposite(collection);
	
	customComposite = ee.Algorithms.Landsat.simpleComposite({collection: collection, percentile: 75, cloudScoreRange: 5});

	# Display and return the composites
	Map.setCenter(-122.3578, 37.7726, 10);
	Map.addLayer(composite, {bands: ['B4', 'B3', 'B2'], max: 128}, 'TOA composite');
	Map.addLayer(customComposite, {bands: ['B4', 'B3', 'B2'], max: 128}, 'Custom TOA composite');
	return Map