#! /usr/bin/env python3
# coding=utf-8
"""Reads latitude/longitude from gpsd client and looks up indexed timezones from color referenced image"""
import time
from math import pi

from PIL import Image
from gps3 import gps3
from pyproj import Geod, Proj

__author__ = 'Moe'
__copyright__ = 'Copyright 2016  Moe'
__license__ = 'MIT'
__version__ = '0.0.4'

geoid = Geod(ellps='WGS84')  # For 8 point 'at sea' distance calculation
coordinates = Proj('+proj=longlat +datum=WGS84 +no_defs')
im = Image.open('tz_5265x2633.png')
size_x, size_y = im.size  # Overall maximums
color_spread = 35  # Colors in the timezone dictionaries at least 35 points divergent from the next color
pix = im.load()

CONVERSION = {'imperial': 1609.344, 'metric': 1000.0, 'nautical': 1852.0}
DISTANCE = CONVERSION['nautical'] * 12  # International Waters


def get_latlon():
    """Rings up a gpsd to get current lat/lon"""
    gpsd_socket = gps3.GPSDSocket()
    gpsd_socket.connect()
    gpsd_socket.watch()
    data_stream = gps3.DataStream()
    try:
        for new_data in gpsd_socket:
            if new_data:
                data_stream.unpack(new_data)
                if data_stream.TPV['lat'] != 'n/a':
                    latitude = data_stream.TPV['lat']
                    longitude = data_stream.TPV['lon']

                    gpsd_socket.close()  # close socket after successful
                    return latitude, longitude
            else:
                time.sleep(.1)  # 1/10th second sleep for requests after lookup yields no result

    except KeyboardInterrupt:
        gpsd_socket.close()
        print('\nTerminated by user\nGood Bye.\n')


def lookup(lat, lon):
    """looks up rgb values on image as key to timezones
    Arguments:
        lat (float), Latitude North (positive), South (negative)
        lon (float), Longitude East (positive), West (negative)
    Returns:
        px (int), pixel column
        py (int), pixel row
        color_value (tuple of ints) RGB color values
        tz (str), 'proper named' timezone
    """
    try:
        px, py, rgb = get_color(lat, lon)
        if rgb in bigdic.keys():
            tz = bigdic[rgb]
            return px, py, rgb, tz

        if rgb in seadic.keys():  # If pixel is ocean,
            tz = seadic[rgb]
            for bearing in range(0, 315, 45):  # look at 8 points around the original location.
                new_lon, new_lat = where_go(lat, lon, bearing, DISTANCE)  # return a point
                px, py, rgb = get_color(new_lat, new_lon)  # Get pixel values
                if rgb not in seadic.keys():  # and compare.
                    tz = bigdic[rgb]  # If pegs land it will stay on last land
            return px, py, rgb, tz  # You are in the territorial waters of Deep Burgundy.

    except KeyError:
        px, py, rgb = get_color(lat, lon)  # The pixel RGB may be off for edge reasons
        rgb = tuple(round(value / color_spread) * color_spread for value in rgb)
        if rgb in bigdic.keys():  # if is
            tz = bigdic[rgb]  # use that.
        if rgb in seadic.keys():
            tz = seadic[rgb]
        else:
            # print("Lasciate ogne speranza, voi ch'intrate")
            tz = "Gates'o'Hell/Houston"
        return px, py, rgb, tz


def get_color(lat, lon):
    """Converts Latitude/Longitude to return pixel x/y coordinates and color value of the pixel.
    Arguments:
        lat (float), Latitude North (positive), South (negative)
        lon (float), Longitude East (positive), West (negative)
    Returns:
        px (int), x pixel column in image
        py (int), y pixel row in image
        rgb (tuple of ints), RGB color tuple
    """
    x, y = coordinates(lon, lat)  # x = -pi --> pi; y = 1/2pi --> -1/2pi
    px = int((x + pi) * ((size_x / 2) / pi))
    py = int(size_y - (y + (pi / 2)) * (size_y / pi))
    rgb = pix[px, py]
    return px, py, rgb


