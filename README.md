
# timmeh


Geo-referenced image of the worlds timezones as a small-footprint database for rapid offline lookup

![Colored_Timezones](https://cloud.githubusercontent.com/assets/4308824/19038948/a0618588-89c9-11e6-995f-11876032535d.png)
![dictionary_lookup](https://cloud.githubusercontent.com/assets/4308824/18680742/54fb836c-7fa8-11e6-94a4-479c0fa5216a.png)

A screen grab was taken of the shapefile found at [The World Timezone Shapefile Repository](http://efele.net/maps/tz/world/) The files have subsequently been modified with "quasi-maritime" timezones and unique colors indexing  the polygons.
 
For those timezones at sea, a quick and dirty 15 degree polygons were hacked in to test the concept.  Greater precision and methods are being sought as well.
 
Lat and lon are converted to pixel coordinates.  The color value of that pixel is referenced and then "*something/something*" a work in process...if there is any timezone/locale change and to change it base on a degree of confidence

Similar to [Ubiquity](https://en.wikipedia.org/wiki/Ubiquity_(software)) handling of timezone setup in hard drive installations for the Debian/\*untu clan, except  using latitude/longitude from gps input rather than cursor selection.
 
