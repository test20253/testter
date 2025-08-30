from Tests.resources.constants.api.artemis.ArtemisConstants import ArtemisConstants


class ArtemisEndpoints:

    @staticmethod
    def ARTEMIS_MAPS_ENDPOINT():
        return ArtemisConstants.ARTEMIS_MAPS_ENDPOINT

    @staticmethod
    def ARTEMIS_MAPS_MAPID_GROUPS_ENDPOINT(map_id):
        return ArtemisConstants.ARTEMIS_MAPS_MAPID_GROUPS_ENDPOINT.format(map_id=map_id)

    @staticmethod
    def ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_TRANSLATE_ENDPOINT(translated_map_id,translated_group_id):
        return ArtemisConstants.ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_TRANSLATE_ENDPOINT.format(translated_map_id=translated_map_id,translated_group_id=translated_group_id)

    @staticmethod
    def ARTEMIS_APPROVALS_ENDPOINT():
        return ArtemisConstants.ARTEMIS_APPROVALS_ENDPOINT

    @staticmethod
    def ARTEMIS_ENTITY_STATUS_ENDPOINT():
        return ArtemisConstants.ARTEMIS_ENTITY_STATUS_ENDPOINT

    @staticmethod
    def ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ITEM_ENDPOINT(map_id, group_id):
        return ArtemisConstants.ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ITEM_ENDPOINT.format(map_id=map_id, group_id=group_id)

    @staticmethod
    def ARTEMIS_MAPS_MAPID_ITEMS_ENDPOINT(map_id):
        return ArtemisConstants.ARTEMIS_MAPS_MAPID_ITEMS_ENDPOINT.format(map_id=map_id)

    @staticmethod
    def ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ENDPOINT(map_id, group_id):
        return ArtemisConstants.ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ENDPOINT.format(map_id=map_id, group_id=group_id)

    @staticmethod
    def ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ITEM_ITEMID_ENDPOINT(map_id, group_id, item_id):
        return ArtemisConstants.ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ITEM_ITEMID_ENDPOINT.format(map_id=map_id, group_id=group_id, item_id=item_id)

    @staticmethod
    def ARTEMIS_MAP_ITEM_ID_TRANSLATE_ENDPOINT(translated_map_id, translated_group_id, translated_item_id):
        return ArtemisConstants.ARTEMIS_MAP_ITEM_ID_TRANSLATE_ENDPOINT.format(translated_map_id=translated_map_id,translated_group_id=translated_group_id,translated_item_id=translated_item_id)

    @staticmethod
    def ARTEMIS_ITEMS_PROFILE_EXCLUSION_ENDPOINT(item_id):
        return ArtemisConstants.ARTEMIS_ITEMS_PROFILE_EXCLUSION_ENDPOINT.format(item_id=item_id)

    @staticmethod
    def ARTEMIS_MAPS_ITEMS_GET_PROFILE_QUESTION_ENDPOINT():
        return ArtemisConstants.ARTEMIS_MAPS_ITEMS_GET_PROFILE_QUESTION

    @staticmethod
    def ARTEMIS_MAP_ITEM_FORM_CLICK_EVENT_ENDPOINT():
        return ArtemisConstants.ARTEMIS_MAP_ITEM_FORM_CLICK_EVENT_ENDPOINT

    @staticmethod
    def ARTEMIS_MAP_ITEM_TASK_CLICK_EVENT_ENDPOINT():
        return ArtemisConstants.ARTEMIS_MAP_ITEM_TASK_CLICK_EVENT_ENDPOINT

    @staticmethod
    def ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ITEM_ITEMID_EVENT_ENDPOINT(map_id, group_id, item_id):
        return ArtemisConstants.ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ITEM_ITEMID_EVENT_ENDPOINT.format(map_id=map_id,
                                                                                                    group_id=group_id,
                                                                                                    item_id=item_id)
    @staticmethod
    def ARTEMIS_EDIT_MAP_ITEM_PROFILE_INCLUSION_ENDPOINT(item_id):
        return ArtemisConstants.ARTEMIS_EDIT_MAP_ITEM_PROFILE_INCLUSION_ENDPOINT.format(item_id=item_id)

    @staticmethod
    def ARTEMIS_MAP_MAP_GROUPS_DELETE_TRANSLATION_ENDPOINT(translated_map_id,translated_group_id, translation_id):
        return ArtemisConstants.ARTEMIS_MAP_MAP_GROUPS_DELETE_TRANSLATION_ENDPOINT.format(translated_map_id=translated_map_id,
                                                                                            translated_group_id=translated_group_id,
                                                                                            translation_id=translation_id)
    @staticmethod
    def ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ITEM_ITEMID_EVENT_EVENTID_ENDPOINT(map_id, group_id, item_id, event_id):
        return ArtemisConstants.ARTEMIS_MAPS_MAPID_GROUPS_GROUPID_ITEM_ITEMID_EVENT_EVENTID_ENDPOINT.format(map_id=map_id, group_id=group_id,
                                                                                                            item_id=item_id, event_id=event_id)
    @staticmethod
    def ARTEMIS_DELETE_MAP_ITEM_ID_TRANSLATE_ENDPOINT (translated_map_id, translated_group_id, translated_item_id, translation_id):
        return ArtemisConstants.ARTEMIS_DELETE_MAP_ITEM_ID_TRANSLATE_ENDPOINT.format(translated_map_id=translated_map_id,
                                                                                     translated_group_id=translated_group_id,
                                                                                     translated_item_id=translated_item_id,
                                                                                     translation_id=translation_id)
    @staticmethod
    def ARTEMIS_MAPS_MAPID_ENDPOINT(map_id):
        return ArtemisConstants.ARTEMIS_MAPS_MAPID_ENDPOINT.format(map_id=map_id)


    @staticmethod
    def ARTEMIS_CHANNELS_ID_ENDPOINT(id):
        return ArtemisConstants.ARTEMIS_CHANNELS_ID_ENDPOINT.format(id=id)

    @staticmethod
    def ARTEMIS_CHANNELS_ENDPOINT():
        return ArtemisConstants.ARTEMIS_CHANNELS_ENDPOINT

    @staticmethod
    def ARTEMIS_CHANNELLANGUAGES_ID_ENDPOINT(id):
        return ArtemisConstants.ARTEMIS_CHANNELLANGUAGES_ID_ENDPOINT.format(id=id)

    @staticmethod
    def ARTEMIS_CHANNELLANGUAGES_ENDPOINT():
        return ArtemisConstants.ARTEMIS_CHANNELLANGUAGES_ID_ENDPOINT

    @staticmethod
    def ARTEMIS_LANGUAGES_ID_ENDPOINT(id):
        return ArtemisConstants.ARTEMIS_LANGUAGES_ID_ENDPOINT.format(id=id)

    @staticmethod
    def ARTEMIS_LANGUAGES_ENDPOINT():
        return ArtemisConstants.ARTEMIS_LANGUAGES_ENDPOINT

    @staticmethod
    def ARTEMIS_SERVICELINEORGANIZATIONS_ID_ENDPOINT(id):
        return ArtemisConstants.ARTEMIS_SERVICELINEORGANIZATIONS_ID_ENDPOINT.format(id=id)

    @staticmethod
    def ARTEMIS_SERVICELINEORGANIZATIONS_ENDPOINT():
        return ArtemisConstants.ARTEMIS_SERVICELINEORGANIZATIONS_ENDPOINT

    @staticmethod
    def ARTEMIS_ROLES_ID_ENDPOINT(id):
        return ArtemisConstants.ARTEMIS_ROLES_ID_ENDPOINT.format(id=id)

    @staticmethod
    def ARTEMIS_ROLES_ENDPOINT():
        return ArtemisConstants.ARTEMIS_ROLES_ENDPOINT

    @staticmethod
    def ARTEMIS_SERVICEMODULEORGANIZATIONS_ID_ENDPOINT(id):
        return ArtemisConstants.ARTEMIS_SERVICEMODULEORGANIZATIONS_ID_ENDPOINT.format(id=id)

    @staticmethod
    def ARTEMIS_SERVICEMODULEORGANIZATIONS_ENDPOINT():
        return ArtemisConstants.ARTEMIS_SERVICEMODULEORGANIZATIONS_ENDPOINT

    @staticmethod
    def ARTEMIS_SERVICELINES_ID_ENDPOINT(id):
        return ArtemisConstants.ARTEMIS_SERVICELINES_ID_ENDPOINT.format(id=id)

    @staticmethod
    def ARTEMIS_SERVICELINES_ENDPOINT():
        return ArtemisConstants.ARTEMIS_SERVICELINES_ENDPOINT

    @staticmethod
    def ARTEMIS_SERVICEMODULES_ID_ENDPOINT(id):
        return ArtemisConstants.ARTEMIS_SERVICEMODULES_ID_ENDPOINT.format(id=id)

    @staticmethod
    def ARTEMIS_SERVICEMODULES_ENDPOINT():
        return ArtemisConstants.ARTEMIS_SERVICEMODULES_ENDPOINT

    @staticmethod
    def ARTEMIS_SERVICEORGANIZATIONS_ID_ENDPOINT(id):
        return ArtemisConstants.ARTEMIS_SERVICEORGANIZATIONS_ID_ENDPOINT.format(id=id)

    @staticmethod
    def ARTEMIS_SERVICEORGANIZATIONS_ENDPOINT():
        return ArtemisConstants.ARTEMIS_SERVICEORGANIZATIONS_ENDPOINT

    @staticmethod
    def ARTEMIS_USERROLES_ENDPOINT():
        return ArtemisConstants.ARTEMIS_USERROLES_ENDPOINT

    @staticmethod
    def ARTEMIS_MAPS_USERS_ME_ENDPOINT():
        return ArtemisConstants.ARTEMIS_MAPS_USERS_ME_ENDPOINT

    @staticmethod
    def ARTEMIS_MAPS_AUDITPHASES_ENDPOINT():
        return ArtemisConstants.ARTEMIS_MAPS_AUDITPHASES_ENDPOINT

    @staticmethod
    def ARTEMIS_MAPS_MAPDISPLAYTYPES_ENDPOINT():
        return ArtemisConstants.ARTEMIS_MAPS_MAPDISPLAYTYPES_ENDPOINT

    @staticmethod
    def ARTEMIS_FORMS_FORMID_SECTIONS_ENDPOINT(form_id):
        return ArtemisConstants.ARTEMIS_FORMS_FORMID_SECTIONS_ENDPOINT.format(form_id=form_id)

    @staticmethod
    def ARTEMIS_FORMS_FORMID_HEADERS_ENDPOINT(form_id):
        return ArtemisConstants.ARTEMIS_FORMS_FORMID_HEADERS_ENDPOINT.format(form_id=form_id)

    @staticmethod
    def ARTEMIS_FORMS_FORMID_BODIES_ENDPOINT(form_id):
        return ArtemisConstants.ARTEMIS_FORMS_FORMID_BODIES_ENDPOINT.format(form_id=form_id)

    @staticmethod
    def ARTEMIS_FORMS_ENDPOINT():
        return ArtemisConstants.ARTEMIS_FORMS_ENDPOINT

    @staticmethod
    def ARTEMIS_TASKS_ENDPOINT():
        return ArtemisConstants.ARTEMIS_TASKS_ENDPOINT
        
