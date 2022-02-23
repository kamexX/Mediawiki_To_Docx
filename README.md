###############################################################################################################
#
#   Generating DOCX FILES from the Mediawiki HTML 
#   
#   * get the page names from the mediawiki database 
#   * login via api using srvautomation user
#   * change the img src direction
#   * remove unnecessary html content (like footer, navigation, links etc.) 
#   * change thumb picture to full pictures
#   * stored as "{title}.docx" into the subfolder: "mediawikiPageAsDocx" 
#
#
#   preliminarys:
#   * set up the enviroment variables MEDIAWIKI_LOGIN_USER, MEDIAWIKI_LOGIN_PASS, MEDIAWIKI_DB_USER, MEDIAWIKI_DB_PASS
#   * change the DB Host Variable
#
#
###############################################################################################################
