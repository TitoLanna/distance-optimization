
##########################################################
### Finding Distance From User Input Address to Nearest###
### Daycare location from the state website list       ###
##########################################################
 
import pandas as pd
from geopy import distance
import geopy as gp
 
# home = input("Enter Home Address: ")
# work = input("Enter Work Address: ")
home = '140 N Poplar Ave, Tea, SD 57064'
work = '515 E Cherry St, Vermillion, SD 57069'
 
locator = gp.Nominatim(user_agent="myGeocoder")
location = locator.geocode(home)
home_lat = location.latitude
home_long = location.longitude
 
location = locator.geocode(work)
work_lat = location.latitude
work_long = location.longitude
 
origin = (home_lat, home_long)
dest = (work_lat, work_long)
### The following will calculate the geographical distance
### "As the crow flies"
result = distance.distance(origin, dest)
result.miles
 
df_ProviderList = pd.read_csv('ProviderList.csv')
df_ProviderList['Zip'] = df_ProviderList['Mailing Zipcode'].apply(lambda x: str(x))
cols = ['Location Address 1', 'City', 'State', 'Zip']
df_ProviderList['address'] = df_ProviderList[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
 
from geopy.extra.rate_limiter import RateLimiter
###https://towardsdatascience.com/geocode-with-python-161ec1e62b89
# 1 - conveneint function to delay between geocoding calls
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
# 2- - create location column
df_ProviderList['location'] = df_ProviderList['address'].apply(geocode)
# 3 - create longitude, laatitude and altitude from location column (returns tuple)
df_ProviderList['point'] = df_ProviderList['location'].apply(lambda loc: tuple(loc.point) if loc else None)
# 4 - split point column into latitude, longitude and altitude columns
df_ProviderList[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df_ProviderList['point'].tolist(), index=df_ProviderList.index)
#df_ProviderList['Lat'] = df_ProviderList['address'].apply(lambda x: locator.geocode(x))
 
###Filter Dataframe to remove invalid addresses
df_ProvList = df_ProviderList[df_ProviderList['point'].notnull()]
 
def calc_distance_home(row):
    lat = row['latitude']
    long = row['longitude']
    loc = (lat, long)
    d = distance.distance(origin, loc)
    return d.miles
 
def calc_distance_work(row):
    lat = row['latitude']
    long = row['longitude']
    loc = (lat, long)
    d = distance.distance(dest, loc)
    return d.miles
 
df_ProvList['dist_home'] = df_ProvList.apply(calc_distance_home, axis=1)
df_ProvList['dist_work'] = df_ProvList.apply(calc_distance_work, axis=1)
df_ProvList['total_dist'] = df_ProvList['dist_home'] + df_ProvList['dist_work']
 
df_ProvList.to_csv("ProviderFileWithMileage_22MAR2023.csv")
