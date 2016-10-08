
# timmeh
####Timmeh's Timezones
*Here's the map, what's the plan?*

**The Map**

This geo-referenced image (`coordinates = pyproj.Proj('+proj=longlat +datum=WGS84 +no_defs')`) of the world's timezones.
![Colored_Timezones](https://cloud.githubusercontent.com/assets/4308824/19038948/a0618588-89c9-11e6-995f-11876032535d.png)
Currently, it has a 3.2 kilometer per pixel resolution at approx. 7% of the derived source file(s) size. 
![dictionary_lookup](https://cloud.githubusercontent.com/assets/4308824/18680742/54fb836c-7fa8-11e6-94a4-479c0fa5216a.png)

**The Plan**

This project will use a database, such as this, for simple, rapid offline look up of these timezones, with a small-er-footprint.

The image file/database may be further reduced as `timmeh` internal logic improves in edge cases and granularity.                

This entire process is functionally similar to when Debian or one of the Ubuntus is installed on a hard drive.  While setting the Timezone/locale a cursor is moved over an image and the user selects a point, 'in the ballpark'.  This timezone selection is made using the software package [Ubiquity](https://en.wikipedia.org/wiki/Ubiquity_(software)), except `timmeh` uses gps input...and the unified database.

Timezones are plotted from the shapefile found at [The World Timezone Shapefile Repository](http://efele.net/maps/tz/world/) 

The files have subsequently been modified with "quasi-maritime" timezones and unique colors are assigned indexing  the polygons.
 
For those timezones at sea, quick and dirty 15 degree polygons were unceremoniously addeded  to test the concept.  

Current logic looks to 8 points (0-315) to see if there is a 'land' timezone within 12 nautical miles, otherwise it becomes 'International' plus or minus the appropriate hour UTC.

Greater precision and methods are being sought while trying to keep a lid on the overall size.

When it's all over except the shouting, `timmeh`  might be able to ask if you want/need to change, or if confidence is high, make those changes automagically.

