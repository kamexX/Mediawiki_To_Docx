# Generate .docx files from a mediawiki  
Get the Website Pagenames from the Mediawiki DB 
Login via API and use session to fetch the HTML Content
Change the Image Source Location, to get the pictures in the .docx file
Remove some unnecessary html content like footer, navigation etc. 
Change a thumbnail to full pictures
Store the DOCX as "{title}.docx" into the subfolder: "mediawikiPageAsDocx" 

# Preliminarys:
Install pypandoc
Install bs4
Install mysql.conector
Set up the enviroment variables:
* MEDIAWIKI_LOGIN_USER
* MEDIAWIKI_LOGIN_PASS
* MEDIAWIKI_DB_USER
* MEDIAWIKI_DB_PASS

Change the following constans:
* PROTOCOL
* HTML_HOSTNAME
* DATABASE_HOSTNAME (optional)
* DATABASE_NAME (optional)
* MEDIAWIKI_URI 
* MEDIAWIKI_UNIX_PATH
* OUTPUT PATH (if it is not wanted that the folder should be in the same directory as the script)


# Known Problems:
* Pandoc Installation
* Mediawiki API activation
* No Images in the Output File
