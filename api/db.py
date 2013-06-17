from pymongo import Connection
import settings

conn = Connection(settings.DBHOST, settings.DBPORT)

_DBCON = eval('conn.'+ settings.DBNAME)


