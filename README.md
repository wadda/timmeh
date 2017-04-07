
# timmeh
####Timmeh's Timezones


**The Map**

This image is a projection of the world's timezones `coordinates = pyproj.Proj('+proj=longlat +datum=WGS84 +no_defs')`.
![Colored_Timezones](https://cloud.githubusercontent.com/assets/4308824/19038948/a0618588-89c9-11e6-995f-11876032535d.png)


**The Plan**

Currently, the map has a 7.6km/pixel (4.7mile) pixel resolution, at the Equator, with approx. 7% of the derived source file(s) size. 

This project uses this as a database for simple, rapid offline look up of timezones, with a small-er footprint.
![dictionary_lookup](https://cloud.githubusercontent.com/assets/4308824/18680742/54fb836c-7fa8-11e6-94a4-479c0fa5216a.png)


Timezones are plotted from the shapefile found at [The World Timezone Shapefile Repository](http://efele.net/maps/tz/world/) 

Those files have subsequently been modified with "quasi-maritime" timezones and unique colors are assigned indexing the polygons.
 
For those timezones at sea, quick and dirty 15 degree polygons were unceremoniously added. The 24 *new* polygons were added to the 418 pre-existing named polygons. Although `uninhabited` isn't an official timezone, the entire list of timezones (443) was assigned a colour in 35 point increments.

Current logic looks to 8 points (0-315) around the compass to see if there is a 'land' timezone within 12 nautical miles, otherwise it becomes 'International' plus or minus the appropriate hour UTC.

When it's all over except the shouting, `timmeh`  might be able to ask if you want/need to change your timezome/locale, or if confidence is high, make those changes automagically.

`timmeh` requires [gps3](https://github.com/wadda/gps3), a stylish Python accouterment to [gpsd](http://www.catb.org/gpsd/) and all your gps needs.

`sudo -H pip3 install gps3` will install **gps3** with a fast delivery from the [Cheese Shop](https://pypi.python.org/pypi/gps3)

[pyproj](https://pypi.python.org/pypi/pyproj/1.9.5.1) is also required.  It can also be found at the [Cheese Shop](https://pypi.python.org/pypi/pyproj/1.9.5.1).

Grab your machine and fire up your gps, make sure it all works.

Put `timmeh.py` and the image(s) you want to test in the same directory and `python3 timmeh.py` away on your favourite terminal, multiple times a day if you're adventurous like me. 

