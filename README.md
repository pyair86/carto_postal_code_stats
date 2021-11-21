
# Postal Code Statistics Endpoints

Goal is to expose to frontend integrated data of postal codes and geometries,   
so that each **geometry with corresponding attributes** can be accessible.

4 endpoints are accessible:

1. Specific postal code with its data - http://127.0.0.1:3000/postal_codes/28011
2. Specific postal code with aggregated data by column (e.g. age) - http://127.0.0.1:3000/postal_codes_agg/28011
3. All postal codes combined into a single polygon with its data - http://127.0.0.1:3000/postal_codes/
4. All postal codes combined into a single polygon with aggregated data by column  - http://127.0.0.1:3000/postal_codes_agg/

It can be used when business and spatial data need to be integrated with other data.  
It's achievable by changing configurations in the config files, and SQL commands stored in TXT files. 

Multithreading was implemented in order to copy the input data in parallel, if there are many input data sources.  
Max threads number can be defined by necessity by the user.

The frontend developer will have to register and login in order to access the geojsons.

Used tools: Docker, Flask, PostGIS

Task was given by the company Carto.



##Instructions:


1. git clone https://github.com/pyair86/carto_postal_code_stats

2. In terminal, go to the cloned directory and execute: **docker-compose build** 

3. Execute: **docker-compose up**
   Ports 3000,5000, 3333 and 5432 must be free 

4. Open another terminal (**without** closing the first one), and go to the cloned folder,in order to set up the data.  
   run: **docker-compose exec web bash -c "python /myApp/App/setup_db.py"**    

5. In browser: http://127.0.0.1:3000/

6. Register - password requires at least 6 digits

7. Login

8. Click Aggregated stats/Turnover per year to access the json for the <b>collected polygon</b>.  
   To access <b>specific</b> polygons - add the postal_code in the URL   
   e.g., http://127.0.0.1:3000/postal_codes_agg/28011


## Running Tests:


From cloned directory run in terminal: **docker-compose exec web bash -c "pytest /myApp/App/tests"**


## Accessing the DB:

From cloned directory run in terminal: **docker exec -ti carto_postal_code_stats_postgis_1 psql -U carto**


## Considerations:

1. *Aggregate all polygons into a single polygon* -  collect was select over union:
 A. ST_Collect is much faster than ST_Union, because it does not dissolve boundaries or check for overlapping regions. 
   It simply combines geometries into MULTI*s or GEOMETRYCOLLECTIONs.
 B. Dissolving boundaries and overlapping regions – like ST_Union does – can lead to undesired effects. 


2. Enforcing check *non overlapping polygons*:  
   Polygons are not allowed to overlap each other. I wanted to prevent that situation before and after the data insert
   into the table.   
   Luckily the data set doesn't contain intersected polygons, but if it were, here's the result of  
   edited overlapping polygons with ID 6179 & 6061 from the dataset:  

    <img width="328" alt="overlapping" src="https://user-images.githubusercontent.com/1562330/142782961-2eda0a74-df2c-4736-aced-f87d6eeb2eb4.PNG">


3. SQL commands, configurations, paths, are not part from the PY files and only read by them.  

4. I was hesitating between setting a *ST_IsValid and ST_MakeValid* constraint, but went with IsValid,
   because I want to avoid unexpected values.  

5. A new POLYGON table was created (dumped) from the mixed MULTI and POLYGON geometries:
   Index works faster with POLYGON. 

6. The mixed MULTI and POLYGON geometries table becomes a MULTIPOLYGON so a type constraint can be enforced.

7. Copy CSV data using Postgres is the fastest way I found to insert data into the table from a CSV.

8. SRID is constraind to 4326 because it's common by frontend maps frameworks.

9. https://geojsonlint.com/ was used to make sure the geojsons present the correct coordinates.

10. Postal codes must start with 28 and contain 5 digits for this particular data set.


##Improvments/real project requirements:


1. CI-CD  - writing a file to run tests automatically when code is commited, and for a deployment pipeline.
2. Tests - aiming for quality unit tests with a satisfying code coverage, and employing Selenium for other types of automated tests.  
   E.g. in a real project an empty DB must be used, and login required endpoints must be well checked. 
3. Error handling - currently too broad in the controllers, so more catching cases should be added.
4. Splitting the DB migration, data population and API commands.
5. Input data processing - currently the input data files are processed in parallel,  
   but what if each file itself is enormous? It might be necessary to split them into chunks.
6. DB - applying more geom restrictions: for instance, new polygons can't be added outside/inside of a defined place (e.g., Madrid only), 
   geom area must be smaller than a defined value... 
7. Storing and querying geom strategies - for example, checking *simplification* of geom to save space by
   checking if info was lost after simplification, via a comparison of before-after tables.
8. Cache - finding a suitable cache strategy for each endpoint and timeout.
9. React - for a stateful and better organized frontend experience.
10. Emails - forgot password, and welcome. 
11. Aggregation - Pandas&Geopandas might come in useful in real project situations to manipulate geospatial data.