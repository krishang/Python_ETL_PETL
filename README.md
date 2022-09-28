# Welcome to Python ETL with the PETL library

Python ETL using  [PETL](https://petl.readthedocs.io/)  to load a bunch of CSV files to a MSSQL DB. Update the config.ini file with the desired user and path variables. I am using PETL for the CSV file upload. 

## Points to Note
The PETL library does not do an accurate job of sizing the database table fields. All the fields will be of varchar thus you will need to review the table and update the table fields data types as desired. 

To trouble shoot the **string binary truncation error**, which is spit out by MSSQL update the following flags.  Enable tracing to figure out which fields needs data type adjustment.
I would strongly recommend doing this on a test server and switch this off once trouble shooting is done.

``` sql
/* This script needs to be run on the MSSQL server. At the time of the writing, I am using SQL2016. 
  Check equivalent for other versions.
            Enable and disable error tracing on the tables 
            DBCC TRACEON(460, -100);  -- enable errors
            DBCC TRACEOFF(460, -100); -- disable errors
            GO
*/
```
