
# timmeh


Geo-referenced image of the world's timezones as a small-footprint database for rapid offline lookup

When people install Debian or one of the Ubuntus on a hard drive timezone selection is made moving a cursor over an image and selecting a point,

![Colored_Timezones](https://cloud.githubusercontent.com/assets/4308824/19038948/a0618588-89c9-11e6-995f-11876032535d.png)
![dictionary_lookup](https://cloud.githubusercontent.com/assets/4308824/18680742/54fb836c-7fa8-11e6-94a4-479c0fa5216a.png)

Similar to [Ubiquity](https://en.wikipedia.org/wiki/Ubiquity_(software)) handling of timezone setup in hard drive installations, except  using a gps for input rather than a cursor.

Timezones are plotted from the shapefile found at [The World Timezone Shapefile Repository](http://efele.net/maps/tz/world/) 

The files have subsequently been modified with "quasi-maritime" timezones and unique colors are assigned indexing  the polygons.
 
For those timezones at sea, quick and dirty 15 degree polygons were unceremoniously addeded  to test the concept.  Greater precision and methods are being sought while trying to keep a lid on the overall size.

Lat and lon are converted to pixel coordinates.  The color value of that pixel is referenced and then "*something/something*" a work in process...if there is any timezone/locale change and to change it base on a degree of confidence...and there you have it.
