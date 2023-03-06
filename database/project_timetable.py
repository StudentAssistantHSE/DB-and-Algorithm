projectTimetableSql = ''' DROP TABLE IF EXISTS projects_timetable CASCADE;
 CREATE TABLE projects_timetable (
 ID SERIAL PRIMARY KEY NOT NULL,
 PROJECT_ID BIGINT REFERENCES PROJECTS,
 DEADLINE DATE NOT NULL,
 NAME text NOT NULL,
 DESCRIPTION text
 )
 ''';

projectTimetableFill = ''' INSERT INTO projects_timetable (PROJECT_ID, DEADLINE, NAME)
 VALUES((SELECT id from projects WHERE ID='1'), '2022-05-15', 'NAme')'''