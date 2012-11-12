                       The Global Airport Database
                         Release Version 0.0.1

Author: Arash Partow 2003
Copyright notice:
Free use of The Global Airport Database is permitted under the guidelines
and in accordance with the most current version of the Common Public License.
http://www.opensource.org/licenses/cpl.php


Introduction


The Global Airport Database is a FREE online downloadable database of aiports
big and small from around the world. The database is presented in a simple
token seperated format.


For more information please visit:

http://www.partow.net/miscellaneous/airportdatabase/index.html

Description

The Global Airport Database is a FREE online downloadable database of 9300 airports big and small from around the world. The database is presented in a simple token separated format. The database provides detailed information about the airports listed including ICAO and IATA codes, country and city, latitude-longitude coordinates and also altitude from mean sea level.

The Global Airport Database Structure

The Global Airport Database is comprised from a series of tuples. Each tuple contains exactly 14 fields of varying pieces of information. The fields depending on what they represent are either a text string, integer values or character. Some of the fields are of constant length whilst others are of varying length. The fields are separated from each other by one colon character ":" acting as a delimiter. There are no leading or trailing delimiters.

Every field must be populated by a value, in the event that a value does not exist for the particular field a string of value "N/A" or ASCII character 0 or for coordinate directions the ASCII character U will be used to represent unknown entity.

The primary key for The Global Airport Database is the airport's ICAO code which is the value in field 1.

The fields are in the following order and have the following properties and meanings:

Field 01 - ICAO Code: 4 character ICAO code
Field 02 - IATA Code: 3 character IATA code
Field 03 - Airport Name: string of varying length
Field 04 - City,Town or Suburb: string of varying length
Field 05 - Country: string of varying length
Field 06 - Latitude Degrees: 2 ASCII characters representing one numeric value
Field 07 - Latitude Minutes: 2 ASCII characters representing one numeric value
Field 08 - Latitude Seconds: 2 ASCII characters representing one numeric value
Field 09 - Latitude Direction: 1 ASCII character either N or S representing compass direction
Field 10 - Longitude Degrees: 2 ASCII characters representing one numeric value
Field 11 - Longitude Minutes: 2 ASCII characters representing one numeric value
Field 12 - Longitude Seconds: 2 ASCII characters representing one numeric value
Field 13 - Longitude Direction: 1 ASCII character either E or W representing compass direction
Field 14 - Altitude: varying sequence of ASCII characters representing a numeric value corresponding to the airport's altitude from mean sea level (ie: "123" or "-123")
