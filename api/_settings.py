import os

ROOTPATH = os.path.abspath('.')
LOGFILEPATH = os.path.join(ROOTPATH, 'site.log')

########################
ENVIRONMENT = 'dev' 
#ENVIRONMENT = 'production' 

if '/iamcm' in ROOTPATH:
    ENVIRONMENT = 'production'
########################

# Is this a persistent session or a 'this session only' session
SESSIONISPERSISTENT = True
# The duration of the session in hours
SESSIONDURATION = 24 * 7 #1 week

# salt
SALT = '<salt>'

# Write all database commands to the site log
DBDEBUG = False

if ENVIRONMENT=='dev': 
    BASEURL = 'http://localhost:8080'    
        
    APPHOST = '0.0.0.0'
    APPPORT = 8080
    
    DBNAME = 'Site'
    DBHOST = 'localhost'
    DBPORT = 27017
    
    EMAILHOST = '127.0.0.1'
    #EMAILUSERNAME = ''
    #EMAILPASSWORD = ''
    EMAILSENDER = 'Dev site <noreply@localhost>'
    EMAILRECIPIENT = 'site@email.com'
    
    USERFILESPATH = ROOTPATH +'/userfiles/'
    
    FACEBOOK_APP_ID = ''
    FACEBOOK_APP_SECRET = ''
    
    DEBUG = True
    
    SERVER = 'wsgiref'

    PROVIDE_STATIC_FILES = True
    
elif ENVIRONMENT=='beta':
    BASEURL = 'http://beta.site.co.uk'    
        
    APPHOST = '127.0.0.1'
    APPPORT = 30234
    
    DBNAME = 'SiteBeta'
    DBHOST = 'localhost'
    DBPORT = 35572
    
    EMAILHOST = ''
    EMAILUSERNAME = ''
    EMAILPASSWORD = ''
    EMAILSENDER = ''
    EMAILRECIPIENT = ''
    
    USERFILESPATH = ROOTPATH +'/userfiles/'
    
    FACEBOOK_APP_ID = ''
    FACEBOOK_APP_SECRET = ''
    
    DEBUG = False
    
    SERVER = 'paste'

    PROVIDE_STATIC_FILES = True
    
elif ENVIRONMENT=='production':
    BASEURL = 'http://site.co.uk'    
        
    APPHOST = '127.0.0.1'
    APPPORT = 30800
    
    DBNAME = 'Site'
    DBHOST = 'localhost'
    DBPORT = 35572
    
    EMAILHOST = ''
    EMAILUSERNAME = ''
    EMAILPASSWORD = ''
    EMAILSENDER = ''
    EMAILRECIPIENT = ''
    
    USERFILESPATH = ROOTPATH +'/userfiles/'
    
    FACEBOOK_APP_ID = ''
    FACEBOOK_APP_SECRET = ''
    
    DEBUG = False
    
    SERVER = 'paste'

    PROVIDE_STATIC_FILES = True