def where_go(lat, lon, azimuth, distance):
    """Calculates *new* lat/lon pair from another pair, given bearing and distance
    Arguments:
        lon (float): longitude of reference point
        lat (float): latitude of reference point
        azimuth (float): bearing in degrees to solution
        distance (float): distance in meters to solution
    Returns:
        lon (float): longitude of solution
        lat (float: latitude of solution
     #  __bearing_fro (float): bearing from the solution point to the reference point
    """
    new_lon, new_lat, __bearing_fro = geoid.fwd(lon, lat, azimuth, distance)  # How easy is that?

    return new_lon, new_lat


seadic = {(0,   0,  35): 'Etc/GMT-12',
          (0,   0,  70): 'Etc/GMT-11',
          (0,   0, 105): 'Etc/GMT-10',
          (0,   0, 140): 'Etc/GMT-9',
          (0,   0, 175): 'Etc/GMT-8',
          (0,   0, 210): 'Etc/GMT-7',
          (0,   0, 245): 'Etc/GMT-6',
          (0,  35,   0): 'Etc/GMT-5',
          (0,  35,  35): 'Etc/GMT-4',
          (0,  35,  70): 'Etc/GMT-3',
          (0,  35, 105): 'Etc/GMT-2',
          (0,  35, 140): 'Etc/GMT-1',
          (0,  35, 175): 'Etc/GMT0',
          (0,  35, 210): 'Etc/GMT+1',
          (0,  35, 245): 'Etc/GMT+2',
          (0,  70,   0): 'Etc/GMT+3',
          (0,  70,  35): 'Etc/GMT+4',
          (0,  70,  70): 'Etc/GMT+5',
          (0,  70, 105): 'Etc/GMT+6',
          (0,  70, 140): 'Etc/GMT+7',
          (0,  70, 175): 'Etc/GMT+8',
          (0,  70, 210): 'Etc/GMT+9',
          (0,  70, 245): 'Etc/GMT+10',
          (0, 105,   0): 'Etc/GMT+11',
          (0, 105,  35): 'Etc/GMT+12'}

