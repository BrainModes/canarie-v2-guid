TABLENAME=hdpzip
psql -U ftptest -a -h localhost -d ftpprov -c\
 "CREATE TABLE ${TABLENAME}(KEY TEXT PRIMARY KEY NOT NULL, VALUE TEXT UNIQUE  NOT NULL );"
