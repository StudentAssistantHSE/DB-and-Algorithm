statusSql = ''' DROP TABLE IF EXISTS statuses CASCADE;
 CREATE TABLE statuses (
 ID SERIAL PRIMARY KEY NOT NULL,
 STATUS text NOT NULL UNIQUE
 )
 ''';

statusFill = ''' INSERT INTO statuses (STATUS)
 VALUES('SENT'), ('REJECTED'), ('ACCEPTED');
 ''';