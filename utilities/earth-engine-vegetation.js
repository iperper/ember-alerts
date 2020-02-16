/**
 * Copy of Earth Engine code for getting vegetation data from satelites
 * Can be found here: https://code.earthengine.google.com/c2aa70947619906448ff53918daab689
 *
 * Currently not fully set up, but backbone of datasets and how to get data for
 * a list of coordinates is at the bottom of file.
 *
 * Author: Isaac Perper
**/


var vegetation_dataset = ee.ImageCollection('MODIS/006/MOD13A2')
                  .filter(ee.Filter.date('2018-01-01', '2018-05-01'));

var evi = vegetation_dataset.select('EVI');
var ndvi = vegetation_dataset.select('NDVI');

var landtype_dataset = ee.ImageCollection('MODIS/006/MCD12Q1');
var igbpLandCover = landtype_dataset.select('LC_Type1');

var eviVis = {
  min: -2000.0,
  max: 10000.0,
  palette: [
    'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
    '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
    '012E01', '011D01', '011301'
  ],
};

var igbpLandCoverVis = {
  min: 1.0,
  max: 17.0,
  palette: [
    '05450a', '086a10', '54a708', '78d203', '009900', 'c6b044', 'dcd159',
    'dade48', 'fbff13', 'b6ff05', '27ff87', 'c24f44', 'a5a5a5', 'ff6d4c',
    '69fff8', 'f9ffa4', '1c0dff'
  ],
};

var lon = -120.3
var lat = 38
Map.setCenter(lon, lat, 8);
Map.addLayer(evi, eviVis, 'EVI');
Map.addLayer(ndvi, eviVis, 'NDVI');
Map.addLayer(igbpLandCover, igbpLandCoverVis, 'IGBP Land Cover');



function getValfromLonLat(image, loc) {
  var geometry = ee.Geometry.Point(loc)
  var out = image.reduceRegion(ee.Reducer.first(), geometry)
  return out
}

var test_locs = ee.List([[-120.4675, 38.4768], [-120.4676, 38.4768], [-119.6326, 38.2183], [-123.4998, 38.8713]]);

var out = getValfromLonLat(evi.first(), [lon, lat]);
var out2 = getValfromLonLat(ndvi.first(), [lon, lat]);

var results = test_locs.map(function map(loc) {return getValfromLonLat(evi.first(), loc).get('EVI')});
print(results)

