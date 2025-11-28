# Dashlane to Bitwarden converter
Tool in python that converts Dashlane credential database (in CSV) to Bitwarden (individual vault only - CSV).

## Procedure
### Step 1 : 
Generate/download Dashlane CSV credential file

### Step 2 : 
Use this converter tool

### Step 3 :
Import newly generated file into Bitwarden.  
Import it to an individual vault by selecting Bitwarden (csv) from the File format list.  
For different importing ways : https://bitwarden.com/help/import-data/

## Tool
### Technical details
Based on ETL structure. Using parsing and pandas DataFrame. A straightforward mapped data convertion.
### Launching the tool
Using python : ```python importer_bitwarden.py```

## Dependency
Python 3.10.9

## Source
Based on the following Bitwarden doc :
- https://bitwarden.com/help/import-data/
- https://bitwarden.com/help/condition-bitwarden-import/#condition-a-json

## Disclamer
Made for individual vaults only (not organization vaults).  
This program uses sensitive data.  
Delete this file immediately after importing to Bitwarden.  
Do not share or commit this file to version control.