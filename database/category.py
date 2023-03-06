categorySql = ''' DROP TABLE IF EXISTS categories CASCADE;
 CREATE TABLE categories (
 ID SERIAL PRIMARY KEY NOT NULL,
 CATEGORY text NOT NULL UNIQUE,
 IS_CUSTOM BOOLEAN
 )
 ''';

categoryFill = ''' INSERT INTO categories (CATEGORY, IS_CUSTOM) 
 VALUES('sport', FALSE);'''