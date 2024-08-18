Band-Gear-Exchange-Forum statusreport 18.08.24:
BGEF_v5 is total rewrite of the BGEF_v4.
- DB-schema is changed, now 7 tables
- sql-views are added
- ORM has removed completely
- UI-templates are new as well as routes, no models at all used
- test data is new
- -file structure tree is new
- BGEF_v5 runs but only only one route (home) is tested

Band-Gear-Exchange-Forum statusreport 04.08.24:

PostgreSQL db created in my local PC:

    - db schema designed and created with primary and foreign keys (9 tables)
    
    - db is populated with test data
    
    - db inquiries and sql-views tested (couple of relevant use-cases of the service)
    
    - first development version of the bgef-db is ready (version 4)
    
Next steps for db: already coded test-service use-cases as sql-views will be tested
to find out the most feasible use cases for the final bgef-service.

MS Edge Copilot LLM assisted in development following standard CRUD and Fetch-services.
These e2e-services are mainly targeted to test the db-schema and support as a prototyping 
tool in innovation of the final use-cases of BGEF-service:

Flask application: CRUD and Fetch(all and one) use-cases.
Coded but not tested: model, service, controller and HTML/css-based UI for CRUD and Fetch.

Next steps with bgef-service: most feasible use-cases will be defined and prototyped.
The allready coded Flask-components will be tested soon and db solution will be tested
thoroughly with CRUD and Fetch functions. Based on the experiences the bgef-service 
use-cases and related UI will be designed for prototyping.

Documentation: documents will be updated soon: entity-diagram, db-schema, use-cases and UI, instructions.
Testing: Test-log will be maintained, test data-set will be improved according to selected use-cases
Configuration: config-files will be maintained and test-cycles speeded up (CI)


# band-gear-exchange
Band Gear Exchange Forum
