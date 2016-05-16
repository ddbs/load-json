# Project EMRYS Data Upload

## Script uploadToEMRYS
Read a newline delimited list of JSON objects and upload to emrys for analysis.

### Usage
```
$uploadToEMRYS -f <data file name> -u <ingest url>
```

### Notes
To determine your ingestion url, go to project emrys data services
(https://portal.projectemrys.com/data_services), select "Ingest", and use that url.
Or invoke the right click menu from "Ingest" and copy the link address.

To convert a csv file into json format for upload, use csvkit
    (http://csvkit.readthedocs.io)
</br>$ csvjson --stream csv-file > json-file
