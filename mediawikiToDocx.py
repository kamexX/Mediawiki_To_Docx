__author__ = "Jendrik Basten"

# used to convert html to docx
from pypandoc import convert_text 

# parsing text to html
from bs4 import BeautifulSoup 

# using sessions for requesting the html pages
from requests import Session 

# disable ssl warnings due to self-signed certificates
from urllib3 import disable_warnings 

# system specific operations
from os import getenv, path, mkdir

# using for sql statements
import mysql.connector

# change: http/https
PROTOCOL            =   "http"

# change: ip addr or hostname
HTML_HOSTNAME       =   "192.168.0.0"

# sometimes the mediawiki runs on a different system, then you need to be sure that you have access from remote to the DB
DATABASE_HOSTNAME   =   "localhost"

# change your mediawiki database name
DATABASE_NAME       =   "my_wiki"

# your uri path like www.mywiki.com/mw/index.php?title=MainPage
MEDIAWIKI_URI       =   "/mw/"

# your os path where the images are stored
MEDIAWIKI_UNIX_PATH =   "/var/www/html/mw/"

# the output folder for the docx files
OUTPUT_FOLDER_DOCX  =   "mediawikiPageAsDocx/"

# MEDIAWIKI VARIABLES
MEDIAWIKI_API_URL   =   f"{PROTOCOL}://{ HTML_HOSTNAME }/{MEDIAWIKI_URI}api.php"
MEDIAWIKI_INDEX_URL =   f"{PROTOCOL}://{ HTML_HOSTNAME }/{MEDIAWIKI_URI}index.php"


def getPagenames(dbHostname: str, dbUsername: str, dbPassword: str, dbDatabasename: str) -> list:
    ''' Fetch the Pagenames out of the Database '''

    mediawikiPagenames = list()

    sqlStatement = "SELECT page_title FROM page WHERE (page_namespace = 0 AND LENGTH(page_title) > 1) ORDER BY page_title"

    # start db Connection
    dbConn = mysql.connector.connect(
        host=dbHostname,
        user=dbUsername,
        password=dbPassword,
        database=dbDatabasename,
    )

    # fetch a cursor to interact with the DB
    dbCursor = dbConn.cursor()
    dbCursor.execute(sqlStatement)
    pagenames = dbCursor.fetchall()

    # returns a bytearray like '(bytearray(b'3rd_Party'),)' 
    for page in pagenames:
        mediawikiPagenames.append( page[0].decode() )

    # generate the pagefile.txt
    print(f"[+] We found { len(mediawikiPagenames) } pages in your mediawiki database")

    return mediawikiPagenames


def getMediawikiSession(apiUrl: str, httpLoginUser: str, httpLoginPassword: str) -> Session:
    ''' Create a Mediawiki session '''

    # mediawiki login over theier api 
    # https://www.mediawiki.org/wiki/API:Main_page/de
    session     =   Session()

    r1 = session.get(apiUrl, verify=False, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
    })

    r2 = session.post(apiUrl, verify=False, data={
        'format': 'json',
        'action': 'login',
        'lgname': httpLoginUser,
        'lgpassword': httpLoginPassword,
        'lgtoken': r1.json()['query']['tokens']['logintoken'],
    })

    # login failed
    if r2.json()['login']['result'] != 'Success':
        raise RuntimeError(r2.json())

    print("[*] The login to the Mediawiki server was successfull")

    return session


if __name__ == "__main__":
    
    # disable ssl warnings on stdout
    disable_warnings()
    
    pagenames = getPagenames(DATABASE_HOSTNAME, getenv("MEDIAWIKI_DB_USER"), getenv("MEDIAWIKI_DB_PASS"), DATABASE_NAME)

    session = getMediawikiSession(MEDIAWIKI_API_URL, getenv("MEDIAWIKI_LOGIN_USER"), getenv("MEDIAWIKI_LOGIN_PASS"))

    if not path.exists(OUTPUT_FOLDER_DOCX):
        mkdir(OUTPUT_FOLDER_DOCX)       
        print(f"[*] We created your output directory on { OUTPUT_FOLDER_DOCX }")
 
    else:
        print(f"[*] We found your output directory, please be sure that this folder not contains previous files")


    # for each pagename fetch the html code, remove headers, footers, change the image path and thumbnail to full picture
    for __htmlpageTitle in pagenames:
        
        # build url for fetch the html
        htmlUrl = f"{ MEDIAWIKI_INDEX_URL }?title={ __htmlpageTitle }"

        # remove the "/" in filename, cause it would try to get in the next folder
        filename = f"{ OUTPUT_FOLDER_DOCX }{ __htmlpageTitle.replace('/', '_') }.docx" 

        # call url to get the html
        response = session.get(url=htmlUrl, verify=False)

        # set right endpoint for mediawiki directory
        htmlpage_content = response.text.replace(MEDIAWIKI_URI, MEDIAWIKI_UNIX_PATH)

        # parse to BeautifulSoup
        soup = BeautifulSoup(htmlpage_content, 'html.parser')

        # edit fields next to headlines
        for __editsection in soup.find_all("span", {'class':'mw-editsection'}):
            __editsection.decompose() #remove

        # footer remove
        for __navigation in soup.find_all("div", {"id": "mw-navigation"}):
            __navigation.decompose() #remove

        # footer remove
        for __footer in soup.find_all("footer", {"class": "mw-footer"}):
            __footer.decompose() #remove

        # footer remove
        for __footersyslog in soup.find_all("div", {"class": "syslogfooter"}):
            __footersyslog.decompose() #remove

        # footer remove
        for __categorylinks in soup.find_all("div", {"class": "catlinks"}):
            __categorylinks.decompose() #remove

        # header remove
        for __jumpLinks in soup.find_all("a", {"class": "mw-jump-link"}):
            __jumpLinks.decompose() #remove

        # header remove
        for __siteName in soup.find_all("div", {"id": "siteSub"}):
            __siteName.decompose() #remove
        
        # change the thumb to full picture
        for __picturepath in soup.find_all("img"):
            __pictureSrc = __picturepath["src"]

            if "/thumb" in __pictureSrc:

                # remove the thumb folder from uri
                __pictureSrc = __pictureSrc.replace("/thumb", "")
                
                # remove the last uri path parameter
                __pictureSrc = "/".join(__pictureSrc.split("/")[:-1])

                # save the src tag to the new manipulated pictureSrc
                __picturepath["src"] = __pictureSrc
    
        
            # check if the prev. generated filename is not empty
            if filename == ".docx":
                print("[-] Pagename is empty, and will not be created.")
                continue

            # check for a specific string in the parsed html, check if a login is required
            if 'Special:Badtitle' in str(soup):
                print("[-] Special:Badtitle is in the html maybe you need to login.")
                continue

        try:
            output = convert_text(source = str(soup) , format='html', to='docx', outputfile=filename, extra_args=["+RTS", "-K64m", "-RTS"])
            print(f"[+] {filename}")  
        
        except Exception as e:
            print(f"[-] {filename}: {e}")

    
