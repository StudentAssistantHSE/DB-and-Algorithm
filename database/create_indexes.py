createIndexes = ''' 
create index on projects(creator_user_id);
create index on applications(applicant_id);
create index on applications(project_id);
create index on applications(status);
create index on user_categories(category_id);
create index on project_categories(category_id);
'''