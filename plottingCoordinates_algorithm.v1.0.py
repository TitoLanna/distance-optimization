"""To run this code first install ipyleaflet """
import ipyleaflet as Lf
from geopy import distance



#----------------Input Data---------------- 
                    #With X being the longitude and Y being the latitude
x_home=42.7873200
y_home=-96.7317125     
x_daycare=42.8690209   
y_daycare=-97.3903966  
x_work=43.5252375     
y_work=-96.7317125     

xy_home=(x_home,y_home)
xy_daycare=(x_daycare,y_daycare)
xy_work=(x_work,y_work)
daycareName='Free kids'            #Name of daycare 
companyName='Business Ink'         #Name of Company 




#------------Processing---------------
mp=Lf.Map(center=xy_home,zoom= 8)      #Using an already built Map function in the ipyleaflet library to create a Map 



#----------------------calculating the distance between home and work---------------------------
dist=distance.distance(xy_home,xy_work)    
_Circle_radius=int(dist.km)*1000                 #finding the radius for our circle

#--------------------Location--------------------------------------
_location ={ 'Home':{'coordinates':xy_home,'name':'Home Address'},
             'Daycare':{'coordinates':xy_daycare,'name':daycareName},
             'Work':{'coordinates':xy_work,'name':companyName}
          }
for address in _location:           #Iterate through the  Dictionary
    point =_location[address]['coordinates']     #Gets the coordinates stored the dictionary named _location
    AdName=_location[address]['name']            #Gets the name stored the dictionary named _location
    marker=Lf.Marker(location=point,title=AdName) #I assign the location and name of location to marker
    mp   +=marker                                 # Adds the points to the Map
#-------------------Drawing a circle using the distance between work and Home divided by 2 to as the radius---------    
circle=Lf.Circle()
circle.location =xy_work           # Using work as the center of origin of our location
circle.radius = _Circle_radius     #radius of our circle
circle.color = "greenyellow"

#--------------------------Drawing a line from home to work--------------
line =Lf.AntPath(locations=[xy_home,xy_work],color="black",fill=False)

#---------------------------Adding layers to our map---------------------
mp.add_layer(circle) 
mp.add_layer(line)



#--------------Output-------------------    
mp #Prints out the Map with the plotted points
