# Generate .docx files from a mediawiki  
* Get the Website Pagenames from the Mediawiki DB 
* Login via API and use session to fetch the HTML Content
* Change the Image Source Location, to get the pictures in the .docx file
* Remove some unnecessary html content like footer, navigation etc. 
* Change a thumbnail to full pictures
* Store the DOCX as "{title}.docx" into the subfolder: "mediawikiPageAsDocx" 

# Preliminarys:
* pip install -r requirements.txt
* Set up the enviroment variables:
    * set MEDIAWIKI_LOGIN_USER=root 
    * set MEDIAWIKI_LOGIN_PASS=myrootpassword
    * set MEDIAWIKI_DB_USER=root
    * set MEDIAWIKI_DB_PASS=myrootpass

Change the following constans in the source code:
* PROTOCOL
* HTML_HOSTNAME
* DATABASE_HOSTNAME (optional)
* DATABASE_NAME (optional)
* MEDIAWIKI_URI 
* MEDIAWIKI_UNIX_PATH
* OUTPUT PATH (if it is not wanted that the folder should be in the same directory as the script)


# Known Issues:
* Pandoc Installation
* Mediawiki API activation
* No Images in the Output File
