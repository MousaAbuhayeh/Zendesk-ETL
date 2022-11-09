
#sql server
native_client ='SQL Server Native Client 11.0'
sql_server = 'eqdb04z.database.windows.net'
database = 'BI-WORKSPACE'
database_uid = 'naljuaidi'
database_pwd = '5CoxmlDDeq'


#zendesk api
zendesk_user = 'nahed.aljuaidi@equiti.com' + '/token'
zendesk_pwd = '8swd2AbpTKhp0GbMMozjwkYnbxsMwYrquUgJxaru'

#key lists
ticket_fields_key_list = ["id","title"]


#column_strs
ticket_fields_column_str = '"id","field_name"'

#mapping urls,table_names,columns_Str,value_lists
map_url_list = ['https://equiti-helpdesk.zendesk.com/api/v2/ticket_fields.json?per_page=100','https://equiti-helpdesk.zendesk.com/api/v2/groups.json?per_page=100','https://equiti-helpdesk.zendesk.com/api/v2/incremental/users.json?per_page=1000&start_time=1667779200']
main_key_list = ['ticket_fields','groups','users']
table_name_list = ['zen_ticket_fields','zen_groups','zen_users']
column_str_list = ['"id","field_name"','"id","is_public","name","description","default","deleted","created_at","updated_at"','"id","name","email","created_at","updated_at","time_zone","iana_time_zone","role","verified","active","last_login_at","two_factor_auth_enabled","custom_role_id","restricted_agent","suspended","default_group_id"']
fields_list_list = [["id","title"],["id","is_public","name","description","default","deleted","created_at","updated_at"],["id","name","email","created_at","updated_at","time_zone","iana_time_zone","role","verified","active","last_login_at","two_factor_auth_enabled","custom_role_id","restricted_agent","suspended","default_group_id"]]

#tickets info
#circle through in order ticket>cia>lists>satisfaction[
tickets_fields_list_ticket = ["id","external_id","created_at","updated_at","type","subject","raw_subject","description","priority","status","recipient","requester_id","submitter_id","assignee_id","organization_id","group_id","forum_topic_id","problem_id","has_incidents","is_public","due_at","sharing_agreement_ids","custom_status_id","comment_count","followup_ids","ticket_form_id","brand_id","allow_channelback","allow_attachments","generated_timestamp"]
tickets_fields_list_via_satisfaction = [('via','channel'),('via','source','from','address'),('via','source','from','name'),('via','source','from','ticket_id'),('via','source','from','subject'),('via','source','from','channel'),('via','source','to','name'),('via','source','to','address'),('via','source','rel'),('satisfaction_rating','score'),('satisfaction_rating','id'),('satisfaction_rating','comment'),('satisfaction_rating','reason'),('satisfaction_rating','reason_id')]
tickets_fields_list_lists = ["collaborator_ids","follower_ids","email_cc_ids","tags"]

#]
tickets_columns_str = '"id","external_id","created_at","updated_at","type","subject","raw_subject","description","priority","status","recipient","requester_id","submitter_id","assignee_id","organization_id","group_id","forum_topic_id","problem_id","has_incidents","is_public","due_at","sharing_agreement_ids","custom_status_id","comment_count","followup_ids","ticket_form_id","brand_id","allow_channelback","allow_attachments","generated_timestamp","via_channel","via_source_from_address","via_source_from_name","via_source_from_ticket_id","via_source_from_subject","via_source_from_channel","via_source_to_name","via_source_to_address","via_source_rel","satisfaction_rating_score","satisfaction_rating_id","satisfaction_rating_comment","satisfaction_rating_reason","satisfaction_rating_reason_id","collaborator_ids","follower_ids","email_cc_ids","tags"'

metric_sets_fields_list=["id","ticket_id","created_at","updated_at","group_stations","assignee_stations","reopens","replies","assignee_updated_at","requester_updated_at","status_updated_at","initially_assigned_at","assigned_at","solved_at","latest_comment_added_at","reply_time_in_minutes","first_resolution_time_in_minutes","full_resolution_time_in_minutes","agent_wait_time_in_minutes","requester_wait_time_in_minutes","on_hold_time_in_minutes"]
metric_sets_columns_str = '"id","ticket_id","created_at","updated_at","group_stations","assignee_stations","reopens","replies","assignee_updated_at","requester_updated_at","status_updated_at","initially_assigned_at","assigned_at","solved_at","latest_comment_added_at","reply_time_in_minutes_calendar","reply_time_in_minutes_business","first_resolution_time_in_minutes_calendar","first_resolution_time_in_minutes_business","full_resolution_time_in_minutes_calendar","full_resolution_time_in_minutes_business","agent_wait_time_in_minutes_calendar","agent_wait_time_in_minutes_business","requester_wait_time_in_minutes_calendar","requester_wait_time_in_minutes_business","on_hold_time_in_minutes_calendar","on_hold_time_in_minutes_business","reply_time_in_seconds_calendar"'

