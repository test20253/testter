class ArtemisConstants():
   """
   https://eycgv2-api-dev2.euw.cloudapp.eydev.net/swagger/index.html
   """

   #Approvals
   ARTEMIS_APPROVALS_ENDPOINT = '/api/Approvals'

   #Bodies
   ARTEMIS_FORMS_FORMID_BODIES_ENDPOINT = '/api/Forms/{form_id}/Bodies'

   #ChannelLanguages
   ARTEMIS_CHANNELLANGUAGES_ENDPOINT = '/api/ChannelLanguages'
   ARTEMIS_CHANNELLANGUAGES_ID_ENDPOINT = '/api/ChannelLanguages/{id}'
   
   #Channels
   ARTEMIS_CHANNELS_ENDPOINT = '/api/Channels'
   ARTEMIS_CHANNELS_ID_ENDPOINT = '/api/Channels/{id}'

   #Forms
   ARTEMIS_FORMS_ENDPOINT = '/api/Forms'

   #Headers
   ARTEMIS_FORMS_FORMID_HEADERS_ENDPOINT = '/api/Forms/{form_id}/Headers'

   #Languages
   ARTEMIS_LANGUAGES_ENDPOINT = '/api/Languages'
   ARTEMIS_LANGUAGES_ID_ENDPOINT = '/api/Languages/{id}'

   # MAPS
   ARTEMIS_MAPS_ENDPOINT = '/api/Maps'
   ARTEMIS_ENTITY_STATUS_ENDPOINT='/api/EntityStatus'
   ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ENDPOINT = '/api/Maps/{map_id}/Groups/{group_id}'
   ARTEMIS_MAPS_MAPID_GROUPS_ENDPOINT = '/api/Maps/{map_id}/Groups'
   ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_TRANSLATE_ENDPOINT = '/api/Maps/{translated_map_id}/Groups/{translated_group_id}/Translate'
   ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ITEM_ENDPOINT = '/api/Maps/{map_id}/Groups/{group_id}/Item'
   ARTEMIS_MAPS_MAPID_ITEMS_ENDPOINT = '/api/Maps/{map_id}/Items'
   ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ITEM_ITEMID_ENDPOINT = '/api/Maps/{map_id}/Groups/{group_id}/Items/{item_id}'
   ARTEMIS_MAP_ITEM_ID_TRANSLATE_ENDPOINT = '/api/Maps/{translated_map_id}/Groups/{translated_group_id}/Items/{translated_item_id}/Translate'
   ARTEMIS_ITEMS_PROFILE_EXCLUSION_ENDPOINT = '/api/Items/{item_id}/ProfileAnswerExclusions'
   ARTEMIS_MAPS_ITEMS_GET_PROFILE_QUESTION = '/api/Questions?'
   ARTEMIS_EDIT_MAP_ITEM_PROFILE_INCLUSION_ENDPOINT = '/api/Items/{item_id}/ProfileAnswerInclusions'
   ARTEMIS_MAP_ITEM_TASK_CLICK_EVENT_ENDPOINT = '/api/Tasks'
   ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ITEM_ITEMID_EVENT_ENDPOINT = '/api/Maps/{map_id}/Groups/{group_id}/Item/{item_id}/Event'
   ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ITEM_ITEMID_EVENT_EVENTID_ENDPOINT = '/api/Maps/{map_id}/Groups/{group_id}/Item/{item_id}/Event/{event_id}'
   ARTEMIS_MAP_MAP_GROUPS_DELETE_TRANSLATION_ENDPOINT = '/api/Maps/{translated_map_id}/Groups/{translated_group_id}/Translate/{translation_id}'
   ARTEMIS_MAPS_MAPID_ENDPOINT = '/api/Maps/{map_id}'
   ARTEMIS_MAPS_USERS_ME_ENDPOINT = '/api/Users/Me'
   ARTEMIS_MAPS_AUDITPHASES_ENDPOINT = '/api/AuditPhases'
   ARTEMIS_MAPS_MAPDISPLAYTYPES_ENDPOINT = '/api/MapDisplayTypes'

   #Roles
   ARTEMIS_ROLES_ENDPOINT = '/api/Roles'
   ARTEMIS_ROLES_ID_ENDPOINT = '/api/Roles/{id}'

   #Sections
   ARTEMIS_FORMS_FORMID_SECTIONS_ENDPOINT = '/api/Forms/{form_id}/Sections'

   #ServiceLineOrganizations
   ARTEMIS_SERVICELINEORGANIZATIONS_ENDPOINT = '/api/ServiceLineOrganizations'
   ARTEMIS_SERVICELINEORGANIZATIONS_ID_ENDPOINT = '/api/ServiceLineOrganizations/{id}'

   #ServiceLines
   ARTEMIS_SERVICELINES_ENDPOINT = '/api/ServiceLines'
   ARTEMIS_SERVICELINES_ID_ENDPOINT = '/api/ServiceLines/{id}'

   #ServiceModuleOrganizations
   ARTEMIS_SERVICEMODULEORGANIZATIONS_ENDPOINT = '/api/ServiceModuleOrganizations'
   ARTEMIS_SERVICEMODULEORGANIZATIONS_ID_ENDPOINT = '/api/ServiceModuleOrganizations/{id}'

   #ServiceModuleRoles
   ARTEMIS_SERVICEMODULEROLES_ENDPOINT = '/api/ServiceModuleRoles'
   ARTEMIS_SERVICEMODULEROLES_ID_ENDPOINT = '/api/ServiceModuleRoles/{id}'

   #ServiceModules
   ARTEMIS_SERVICEMODULES_ENDPOINT = '/api/ServiceModules'
   ARTEMIS_SERVICEMODULES_ID_ENDPOINT = '/api/ServiceModules/{id}'

   #ServiceOrganizations
   ARTEMIS_SERVICEORGANIZATIONS_ENDPOINT = '/api/ServiceOrganizations'
   ARTEMIS_SERVICEORGANIZATIONS_ID_ENDPOINT = '/api/ServiceOrganizations/{id}'
   
   #UserRoles
   ARTEMIS_USERROLES_ENDPOINT = '/api/UserRoles'

   #Items
   ARTEMIS_DELETE_MAP_ITEM_ID_TRANSLATE_ENDPOINT = '/api/Maps/{translated_map_id}/Groups/{translated_group_id}/Items/{translated_item_id}/Translate/{translation_id}'

  # Canvas Tasks
   ARTEMIS_TASKS_ENDPOINT = '/api/Tasks?'
