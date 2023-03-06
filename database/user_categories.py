accountInterestsSql = ''' DROP TABLE IF EXISTS user_categories CASCADE;
CREATE TABLE user_categories (
  user_id int NOT NULL,
  category_id int NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE,
  FOREIGN KEY (category_id) REFERENCES categories(id) ON UPDATE CASCADE,
  PRIMARY KEY (user_id, category_id)
);
 ''';

accountInterestsFill = ''' INSERT INTO user_categories (user_id, category_id) 
 VALUES((SELECT id from users WHERE ID='1'), (SELECT id from categories WHERE ID='1'));'''