bigdic = {(175,   0, 105): 'Africa/Abidjan',
          ( 35, 105, 105): 'Africa/Accra',
          (175, 210, 210): 'Africa/Addis_Ababa',
          (210, 105,   0): 'Africa/Algiers',
          (105,   0,   0): 'Africa/Asmara',
          ( 70, 210, 245): 'Africa/Bamako',
          (105,  35, 210): 'Africa/Bangui',
          (140,  70,  35): 'Africa/Banjul',
          (  0, 210, 140): 'Africa/Bissau',
          (105, 140, 175): 'Africa/Blantyre',
          ( 70, 140, 210): 'Africa/Brazzaville',
          ( 35, 175, 245): 'Africa/Bujumbura',
          ( 70,  35, 140): 'Africa/Cairo',
          (175, 105,  70): 'Africa/Casablanca',
          (175, 105,   0): 'Africa/Ceuta',
          ( 70, 245, 175): 'Africa/Conakry',
          (105, 245,   0): 'Africa/Dakar',
          (  0, 140, 175): 'Africa/Dar_es_Salaam',
          (175,  70, 175): 'Africa/Djibouti',
          (175, 105, 210): 'Africa/Douala',
          (  0, 175, 210): 'Africa/El_Aaiun',
          ( 35, 105,  35): 'Africa/Freetown',
          (  0, 140,  70): 'Africa/Gaborone',
          (140, 175, 140): 'Africa/Harare',
          ( 70, 175, 140): 'Africa/Johannesburg',
          (210, 105, 210): 'Africa/Juba',
          ( 70, 245,   0): 'Africa/Kampala',
          (175, 105, 175): 'Africa/Khartoum',
          (140, 210,  35): 'Africa/Kigali',
          (175, 140,  35): 'Africa/Kinshasa',
          ( 35, 140,  70): 'Africa/Lagos',
          ( 70, 140, 245): 'Africa/Libreville',
          (140, 175, 245): 'Africa/Lome',
          (175,   0,   0): 'Africa/Luanda',
          (175, 245, 140): 'Africa/Lubumbashi',
          (140, 140,  35): 'Africa/Lusaka',
          (105, 105, 210): 'Africa/Malabo',
          (210,  35,  70): 'Africa/Maputo',
          (175, 175, 210): 'Africa/Maseru',
          ( 70,  35, 105): 'Africa/Mbabane',
          (105, 210, 175): 'Africa/Mogadishu',
          (210,   0,   0): 'Africa/Monrovia',
          (210, 210, 210): 'Africa/Nairobi',
          (105, 140,   0): 'Africa/Ndjamena',
          (140, 105,  35): 'Africa/Niamey',
          (  0, 210,   0): 'Africa/Nouakchott',
          (140, 105, 105): 'Africa/Ouagadougou',
          ( 35, 210, 105): 'Africa/Porto-Novo',
          ( 70, 175,   0): 'Africa/Sao_Tome',
          (175, 140, 175): 'Africa/Tripoli',
          (175,  35, 175): 'Africa/Tunis',
          (105,  70, 140): 'Africa/Windhoek',
          ( 70, 210,  70): 'America/Adak',
          (210,  70, 105): 'America/Anchorage',
          ( 70, 210, 105): 'America/Anguilla',
          (105, 140, 140): 'America/Antigua',
          ( 35,  35, 175): 'America/Araguaina',
          (105, 245, 245): 'America/Argentina/Buenos_Aires',
          ( 35, 210, 175): 'America/Argentina/Catamarca',
          (140, 175,  35): 'America/Argentina/Cordoba',
          ( 70, 245, 210): 'America/Argentina/Jujuy',
          (140,  35, 245): 'America/Argentina/La_Rioja',
          ( 70, 245, 140): 'America/Argentina/Mendoza',
          ( 35, 210, 140): 'America/Argentina/Rio_Gallegos',
          ( 70,  70, 175): 'America/Argentina/Salta',
          (175, 210,  70): 'America/Argentina/San_Juan',
          (175,  70, 245): 'America/Argentina/San_Luis',
          ( 70, 105,   0): 'America/Argentina/Tucuman',
          (140, 245,  35): 'America/Argentina/Ushuaia',
          (140,   0,  70): 'America/Aruba',
          (105, 175, 210): 'America/Asuncion',
          (105, 210, 245): 'America/Atikokan',
          ( 70, 175, 175): 'America/Bahia',
          (  0, 210,  70): 'America/Bahia_Banderas',
          (105, 140, 105): 'America/Barbados',
          (210, 175, 105): 'America/Belem',
          (  0, 245,  70): 'America/Belize',
          (140,  35, 175): 'America/Blanc-Sablon',
          (175, 210, 175): 'America/Boa_Vista',
          (210, 245, 105): 'America/Bogota',
          (  0, 175,  35): 'America/Boise',
          ( 70,  35, 175): 'America/Cambridge_Bay',
          (175,  35, 140): 'America/Campo_Grande',
          (210, 175,  35): 'America/Cancun',
          (210, 140, 140): 'America/Caracas',
          (210,   0, 175): 'America/Cayenne',
          (105, 210,  35): 'America/Cayman',
          (105, 105,  35): 'America/Chicago',
          (105,   0,  35): 'America/Chihuahua',
          ( 35,  70, 210): 'America/Coral_Harbour',
          (210, 105, 245): 'America/Costa_Rica',
          (140,  70, 105): 'America/Creston',
          (210,  35,  35): 'America/Cuiaba',
          ( 35, 245,   0): 'America/Curacao',
          (175, 175,  35): 'America/Danmarkshavn',
          (175, 140,   0): 'America/Dawson',
          ( 70,  35,  70): 'America/Dawson_Creek',
          (140, 175, 210): 'America/Denver',
          ( 35,  70, 140): 'America/Detroit',
          (  0, 105,  70): 'America/Dominica',
          (105, 245, 105): 'America/Edmonton',
          (140,   0, 245): 'America/Eirunepe',
          (140,  70, 245): 'America/El_Salvador',
          (140, 175, 105): 'America/Fort_Nelson',
          ( 70, 140,  35): 'America/Fortaleza',
          ( 35, 210,  35): 'America/Glace_Bay',
          ( 70,   0, 105): 'America/Godthab',
          ( 70, 245, 105): 'America/Goose_Bay',
          ( 35, 245, 210): 'America/Grand_Turk',
          ( 35, 175,  70): 'America/Grenada',
          (140, 140, 245): 'America/Guadeloupe',
          (210, 210,  35): 'America/Guatemala',
          (210, 105,  35): 'America/Guayaquil',
          (175,   0,  70): 'America/Guyana',
          ( 70, 105,  35): 'America/Halifax',
          (210, 175,   0): 'America/Havana',
          (210, 175,  70): 'America/Hermosillo',
          ( 35, 210, 210): 'America/Indiana/Indianapolis',
          (140,  70,   0): 'America/Indiana/Knox',
          (210, 140,  70): 'America/Indiana/Marengo',
          ( 35,   0, 245): 'America/Indiana/Petersburg',
          ( 35, 210, 245): 'America/Indiana/Tell_City',
          (210, 175, 245): 'America/Indiana/Vevay',
          (175,  35, 245): 'America/Indiana/Vincennes',
          (105, 210, 105): 'America/Indiana/Winamac',
          ( 35,  35,  70): 'America/Inuvik',
          ( 70, 175,  35): 'America/Iqaluit',
          ( 35, 140, 105): 'America/Jamaica',
          (210,  35, 210): 'America/Juneau',
          ( 70,  70, 245): 'America/Kentucky/Louisville',
          ( 70,   0, 175): 'America/Kentucky/Monticello',
          ( 35, 175, 210): 'America/Kralendijk',
          (105,  70, 245): 'America/La_Paz',
          (105,  35, 245): 'America/Lima',
          (  0, 210, 175): 'America/Los_Angeles',
          (175, 245, 210): 'America/Lower_Princes',
          (175, 105, 140): 'America/Maceio',
          (140, 105,   0): 'America/Managua',
          ( 70, 245,  35): 'America/Manaus',
          (210, 245,  70): 'America/Marigot',
          (175, 140,  70): 'America/Martinique',
          (210,  70, 140): 'America/Matamoros',
          (210, 210, 140): 'America/Mazatlan',
          ( 35, 105, 245): 'America/Menominee',
          (  0, 210,  35): 'America/Merida',
          (105,   0, 105): 'America/Metlakatla',
          (105, 105,  70): 'America/Mexico_City',
          ( 35,  70,  70): 'America/Miquelon',
          ( 35, 175,   0): 'America/Moncton',
          (210, 105, 175): 'America/Monterrey',
          (140,  35, 105): 'America/Montevideo',
          (  0, 140, 245): 'America/Montreal',
          ( 35, 210,   0): 'America/Montserrat',
          (140, 210, 210): 'America/Nassau',
          ( 70, 175,  70): 'America/New_York',
          (175, 175,   0): 'America/Nipigon',
          ( 70, 105, 140): 'America/Nome',
          (140, 245, 175): 'America/Noronha',
          ( 35, 105, 210): 'America/North_Dakota/Beulah',
          ( 70,   0,   0): 'America/North_Dakota/Center',
          ( 35,   0, 175): 'America/North_Dakota/New_Salem',
          (210, 210, 175): 'America/Ojinaga',
          (  0, 175,   0): 'America/Panama',
          (105, 245,  70): 'America/Pangnirtung',
          (105, 105, 245): 'America/Paramaribo',
          (  0, 140,   0): 'America/Phoenix',
          (  0, 140, 210): 'America/Port-au-Prince',
          (105,   0,  70): 'America/Port_of_Spain',
          (175, 175, 175): 'America/Porto_Velho',
          (210, 245,  35): 'America/Puerto_Rico',
          (210,  70, 175): 'America/Rainy_River',
          (175,  35, 210): 'America/Rankin_Inlet',
          (105, 105,   0): 'America/Recife',
          (175,  35,  35): 'America/Regina',
          ( 70, 140, 175): 'America/Resolute',
          ( 70, 210, 210): 'America/Rio_Branco',
          (175,  70,   0): 'America/Santarem',
          (  0, 175, 140): 'America/Santiago',
          (105, 245, 175): 'America/Santo_Domingo',
          (175, 140, 140): 'America/Sao_Paulo',
          ( 35, 140, 245): 'America/Scoresbysund',
          (  0, 210, 210): 'America/Sitka',
          (105,  35,  70): 'America/St_Barthelemy',
          (140, 245, 210): 'America/St_Johns',
          (175, 105,  35): 'America/St_Kitts',
          (210,   0, 210): 'America/St_Lucia',
          (175, 175, 140): 'America/St_Thomas',
          (  0, 105, 105): 'America/St_Vincent',
          ( 35, 140, 140): 'America/Swift_Current',
          (175, 245,  70): 'America/Tegucigalpa',
          (175,  35,  70): 'America/Thule',
          (210,   0,  70): 'America/Thunder_Bay',
          (105, 105, 140): 'America/Tijuana',
          (140,  35,   0): 'America/Toronto',
          (175,   0, 140): 'America/Tortola',
          (  0, 245, 105): 'America/Vancouver',
          (175,  70, 140): 'America/Whitehorse',
          (140, 210, 175): 'America/Winnipeg',
          ( 35, 245,  35): 'America/Yakutat',
          ( 70, 140, 105): 'America/Yellowknife',
          ( 35,  35, 140): 'Antarctica/Macquarie',
          ( 70,   0, 210): 'Arctic/Longyearbyen',
          (105,  70,  35): 'Asia/Aden',
          (175, 210, 105): 'Asia/Almaty',
          (105, 105, 175): 'Asia/Amman',
          (210,  35, 105): 'Asia/Anadyr',
          ( 70,  35, 210): 'Asia/Aqtau',
          (140,   0, 210): 'Asia/Aqtobe',
          ( 35,  70, 105): 'Asia/Ashgabat',
          (  0, 175, 105): 'Asia/Baghdad',
          ( 70,   0, 140): 'Asia/Bahrain',
          ( 35,  35,   0): 'Asia/Baku',
          (140, 175, 175): 'Asia/Bangkok',
          (140, 210, 105): 'Asia/Barnaul',
          (210, 175, 175): 'Asia/Beirut',
          (105, 245, 210): 'Asia/Bishkek',
          (105, 175, 140): 'Asia/Brunei',
          (210, 210,   0): 'Asia/Chita',
          (105, 140,  35): 'Asia/Choibalsan',
          (210, 175, 140): 'Asia/Chongqing',
          (140, 245,  70): 'Asia/Colombo',
          (210,  35, 175): 'Asia/Damascus',
          (105,  70, 175): 'Asia/Dhaka',
          (175, 210,   0): 'Asia/Dili',
          (175,  70, 105): 'Asia/Dubai',
          (105, 175,   0): 'Asia/Dushanbe',
          (140,  70, 210): 'Asia/Gaza',
          (  0, 245,  35): 'Asia/Harbin',
          (175, 105, 105): 'Asia/Hebron',
          (  0, 175,  70): 'Asia/Ho_Chi_Minh',
          (210, 140, 175): 'Asia/Hong_Kong',
          ( 70,  35, 245): 'Asia/Hovd',
          ( 70, 105, 245): 'Asia/Irkutsk',
          (  0, 210, 245): 'Asia/Jakarta',
          (210, 245,   0): 'Asia/Jayapura',
          (  0, 105, 245): 'Asia/Jerusalem',
          (210,  35, 140): 'Asia/Kabul',
          (210,  70,  35): 'Asia/Kamchatka',
          (105,  35, 140): 'Asia/Karachi',
          (  0, 105, 175): 'Asia/Kashgar',
          (140, 140,  70): 'Asia/Kathmandu',
          ( 35, 245, 245): 'Asia/Khandyga',
          (210,   0, 245): 'Asia/Kolkata',
          (140, 245, 105): 'Asia/Krasnoyarsk',
          (175, 105, 245): 'Asia/Kuala_Lumpur',
          (140, 245,   0): 'Asia/Kuching',
          (140,   0,   0): 'Asia/Kuwait',
          ( 70, 105, 105): 'Asia/Macau',
          ( 35,   0,  70): 'Asia/Magadan',
          (210, 140, 105): 'Asia/Makassar',
          (140, 175,   0): 'Asia/Manila',
          (210,   0,  35): 'Asia/Muscat',
          (105,   0, 245): 'Asia/Nicosia',
          ( 35, 175, 105): 'Asia/Novokuznetsk',
          ( 35, 140,   0): 'Asia/Novosibirsk',
          (210,  70, 245): 'Asia/Omsk',
          ( 70,  35,  35): 'Asia/Oral',
          (140,  70,  70): 'Asia/Phnom_Penh',
          (175, 210, 245): 'Asia/Pontianak',
          ( 70, 210,  35): 'Asia/Pyongyang',
          ( 35, 245, 140): 'Asia/Qatar',
          (140,   0, 175): 'Asia/Qyzylorda',
          ( 35, 245, 105): 'Asia/Rangoon',
          (105, 140,  70): 'Asia/Riyadh',
          ( 35, 105, 140): 'Asia/Sakhalin',
          ( 70, 175, 105): 'Asia/Samarkand',
          (  0, 140, 140): 'Asia/Seoul',
          (175,  35,   0): 'Asia/Shanghai',
          (175,  35, 105): 'Asia/Singapore',
          (105,  70,   0): 'Asia/Srednekolymsk',
          ( 70,  70, 140): 'Asia/Taipei',
          (140,  35, 140): 'Asia/Tashkent',
          (  0, 245, 210): 'Asia/Tbilisi',
          ( 35,  35,  35): 'Asia/Tehran',
          ( 35,  70,   0): 'Asia/Thimphu',
          (140, 175,  70): 'Asia/Tokyo',
          (175, 140, 245): 'Asia/Tomsk',
          ( 70,  70,  70): 'Asia/Ulaanbaatar',
          (210, 210, 105): 'Asia/Urumqi',
          (175, 245,  35): 'Asia/Ust-Nera',
          (140, 105, 245): 'Asia/Vientiane',
          ( 35, 140, 210): 'Asia/Vladivostok',
          ( 70, 105, 210): 'Asia/Yakutsk',
          ( 70, 245,  70): 'Asia/Yekaterinburg',
          (  0, 245, 245): 'Asia/Yerevan',
          (140, 210, 140): 'Atlantic/Azores',
          (140,  35, 210): 'Atlantic/Bermuda',
          (140, 105, 210): 'Atlantic/Canary',
          (175, 245, 175): 'Atlantic/Cape_Verde',
          (210,   0, 140): 'Atlantic/Faroe',
          ( 35,  70, 175): 'Atlantic/Madeira',
          (105, 210, 140): 'Atlantic/Reykjavik',
          ( 35, 105,  70): 'Atlantic/South_Georgia',
          ( 70, 175, 245): 'Atlantic/St_Helena',
          ( 35, 210,  70): 'Atlantic/Stanley',
          ( 35, 105, 175): 'Australia/Adelaide',
          (140,   0, 105): 'Australia/Brisbane',
          ( 70,  70, 210): 'Australia/Broken_Hill',
          (  0, 245,   0): 'Australia/Currie',
          ( 35,  70,  35): 'Australia/Darwin',
          ( 35, 175,  35): 'Australia/Eucla',
          ( 70,   0, 245): 'Australia/Hobart',
          (105, 175, 105): 'Australia/Lindeman',
          (  0, 105, 140): 'Australia/Lord_Howe',
          ( 70, 105,  70): 'Australia/Melbourne',
          ( 35,   0, 105): 'Australia/Perth',
          (105, 140, 210): 'Australia/Sydney',
          # (0,  35, 210): 'Etc/GMT+1',
          # (0,  70, 245): 'Etc/GMT+10',
          # (0, 105,   0): 'Etc/GMT+11',
          # (0, 105,  35): 'Etc/GMT+12',
          # (0,  35, 245): 'Etc/GMT+2',
          # (0,  70,   0): 'Etc/GMT+3',
          # (0,  70,  35): 'Etc/GMT+4',
          # (0,  70,  70): 'Etc/GMT+5',
          # (0,  70, 105): 'Etc/GMT+6',
          # (0,  70, 140): 'Etc/GMT+7',
          # (0,  70, 175): 'Etc/GMT+8',
          # (0,  70, 210): 'Etc/GMT+9',
          # (0,  35, 140): 'Etc/GMT-1',
          # (0,   0, 105): 'Etc/GMT-10',
          # (0,   0,  70): 'Etc/GMT-11',
          # (0,   0,  35): 'Etc/GMT-12',
          # (0,  35, 105): 'Etc/GMT-2',
          # (0,  35,  70): 'Etc/GMT-3',
          # (0,  35,  35): 'Etc/GMT-4',
          # (0,  35,   0): 'Etc/GMT-5',
          # (0,   0, 245): 'Etc/GMT-6',
          # (0,   0, 210): 'Etc/GMT-7',
          # (0,   0, 175): 'Etc/GMT-8',
          # (0,   0, 140): 'Etc/GMT-9',
          # (0,  35, 175): 'Etc/GMT0',
          (210, 105, 140): 'Europe/Amsterdam',
          (210, 210, 245): 'Europe/Andorra',
          (  0, 210, 105): 'Europe/Astrakhan',
          (105, 105, 105): 'Europe/Athens',
          (105, 175,  35): 'Europe/Belgrade',
          (  0, 140,  35): 'Europe/Berlin',
          ( 70, 245, 245): 'Europe/Bratislava',
          (140,  70, 175): 'Europe/Brussels',
          (140, 140,   0): 'Europe/Bucharest',
          (105,   0, 210): 'Europe/Budapest',
          (210,  70, 210): 'Europe/Busingen',
          (140, 210,  70): 'Europe/Chisinau',
          (175,  70,  70): 'Europe/Copenhagen',
          (140, 210, 245): 'Europe/Dublin',
          (210, 210,  70): 'Europe/Gibraltar',
          (140, 245, 245): 'Europe/Guernsey',
          (175, 245, 245): 'Europe/Helsinki',
          (140,  35,  35): 'Europe/Isle_of_Man',
          (105,  35, 175): 'Europe/Istanbul',
          (175, 245,   0): 'Europe/Jersey',
          (105,  35,  35): 'Europe/Kaliningrad',
          (140, 140, 140): 'Europe/Kiev',
          (210,  35, 245): 'Europe/Kirov',
          ( 35,  35, 105): 'Europe/Lisbon',
          ( 70, 210, 140): 'Europe/Ljubljana',
          (175,   0, 210): 'Europe/London',
          (105, 175,  70): 'Europe/Luxembourg',
          (175, 140, 210): 'Europe/Madrid',
          (175,   0, 175): 'Europe/Malta',
          (105,  70, 210): 'Europe/Mariehamn',
          (210, 140, 245): 'Europe/Minsk',
          (140, 105,  70): 'Europe/Monaco',
          (105, 245, 140): 'Europe/Moscow',
          (210,   0, 105): 'Europe/Oslo',
          (175,   0,  35): 'Europe/Paris',
          (105,  35, 105): 'Europe/Podgorica',
          (105, 210,   0): 'Europe/Prague',
          (175, 140, 105): 'Europe/Riga',
          (140, 140, 210): 'Europe/Rome',
          ( 70, 210,   0): 'Europe/Samara',
          (175,  70, 210): 'Europe/San_Marino',
          (175, 210, 140): 'Europe/Sarajevo',
          (105,   0, 175): 'Europe/Simferopol',
          (175, 175, 105): 'Europe/Skopje',
          (175, 175, 245): 'Europe/Sofia',
          (210, 140,   0): 'Europe/Stockholm',
          ( 35,   0,   0): 'Europe/Tallinn',
          ( 35, 140, 175): 'Europe/Tirane',
          ( 35, 140,  35): 'Europe/Ulyanovsk',
          (210, 140,  35): 'Europe/Uzhgorod',
          ( 35,   0, 140): 'Europe/Vaduz',
          ( 35,  35, 210): 'Europe/Vatican',
          (140, 140, 175): 'Europe/Vienna',
          ( 35,   0, 210): 'Europe/Vilnius',
          ( 35, 245,  70): 'Europe/Volgograd',
          (105,  70, 105): 'Europe/Warsaw',
          (  0, 175, 245): 'Europe/Zagreb',
          ( 70, 140,   0): 'Europe/Zaporozhye',
          ( 70, 175, 210): 'Europe/Zurich',
          ( 35, 245, 175): 'Indian/Antananarivo',
          (  0, 140, 105): 'Indian/Chagos',
          ( 70,  70, 105): 'Indian/Christmas',
          ( 35, 175, 140): 'Indian/Cocos',
          (105, 175, 175): 'Indian/Comoro',
          (140, 105, 175): 'Indian/Kerguelen',
          ( 35, 105,   0): 'Indian/Mahe',
          (210, 105, 105): 'Indian/Maldives',
          (140,   0,  35): 'Indian/Mauritius',
          (175, 245, 105): 'Indian/Mayotte',
          (140, 140, 105): 'Indian/Reunion',
          (105,  35,   0): 'Pacific/Apia',
          (210, 105,  70): 'Pacific/Auckland',
          (105, 140, 245): 'Pacific/Bougainville',
          ( 35,  35, 245): 'Pacific/Chatham',
          (105, 175, 245): 'Pacific/Chuuk',
          (140, 105, 140): 'Pacific/Easter',
          (140,  70, 140): 'Pacific/Efate',
          (140, 210,   0): 'Pacific/Enderbury',
          (175, 175,  70): 'Pacific/Fakaofo',
          ( 70, 140,  70): 'Pacific/Fiji',
          ( 35,  70, 245): 'Pacific/Funafuti',
          ( 70,  35,   0): 'Pacific/Galapagos',
          (175,  70,  35): 'Pacific/Gambier',
          (175,   0, 245): 'Pacific/Guadalcanal',
          ( 35, 175, 175): 'Pacific/Guam',
          (140,  35,  70): 'Pacific/Honolulu',
          ( 35,   0,  35): 'Pacific/Johnston',
          (140,   0, 140): 'Pacific/Kiritimati',
          (105, 210,  70): 'Pacific/Kosrae',
          (140, 245, 140): 'Pacific/Kwajalein',
          (  0, 175, 175): 'Pacific/Majuro',
          ( 70,   0,  70): 'Pacific/Marquesas',
          (105,   0, 140): 'Pacific/Midway',
          (210, 140, 210): 'Pacific/Nauru',
          (210,  70,  70): 'Pacific/Niue',
          (105, 245,  35): 'Pacific/Norfolk',
          (210,  70,   0): 'Pacific/Noumea',
          (  0, 245, 140): 'Pacific/Pago_Pago',
          (105,  70,  70): 'Pacific/Palau',
          ( 70,   0,  35): 'Pacific/Pitcairn',
          (105, 210, 210): 'Pacific/Pohnpei',
          ( 70, 210, 175): 'Pacific/Port_Moresby',
          (210,  35,   0): 'Pacific/Rarotonga',
          (210, 175, 210): 'Pacific/Saipan',
          (175, 210,  35): 'Pacific/Tahiti',
          ( 70, 140, 140): 'Pacific/Tarawa',
          ( 70,  70,   0): 'Pacific/Tongatapu',
          ( 70, 105, 175): 'Pacific/Wake',
          (  0, 105, 210): 'Pacific/Wallis',
          (  0, 245, 175): 'Pacific/Yap',
          ( 70,  70,  35): 'uninhabited'}

if __name__ == '__main__':
    lat, lon = get_latlon()
    pix_x, pix_y, _rgb_values, timezone = lookup(lat, lon)
    print('Lat:', lat, ' Lon:', lon)
    print('Timezone:', timezone, 'px:', pix_x, 'py:', pix_y)
#
# End
