# Generate .docx files from a mediawiki  
* get the page names from the mediawiki database 
* login via api
* change the img src direction
* remove unnecessary html content like footer, navigation etc. 
* change thumb picture to full pictures
* stored as "{title}.docx" into a subfolder: "mediawikiPageAsDocx" 

# Preliminarys:
* install pypandoc
* install bs4
* install mysql.conector

* set up the enviroment variables:
** MEDIAWIKI_LOGIN_USER
** MEDIAWIKI_LOGIN_PASS
** MEDIAWIKI_DB_USER
** MEDIAWIKI_DB_PASS

* change the following constans:
** PROTOCOL
** HTML_HOSTNAME
** DATABASE_HOSTNAME (optional)
** DATABASE_NAME (optional)
** MEDIAWIKI_URI 
** MEDIAWIKI_UNIX_PATH
** OUTPUT PATH (if it is not wanted that the folder should be in the same directory as the script)


# Known Problems:
* installation of pypandoc
* mediawiki api activation
