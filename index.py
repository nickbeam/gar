from datetime import datetime

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, \
        DB_SCHEMA, XSD_DIRECTORY, XML_DIRECTORY, REGION_CODE
from connection import connectToDB
from parseXSD import parseXsd
from createPgTables import createPgTables
from fillPgTables import fillPgTables
from createFunctions import createFunctions
from createIndexes import createIndexes
from validateXML import batchValidation

(connection, cursor) = connectToDB(
  DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

cursor.execute("CREATE SCHEMA IF NOT EXISTS {schema};" \
    .format(schema=DB_SCHEMA))
print('--- Создана схема {schema} ---'.format(schema=DB_SCHEMA))

parsedXSD = parseXsd(XSD_DIRECTORY)
"""
validation = batchValidation(XML_DIRECTORY, XSD_DIRECTORY, REGION_CODE)
for file in validation:
    if file['IsValid'] is False:
        print('\t' + file['File'] + '\t' + str(file['IsValid']))
"""
createPgTables(parsedXSD, connection, cursor, DB_SCHEMA)

for CUR_REGION_CODE in REGION_CODE:
    print("==========", datetime.now(), " Начало загрузки региона: ", CUR_REGION_CODE, "==========")
    fillPgTables(XML_DIRECTORY, cursor, connection, DB_SCHEMA, CUR_REGION_CODE)
    print("==========", datetime.now(), " Конец загрузки региона: ", CUR_REGION_CODE, "==========")

createFunctions(connection, cursor, DB_SCHEMA)

createIndexes(parsedXSD, connection, cursor, DB_SCHEMA)

connection.close()