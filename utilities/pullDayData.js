/**
 * Author: Wilbur Li
 *
 * Google Earth Engine Script for exporting CSV of (lon,lat,visibility) for fire events in our region for any specified day. 
**/


// ----- from FIRMS sample snippet -----

var dataset = ee.ImageCollection('FIRMS').filter(
    ee.Filter.date('2018-08-01', '2018-08-2'));

var fires = dataset.select('T21').first().toInt();
print('fires', fires)

var firesVis = {
  min: 325.0,
  max: 400.0,
  palette: ['red', 'orange', 'yellow'],
};
Map.setCenter(-119.086, 47.295, 6);
Map.addLayer(fires, firesVis, 'Fires');

// ----- from Nick -----

var mask = dataset.select('T21').mosaic().mask()
Map.addLayer(mask)

var coords = mask.multiply(ee.Image.pixelLonLat())
print('coords', coords)
Map.addLayer(coords)

var fireVector = fires.reduceToVectors({geometry: geometry})
var i = 0;
var centroidFire = fireVector.map(function(f) { 
  return f.centroid(1) } );
print('fire vector', fireVector)
print('centroid', centroidFire)
Map.addLayer(centroidFire.style({pointSize: 10}),{},'Centroids')
// image.reduceToVectors().map(function(f) { return f.centroid() } )
// reduceRegions

print(dataset)

// ----- experimentation -----

var image = coords

var region = ee.Geometry.Rectangle(-122.2806, 37.1209, -122.0554, 37.2413);

var means = image.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: region,
  scale: 30
});

print(dataset)

var feature = ee.Feature(null, means);
print('feature', feature)

var featureCollection = ee.FeatureCollection([feature]);


// Export the FeatureCollection to a KML file.
Export.table.toDrive({
  collection: centroidFire,
  description:'vectorsToDriveExample',
  fileFormat: 'CSV'
});
