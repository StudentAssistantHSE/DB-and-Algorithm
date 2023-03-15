recommendationSql = ''' DROP TABLE IF EXISTS user_recommendations CASCADE;
CREATE TABLE user_recommendations (
  ID SERIAL PRIMARY KEY NOT NULL,
  user_id int NOT NULL,
  project_id int NOT NULL,
  generated_date Date DEFAULT CURRENT_DATE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE,
  FOREIGN KEY (project_id) REFERENCES projects(id) ON UPDATE CASCADE
);
 ''';