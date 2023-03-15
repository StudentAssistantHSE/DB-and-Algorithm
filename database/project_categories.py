projectCategoriesSql = ''' DROP TABLE IF EXISTS project_categories CASCADE;
CREATE TABLE project_categories (
  ID SERIAL PRIMARY KEY NOT NULL,
  project_id int NOT NULL,
  category_id int NOT NULL,
  UNIQUE(project_id, category_id),
  FOREIGN KEY (project_id) REFERENCES projects(id) ON UPDATE CASCADE,
  FOREIGN KEY (category_id) REFERENCES categories(id) ON UPDATE CASCADE
);
 ''';

projectCategoriesFill = ''' INSERT INTO project_categories (project_id, category_id) 
 VALUES((SELECT id from projects WHERE ID='1'), (SELECT id from categories WHERE ID='1'));'''