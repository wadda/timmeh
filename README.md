
# timmeh


Geo-referenced image of the wolrds timezones as a database for rapid offline lookup

![Colored_Timezones](https://cloud.githubusercontent.com/assets/4308824/18680602/d4cc97e4-7fa7-11e6-96f2-f20bec42906b.png)

![dictionary_lookup](https://cloud.githubusercontent.com/assets/4308824/18680742/54fb836c-7fa8-11e6-94a4-479c0fa5216a.png)

A screen grab was taken of the shapefile found at [The World Timezone Shapefile Repository](http://efele.net/maps/tz/world/) and subsequently modified with "quasi-maritime" timezones and unique color index for the polygons.
 
Lat and lon are converted to pixel coordinates.  The color value of the image is referenced and then "*something/something*" if there is any timezone/locale change and to change it base on a degree of confidence

Similar to [Ubiquity](https://en.wikipedia.org/wiki/Ubiquity_(software)) handling of timezone setup in hard drive installations for the Debian/\*untu clan, except  using latitude/longitude from gps input rather than cursor selection.
 
 
For timezones at sea, quick and dirty 15 degree time polygons were hacked in to test the concept. if this works well enough greater precision can be used, as well as precision and projection of the image used for the database.
