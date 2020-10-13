## Detour Design Document
*Marcus Lannon*

### 0. Overview
Detour is designed to help cyclists avoid closed roads. Current mapping software only shows closed roads for A-B navigation, rather than for a user defined route. Road side diversions are designed for cars, with no consideration of hills/road size - both of which have significant impact on cyclists. By pre-planning detours, an optimal route can be found, with no on bike frustation!


### 1. User Story
On the day of their ride, a user will upload the GPX file of their route. The app will then return a map with any closed roads that impact the route flagged. Detours will be suggested, or set manually and then the user can download the updated GPX file.


### 2. Technologies Used
#### 2.1 Backend
Python will be used to handle the route calculations and detours. The HERE Traffic API will be used for closed roads data. The webapp will be created using flask and hosted on AWS. 


### 3. Application Architecture
#### 3.1 Backend
Details of the structure and design of the backend. 
##### 3.1.1 Road
Since the exact long/lat of each GPX file and closed road route may differ slightly, functionality is required to map long/lat paths to roads.

##### 3.1.2 Routes
Each route will be turned into a route object. The primary function will be to parse the xml into a collection of Road objects. Route features will also be extracted/calculated such as a bounding box, *add more route features*. Closed roads can be fed into this class and any that intersect the route will be kept. 

##### 3.1.3 Closed Roads
Each closed road will be an object, with all of the features of the closed road as class variables. This will feature a track consisting of one or more closed Road objects.


#### 3.2 Frontend
##### 3.1.1 Design Principles
*todo*


