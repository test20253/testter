class Endpoints():
    def __init__(self):
        # API_Canvas_Forms
        self._SEARCH_FORM_ENDPOINT = '/api/v1/Forms?'
        self._GET_USER_ROLES_FOR_USER = '/api/v1/UserRoles/roles/{user_id}?'
        self._CREATE_FORM_ENDPOINT = '/api/v1/forms'
        self._ADD_HEADER_TO_FORM = '/api/v1/headers'
        self._GET_HEADER_TO_FORM = '/api/v1/Headers?'
        self._ADD_SECTION_TO_HEADER = '/api/v1/Sections'
        self._ADD_BODY_TO_SECTION = '/api/v1/Bodies'
        self._DELETE_FORM_BODY = '/api/v1/Bodies/{body_id}?'
        self._LOCALIZE_HEADER_FOR_FORM = '/api/v1/headers/{header_id}'
        self._SEARCH_SECTION_ENDPOINT = '/api/v1/Sections/{section_id}?'
        self._TRANSLATE_SECTION = '/api/v1/Sections/Translate'
        self._SELECT_RELATED_OBJECT = '/api/v1/Entity'
        self._SELECT_FORM_DOCUMENT_TYPE = '/api/v1/CanvasDocumentType'
        self._SELECT_RELATED_OBJECT_HIERARCHY = '/api/v1/EntityObject/Entity/{entity_id}'
        self._GET_CANVAS_FORMS = '/api/v1/forms/{form_id}?'
        self._APPROVE_FORM_ENTITY = '/api/v1/FormApproval'
        self._TRANSLATE_FORM = '/api/v1/forms/Translate'
        self._TRANSLATE_HEADER = '/api/v1/headers/translate'
        self._SUMMARY_TYPE = '/api/v1/SummaryType'
        self._CARD_TYPE = '/api/v1/CardType'
        self._GET_BODY_INFO = '/api/v1/Bodies/{body_id}?'
        self._TRANSLATE_BODY = '/api/v1/Bodies/Translate'
        self._ADD_FORM_ATLAS_GUIDANCE = '/api/v1/Guidance'
        self._TRANSLATE_BODY_OPTION = '/api/v1/BodyOptionsTranslate/{bodyOptionContentId}'
        self._TRANSLATE_BODY_GUIDANCE = '/api/v1/GuidanceTranslate'
        self._UPDATE_FORM = '/api/v1/forms/{form_id}'
        self._UPDATE_SECTION_TO_HEADER = '/api/v1/Sections/{section_id}'
        self._GET_BODY_RESPONSE = '/api/v1/Bodies?'
        self._DELETE_HEADER = '/api/v1/headers/{header_id}?'
        self._GET_FORM_PROFILE_QUESTIONS = '/api/v1/Questions?'
        self._ADD_ANSWER_TO_FORM_PROFILE_QUESTION = '/api/v1/Body/{body_id}/ProfileAnswer'
        self._EXCLUSION_ANSWER_FROM_FORM_PROFILE_QUESTION = '/api/v1/Body/{body_id}/ProfileAnswerExclusion'
        self._UPDATE_BODYOPTION = '/api/v1/Bodies/{body_id}'
        self._ADD_NESTED_BODIES = '/api/v1/Bodies/{body_id}/NestedBodies'
        self._ADD_LINEAGE_TO_BODY = '/api/v1/Forms/{form_id}/Bodies/{body_id}/BodyLineage/?'
        self._GET_BODY_TYPE = '/api/v1/BodyTypes'
        self._ADD_ANSWER_TO_SECTION_PROFILE_QUESTION = '/api/v1/Sections/{section_id}/ProfileAnswer'
        self._EXCLUSION_ANSWER_FROM_SECTION_PROFILE_QUESTION = '/api/v1/Sections/{section_id}/ProfileAnswerExclusion'
        self._REMOVE_ANSWER_FROM_SECTION_PROFILE_QUESTION = '/api/v1/Sections/{section_id}/ProfileAnswer/{question_id}'
        self._REMOVE_EXCLUDED_ANSWER_FROM_SECTION_PROFILE_QUESTION = '/api/v1/Sections/{section_id}/ProfileAnswerExclusion/{question_id}'
        self._REMOVE_ANSWER_FROM_BODY_PROFILE_QUESTION = '/api/v1/Body/{body_id}/ProfileAnswer/{question_id}'
        self._REMOVE_EXCLUDED_ANSWER_FROM_BODY_PROFILE_QUESTION = '/api/v1/Body/{body_id}/ProfileAnswerExclusion/{question_id}'
        self._ADD_RISK_FACTOR_TO_BODY = '/api/v1/Bodies/{body_id}/BodyOptionActions/{body_action_id}'
        self._GET_BODY_ACTION_TYPE = '/api/v1/BodyActions?'
        self._GET_Materiality_Type = '/api/v1/MaterialityType'
        self._BODY_OPTION_PROFILE_ANSWER_INCLUSION = '/api/v1/Body/{body_id}/BodyOptions/{body_option_id}/ProfileAnswer'
        self._BODY_OPTION_PROFILE_ANSWER_EXCLUSION = '/api/v1/Body/{body_id}/BodyOptions/{body_option_id}/ProfileAnswerExclusion'
        self._REMOVE_BODY_OPTION_PROFILE_ANSWER_INCLUSION = '/api/v1/Body/{body_id}/BodyOptions/{body_option_id}/ProfileAnswer/{inclusion_id}'
        self._REMOVE_BODY_OPTION_PROFILE_ANSWER_EXCLUSION = '/api/v1/Body/{body_id}/BodyOptions/{body_option_id}/ProfileAnswerExclusion/{exclusion_id}'
        self._ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION = '/api/v1/Guidance/{guidance_id}/ProfileAnswer'
        self._ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION = '/api/v1/Guidance/{guidance_id}/ProfileAnswerExclusion'

        # API_Common
        self._SELECT_CHANNEL = '/api/v1/Channels'
        self._SELECT_CHANNEL_LANGUAGE = '/api/v1/ChannelLanguage?'
        self._SELECT_SERVICE_LINE = '/api/v1/ServiceLine'
        self._GET_SERVICE_ORGANIZATION = '/api/v1/ServiceOrganization/Line/1'
        self._GET_PROFILE_QUESTIONS = '/api/v1/Questions?'
        self._GET_ATLAS_GUIDANCE_TYPE = '/api/v1/GuidanceType?'
        self._ADD_CG_USER = '/api/v1/UserRoles'
        self._REVOKE_CG_USER_ROLE = '/api/v1/Users/{user_id}'
        self._REVOKE_CG_USER_ACCESS = '/api/v1/UserRoles?'
        self._CHANNEL_CHILDREN = '/api/v1/Channels/1/children?'
        self._SEARCH_CG_USER = '/api/v1/Users?'
        self._ADD_ATLAS_GUIDANCE = '/api/v1/GroupInstruction/Atlas'
        self._GUIDANCE_SERVICE = '/api/v1/GuidanceService?'
        self._SELECT_SERVICE_LINE_FOR_ALL = '/api/v1/ServiceLine?'
        self._GET_SERVICE_ORGANIZATION_FOR_ALL = '/api/v1/ServiceOrganization?'
        self._GET_ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION_ID = '/api/v1/Guidance/{guidance_id}/DataEntityUId/{data_entity_uid}/DataEntityId/{data_entity_id}/ProfileAnswer?'
        self._GET_ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION_ID = '/api/v1/Guidance/{guidance_id}/DataEntityUId/{data_entity_uid}/DataEntityId/{data_entity_id}/ProfileAnswerExclusion?'
        self._REMOVE_ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION = '/api/v1/Guidance/{guidance_id}/DataEntityUId/{data_entity_uid}/DataEntityId/{data_entity_id}/ProfileAnswer/{inclusion_id}'
        self._REMOVE_ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION = '/api/v1/Guidance/{guidance_id}/DataEntityUId/{data_entity_uid}/DataEntityId/{data_entity_id}/ProfileAnswerExclusion/{exclusion_id}'

        # API_CGGroup_audit_instructions
        self._GET_GROUP_INSTRUCTIONS = '/api/v1/GroupInstruction?'
        self._SEARCH_GROUP_AUDIT_INSTRUCTION = '/api/v1/GroupInstruction/{instruction_id}?'
        self._TRANSLATE_GROUP_INSTRUCTION = '/api/v1/GroupInstructionTranslate/translate'
        self._LOCALIZE_GROUP_INSTRUCTION = '/api/v1/GroupInstructionLocalize/localize'
        self._CREATE_GROUP_INSTRUCTIONS = '/api/v1/GroupInstruction'
        self._GET_GROUP_INSTRUCTION_SCOPE = '/api/v1/GroupInstructionScope?'
        self._GET_GROUP_INSTRUCTION_SECTION = '/api/v1/GroupInstructionSection?'
        self._GET_RECOMMENDATION_TYPE = '/api/v1/RecommendationType'
        self._DELETE_GROUP_INSTRUCTION_TRANSLATE = '/api/v1/GroupInstructionTranslate/{content_id}'
        self._SEARCH_GROUP_AUDIT_INSTRUCTION_ID = '/api/v1/GroupInstruction/{instruction_id}'
        self._SEARCH_GA_INSTRUCTION_PROFILE_QUESTION = '/api/v1/GroupInstructionProfileAnswer/{instruction_id}?'
        self._DELETE_GROUP_INSTRUCTION_LOCALIZE = '/api/v1/GroupInstructionLocalize/{localize_id}'
        self._APPROVE_DELETED_INSTRUCTION = '/api/v1/groupinstruction/approve'
        self._GA_ADD_EVIDENCE = '/api/v1/GroupInstructionEvidence/Evidence'
        self._GA_GUIDANCE_TRANSLATE = '/api/v1/GuidanceTranslate/'
        self._GA_ENTITY_STATUS_PREVIEW = '/api/v1/EntityStatus/entitypreview'
        self._GA_ATLAS_GUIDANCE_PROFILE_INCLUSION = '/api/v1/Guidance/{guidance_id}/ProfileAnswer'
        self._GA_ATLAS_GUIDANCE_PROFILE_EXCLUSION = '/api/v1/Guidance/{guidance_id}/ProfileAnswerExclusion'


        # API_CG_Canvas_Psp_Index
        self._CREATE_PSP_INDEX = '/api/v1/PSPIndex'
        self._GET_METADATA_TAG = '/api/v1/Tag?'
        self._TRANSLATE_PSP_INDEXES = '/api/v1/pspindex/translate/'
        self._GET_PSP_INDEXES_LIST = '/api/v1/pspindex?'
        self._GET_PSP_INDEX = '/api/v1/pspindex/{pspindex_id}?'
        self._SELECT_SERVICE_MODULE = '/api/v1/ServiceModule'
        self._DELETE_PSP_INDEX = '/api/v1/PSPIndex/{psp_index_id}?'
        self._DELETED_PSP_PENDING_APPROVAL = '/api/v1/EntityStatus'
        self._DELETED_PSP_APPROVE = '/api/v1/pSPIndex/approve'
        self._EDIT_PSP_INDEX = '/api/v1/PSPIndex/{psp_index_id}'
        self._ADD_PSP_ATLAS_GUIDANCE = '/api/v1/PSPIndex/Atlas'
        self._MOVE_PSPINDEX = '/api/v1/PSPIndex/{psp_index_id}/MovePSPIndex/?'
        self._PSP_PROFILE_ANSWER = '/api/v1/PSPIndexProfileAnswer/{psp_index_id}'
        self._PSP_LOCALIZED_PROFILE_ANSWER = '/api/v1/PSPIndexProfileAnswer/{psp_index_id}/{channel_id}'
        self._ENTITYPREVIEW_ENDPOINT = '/api/v1/EntityStatus/EntityPreview'
        self._ADD_ANSWER_TO_PSP_PROFILE_QUESTION = '/api/v1/Guidance/{body_id}/ProfileAnswer'
        self._EXCLUSION_ANSWER_FROM_PSP_PROFILE_QUESTION = '/api/v1/Guidance/{body_id}/ProfileAnswerExclusion'

        # API_CG_Tasks
        self._SELECT_TASK_TYPE = '/api/v1/TaskType?'
        self._SELECT_TASK_GROUP = '/api/v1/TaskGroup?'
        self._SELECT_TASK_BUILD_MILESTONE = '/api/v1/TaskBuildMilestone?'
        self._SELECT_TASK_MILESTONE_TYPE = '/api/v1/MilestoneType?'
        self._SELECT_TASK_MULTIENTITY_TYPE = '/api/v1/MultiEntityType?'
        self._CREATE_TASK = '/api/v1/Tasks'
        self._SEARCH_AND_FETCH_TASK_BY_ID = '/api/v1/Tasks/{task_id}?'
        self._DELETE_TASK = '/api/v1/tasks/{task_id}?'
        self._DELETE_ENTITYSTATUS = '/api/v1/EntityStatus'
        self._TASK_APPROVAL = '/api/v1/TaskApproval'
        self._REMOVE_LOCALIZATION_0R_TRANSLATION = '/api/v1/tasks/{task_content_id}?'
        self._SEARCH_AND_FETCH_BY_ID_IN_SEARCH_BOX = '/api/v1/tasks?'
        self._LOCALIZE_TASK = '/api/v1/Tasks/{task_id}/local'
        self._TRANSLATE_CANVAS_TASK = '/api/v1/Tasks/translate/'
        self._GET_PROFILE_QUESTIONS_ANSWERS = '/api/v1/Questions?'
        self._ADD_ANSWER_TO_TASK_PROFILE_QUESTION = '/api/v1/Task/{task_id}/ProfileAnswer'
        self._FETCH_PSP_INDEXES = '/api/v1/PSPIndex?'
        self._FETCH_ASSERTIONS = '/api/v1/Assertion?'
        self._UPDATE_TASK = '/api/v1/Tasks/{task_id}'
        self._EXCLUSION_ANSWER_FROM_TASK_PROFILE_QUESTION = '/api/v1/Task/{task_id}/ProfileAnswerExclusion'
        self._GET_SUPPORT_PANE = '/api/v1/Tasks/Atlas'
        self._ADD_EVIDENCE = '/api/v1/Tasks/Canvas'
        self._GET_RELATED_FORMS = '/api/v1/Forms?'
        self._GET_RALATED_TASKS = '/api/v1/Tasks?'
        self._TRANSLATE_GUIDANCE_OR_ATTACHMENT = '/api/v1/GuidanceTranslate'
        self._MOVE_TASK = '/api/v1/Tasks/{task_id}/MoveTask/?'
        self._REMOVE_ATLAS_GUIDANCE_TRANSLATION = '/api/v1/GuidanceTranslate/{guidance_content_id}?'
        self._GET_ANSWER_TO_TASK_PROFILE_QUESTION = '/api/v1/Task/{task_id}/ProfileAnswer?'
        self._REMOVE_LOCALIZED_PROFILE_QUESTION_ANSWER = '/api/v1/Task/{task_id}/ProfileAnswer/{profile_id}'
        self._FETCH_RELATED_FORMS_DETAILS = '/api/v1/TaskForm/TaskForm/{task_id}?'
        self._FETCH_RELATED_TASKS_DETAILS = '/api/v1/TaskRelatedTask/{task_id}?'
        self._ADD_SMART_WORKPAPERS = '/api/v1/Tasks/SmartWorkPaper'
        self._PROFILE_QUESTION_ANSWER_INCLUSION_EXCLUSION_TASKS = '/api/v1/Guidance/{guidance_id}/ProfileAnswerExclusion'
        self._ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION_TASKS = '/api/v1/Guidance/{guidance_id}/ProfileAnswer'
        self._ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION_TASKS = '/api/v1/Guidance/{guidance_id}/ProfileAnswerExclusion'

        # API_CG_RISK_FACTORS
        self._CREATE_RISK_FACTOR = '/api/v1/RiskFactor'
        self._GET_RISK_FACTORS = '/api/v1/RiskFactor?'
        self._UPDATE_RISK_FACTOR = '/api/v1/RiskFactor/{riskfactor_id}'
        self._TRANSLATE_RISK_FACTOR = '/api/v1/riskfactortranslate/translate'
        self._APPROVE_RISK_FACTOR = '/api/v1/RiskFactor/approve'
        self._REMOVE_TRANSLATE_RISK_FACTOR = '/api/v1/riskfactortranslate/{riskfactor_id}?'
        self._ADD_ANSWER_TO_RISK_FACTOR_PROFILE_QUESTION = '/api/v1/RiskFactorProfileAnswer/{riskfactor_id}?'

        # API_ARTEMIS_MAPS
        self._CREATE_MAP = '/api/Maps'

        # API_CG_REPLICA
        self._CREATE_REPLICA = '/api/v1/replica'
        self._GET_Publish_Content = '/api/v1/Publications?'

        # API_CG_MANAGE_ACCESS
        self._GET_CHANNELS_LANGUAGES_FOR_USER = '/api/v1/UserRoles/Roles/{user_id}/ChannelsAndLanguages?'

        # API_CG_PROFILE
        self._CREATE_PROFILE_QUESTION = '/api/v1/Questions'
        self._ADD_PROFILE_ANSWERS = '/api/v1/Answers'
        self._MOVE_PROFILE_QUESTION = '/api/v1/Questions/{profile_question_id}'

    # API_Canvas_Forms
    def SEARCH_FORM_ENDPOINT(self):
        return self._SEARCH_FORM_ENDPOINT

    def CREATE_FORM_ENDPOINT(self):
        return self._CREATE_FORM_ENDPOINT

    def ADD_HEADER_TO_FORM(self):
        return self._ADD_HEADER_TO_FORM

    def GET_HEADER_TO_FORM(self):
        return self._GET_HEADER_TO_FORM

    def ADD_FORM_ATLAS_GUIDANCE(self):
        return self._ADD_FORM_ATLAS_GUIDANCE

    def ADD_SECTION_TO_HEADER(self):
        return self._ADD_SECTION_TO_HEADER

    def ADD_BODY_TO_SECTION(self):
        return self._ADD_BODY_TO_SECTION

    def DELETE_FORM_BODY(self, body_id):
        return self._DELETE_FORM_BODY.format(body_id=body_id)

    def TRANSLATE_BODY(self):
        return self._TRANSLATE_BODY

    def GET_BODY_RESPONSE(self):
        return self._GET_BODY_RESPONSE

    def TRANSLATE_BODY_OPTION(self, bodyOptionContentId):
        return self._TRANSLATE_BODY_OPTION.format(bodyOptionContentId=bodyOptionContentId)

    def TRANSLATE_BODY_GUIDANCE(self):
        return self._TRANSLATE_BODY_GUIDANCE

    def SEARCH_SECTION_ENDPOINT(self, section_id):
        return self._SEARCH_SECTION_ENDPOINT.format(section_id=section_id)

    def TRANSLATE_SECTION(self):
        return self._TRANSLATE_SECTION

    def TRANSLATE_HEADER(self):
        return self._TRANSLATE_HEADER

    def SELECT_RELATED_OBJECT(self):
        return self._SELECT_RELATED_OBJECT

    def SELECT_FORM_DOCUMENT_TYPE(self):
        return self._SELECT_FORM_DOCUMENT_TYPE

    def SELECT_RELATED_OBJECT_HIERARCHY(self, entity_id):
        return self._SELECT_RELATED_OBJECT_HIERARCHY.format(entity_id=entity_id)

    def GET_CANVAS_FORMS(self, form_id):
        return self._GET_CANVAS_FORMS.format(form_id=form_id)

    def UPDATE_FORM(self, form_id):
        return self._UPDATE_FORM.format(form_id=form_id)

    def UPDATE_SECTION_TO_HEADER(self, section_id):
        return self._UPDATE_SECTION_TO_HEADER.format(section_id=section_id)

    def APPROVE_FORM_ENTITY(self):
        return self._APPROVE_FORM_ENTITY

    def TRANSLATE_FORM(self):
        return self._TRANSLATE_FORM

    def LOCALIZE_HEADER_FOR_FORM(self, header_id):
        return self._LOCALIZE_HEADER_FOR_FORM.format(header_id=header_id)

    def SUMMARY_TYPE(self):
        return self._SUMMARY_TYPE

    def CARD_TYPE(self):
        return self._CARD_TYPE

    def GET_BODY_INFO(self, body_id):
        return self._GET_BODY_INFO.format(body_id=body_id)

    def DELETE_HEADER(self, header_id):
        return self._DELETE_HEADER.format(header_id=header_id)

    def ADD_NESTED_BODIES(self, body_id):
        return self._ADD_NESTED_BODIES.format(body_id=body_id)

    def ADD_LINEAGE_TO_BODY(self, form_id, body_id):
        return self._ADD_LINEAGE_TO_BODY.format(form_id=form_id, body_id=body_id)

    def GET_BODY_TYPE(self):
        return self._GET_BODY_TYPE

    def GET_FORM_PROFILE_QUESTIONS(self):
        return self._GET_FORM_PROFILE_QUESTIONS

    def ADD_ANSWER_TO_FORM_PROFILE_QUESTION(self, body_id):
        return self._ADD_ANSWER_TO_FORM_PROFILE_QUESTION.format(body_id=body_id)

    def EXCLUSION_ANSWER_FROM_FORM_PROFILE_QUESTION(self, body_id):
        return self._EXCLUSION_ANSWER_FROM_FORM_PROFILE_QUESTION.format(body_id=body_id)

    def UPDATE_BODYOPTION(self, body_id):
        return self._UPDATE_BODYOPTION.format(body_id=body_id)

    def ADD_ANSWER_TO_SECTION_PROFILE_QUESTION(self, section_id):
        return self._ADD_ANSWER_TO_SECTION_PROFILE_QUESTION.format(section_id=section_id)

    def EXCLUSION_ANSWER_FROM_SECTION_PROFILE_QUESTION(self, section_id):
        return self._EXCLUSION_ANSWER_FROM_SECTION_PROFILE_QUESTION.format(section_id=section_id)

    def REMOVE_ANSWER_FROM_SECTION_PROFILE_QUESTION(self, section_id, question_id):
        return self._REMOVE_ANSWER_FROM_SECTION_PROFILE_QUESTION.format(section_id=section_id, question_id=question_id)

    def REMOVE_EXCLUDED_ANSWER_FROM_SECTION_PROFILE_QUESTION(self, section_id, question_id):
        return self._REMOVE_EXCLUDED_ANSWER_FROM_SECTION_PROFILE_QUESTION.format(section_id=section_id,
                                                                                 question_id=question_id)

    def REMOVE_ANSWER_FROM_BODY_PROFILE_QUESTION(self, body_id, question_id):
        return self._REMOVE_ANSWER_FROM_BODY_PROFILE_QUESTION.format(body_id=body_id, question_id=question_id)

    def REMOVE_EXCLUDED_ANSWER_FROM_BODY_PROFILE_QUESTION(self, body_id, question_id):
        return self._REMOVE_EXCLUDED_ANSWER_FROM_BODY_PROFILE_QUESTION.format(body_id=body_id, question_id=question_id)

    def ADD_RISK_FACTOR_TO_BODY(self, body_id, body_action_id):
        return self._ADD_RISK_FACTOR_TO_BODY.format(body_id=body_id, body_action_id=body_action_id)

    def GET_BODY_ACTION_TYPE(self):
        return self._GET_BODY_ACTION_TYPE

    def GET_Materiality_Type(self):
        return self._GET_Materiality_Type

    def BODY_OPTION_PROFILE_ANSWER_INCLUSION(self, body_id, body_option_id):
        return self._BODY_OPTION_PROFILE_ANSWER_INCLUSION.format(body_id=body_id, body_option_id=body_option_id)

    def BODY_OPTION_PROFILE_ANSWER_EXCLUSION(self, body_id, body_option_id):
        return self._BODY_OPTION_PROFILE_ANSWER_EXCLUSION.format(body_id=body_id, body_option_id=body_option_id)

    def REMOVE_BODY_OPTION_PROFILE_ANSWER_INCLUSION(self, body_id, body_option_id, inclusion_id):
        return self._REMOVE_BODY_OPTION_PROFILE_ANSWER_INCLUSION.format(body_id=body_id, body_option_id=body_option_id,
                                                                        inclusion_id=inclusion_id)

    def REMOVE_BODY_OPTION_PROFILE_ANSWER_EXCLUSION(self, body_id, body_option_id, exclusion_id):
        return self._REMOVE_BODY_OPTION_PROFILE_ANSWER_EXCLUSION.format(body_id=body_id, body_option_id=body_option_id,
                                                                        exclusion_id=exclusion_id)

    def ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION(self, guidance_id):
        return self._ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION.format(guidance_id=guidance_id)

    def ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION(self, guidance_id):
        return self._ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION.format(guidance_id=guidance_id)

    # API_Common
    def SELECT_CHANNEL(self):
        return self._SELECT_CHANNEL

    def SELECT_CHANNEL_LANGUAGE(self):
        return self._SELECT_CHANNEL_LANGUAGE

    def SELECT_SERVICE_LINE(self):
        return self._SELECT_SERVICE_LINE

    def GET_SERVICE_ORGANIZATION(self):
        return self._GET_SERVICE_ORGANIZATION

    def GET_PROFILE_QUESTIONS(self):
        return self._GET_PROFILE_QUESTIONS

    def GET_ATLAS_GUIDANCE_TYPE(self):
        return self._GET_ATLAS_GUIDANCE_TYPE

    def ADD_CG_USER(self):
        return self._ADD_CG_USER

    def REVOKE_CG_USER_ROLE(self, user_id):
        return self._REVOKE_CG_USER_ROLE.format(user_id=user_id)

    def REVOKE_CG_USER_ACCESS(self):
        return self._REVOKE_CG_USER_ACCESS

    def CHANNEL_CHILDREN(self):
        return self._CHANNEL_CHILDREN

    def SEARCH_CG_USER(self):
        return self._SEARCH_CG_USER

    def SELECT_SERVICE_MODULE(self):
        return self._SELECT_SERVICE_MODULE

    def GET_USER_ROLES_FOR_USER(self, user_id):
        return self._GET_USER_ROLES_FOR_USER.format(user_id=user_id)

    def SELECT_SERVICE_LINE_FOR_ALL(self):
        return self._SELECT_SERVICE_LINE_FOR_ALL

    def GET_SERVICE_ORGANIZATION_FOR_ALL(self):
        return self._GET_SERVICE_ORGANIZATION_FOR_ALL

    def GET_ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION_ID(self, guidance_id, data_entity_uid, data_entity_id):
        return self._GET_ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION_ID.format(guidance_id=guidance_id, data_entity_uid=data_entity_uid,
                                                                           data_entity_id=data_entity_id)

    def GET_ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION_ID(self, guidance_id, data_entity_uid, data_entity_id):
        return self._GET_ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION_ID.format(guidance_id=guidance_id, data_entity_uid=data_entity_uid,
                                                                           data_entity_id=data_entity_id)

    def REMOVE_ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION(self, guidance_id, data_entity_uid, data_entity_id, inclusion_id):
        return self._REMOVE_ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION.format(guidance_id=guidance_id, data_entity_uid=data_entity_uid,
                                                                           data_entity_id=data_entity_id, inclusion_id=inclusion_id)

    def REMOVE_ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION(self, guidance_id, data_entity_uid, data_entity_id, exclusion_id):
        return self._REMOVE_ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION.format(guidance_id=guidance_id, data_entity_uid=data_entity_uid,
                                                                           data_entity_id=data_entity_id, exclusion_id=exclusion_id)

    # API_CGGroup_audit_instructions
    def GET_GROUP_INSTRUCTIONS(self):
        return self._GET_GROUP_INSTRUCTIONS

    def SEARCH_GROUP_AUDIT_INSTRUCTION(self, instruction_id):
        return self._SEARCH_GROUP_AUDIT_INSTRUCTION.format(instruction_id=instruction_id)

    def TRANSLATE_GROUP_INSTRUCTION(self):
        return self._TRANSLATE_GROUP_INSTRUCTION

    def LOCALIZE_GROUP_INSTRUCTION(self):
        return self._LOCALIZE_GROUP_INSTRUCTION

    def CREATE_GROUP_INSTRUCTIONS(self):
        return self._CREATE_GROUP_INSTRUCTIONS

    def GET_GROUP_INSTRUCTION_SCOPE(self):
        return self._GET_GROUP_INSTRUCTION_SCOPE

    def GET_GROUP_INSTRUCTION_SECTION(self):
        return self._GET_GROUP_INSTRUCTION_SECTION

    def GET_RECOMMENDATION_TYPE(self):
        return self._GET_RECOMMENDATION_TYPE

    def DELETE_GROUP_INSTRUCTION_TRANSLATE(self, content_id):
        return self._DELETE_GROUP_INSTRUCTION_TRANSLATE.format(content_id=content_id)

    def SEARCH_GROUP_AUDIT_INSTRUCTION_ID(self, instruction_id):
        return self._SEARCH_GROUP_AUDIT_INSTRUCTION_ID.format(instruction_id=instruction_id)

    def SEARCH_GA_INSTRUCTION_PROFILE_QUESTION(self, instruction_id):
        return self._SEARCH_GA_INSTRUCTION_PROFILE_QUESTION.format(instruction_id=instruction_id)

    def DELETE_GROUP_INSTRUCTION_LOCALIZE(self, localize_id):
        return self._DELETE_GROUP_INSTRUCTION_LOCALIZE.format(localize_id=localize_id)

    def APPROVE_DELETED_INSTRUCTION(self):
        return self._APPROVE_DELETED_INSTRUCTION

    def GA_ADD_EVIDENCE(self):
        return self._GA_ADD_EVIDENCE

    def GA_GUIDANCE_TRANSLATE(self):
        return self._GA_GUIDANCE_TRANSLATE

    def GA_ATLAS_GUIDANCE_PROFILE_INCLUSION(self, guidance_id):
        return self._GA_ATLAS_GUIDANCE_PROFILE_INCLUSION.format(guidance_id=guidance_id)

    def GA_ATLAS_GUIDANCE_PROFILE_EXCLUSION(self, guidance_id):
        return self._GA_ATLAS_GUIDANCE_PROFILE_EXCLUSION.format(guidance_id=guidance_id)

        # API_CG_ENTITY_STATUS_PREVIEW

    def GA_ENTITY_STATUS_PREVIEW(self):
        return self._GA_ENTITY_STATUS_PREVIEW

    # API_CG_Canvas_Psp_Index
    def CREATE_PSP_INDEX(self):
        return self._CREATE_PSP_INDEX

    def GET_METADATA_TAG(self):
        return self._GET_METADATA_TAG

    def TRANSLATE_PSP_INDEXES(self):
        return self._TRANSLATE_PSP_INDEXES

    def GET_PSP_INDEXES_LIST(self):
        return self._GET_PSP_INDEXES_LIST

    def GET_PSP_INDEX(self, pspindex_id):
        return self._GET_PSP_INDEX.format(pspindex_id=pspindex_id)

    def DELETE_PSP_INDEX(self, psp_index_id):
        return self._DELETE_PSP_INDEX.format(psp_index_id=psp_index_id)

    def DELETED_PSP_PENDING_APPROVAL(self):
        return self._DELETED_PSP_PENDING_APPROVAL

    def DELETED_PSP_APPROVE(self):
        return self._DELETED_PSP_APPROVE

    def EDIT_PSP_INDEX(self, psp_index_id):
        return self._EDIT_PSP_INDEX.format(psp_index_id=psp_index_id)

    def MOVE_PSPINDEX(self, psp_index_id):
        return self._MOVE_PSPINDEX.format(psp_index_id=psp_index_id)

    def ADD_PSP_ATLAS_GUIDANCE(self):
        return self._ADD_PSP_ATLAS_GUIDANCE

    def PSP_PROFILE_ANSWER(self, psp_index_id):
        return self._PSP_PROFILE_ANSWER.format(psp_index_id=psp_index_id)

    def PSP_LOCALIZED_PROFILE_ANSWER(self, psp_index_id, channel_id):
        return self._PSP_LOCALIZED_PROFILE_ANSWER.format(psp_index_id=psp_index_id, channel_id=channel_id)

    def ENTITYPREVIEW_PSP(self):
        return self._ENTITYPREVIEW_ENDPOINT

    def ADD_ANSWER_TO_PSP_PROFILE_QUESTION(self, body_id):
        return self._ADD_ANSWER_TO_PSP_PROFILE_QUESTION.format(body_id=body_id)

    def EXCLUSION_ANSWER_FROM_PSP_PROFILE_QUESTION(self, body_id):
        return self._EXCLUSION_ANSWER_FROM_PSP_PROFILE_QUESTION.format(body_id=body_id)

    # API_CG_Canvas_Tasks

    def SELECT_TASK_TYPE(self):
        return self._SELECT_TASK_TYPE

    def SELECT_TASK_GROUP(self):
        return self._SELECT_TASK_GROUP

    def SELECT_TASK_BUILD_MILESTONE(self):
        return self._SELECT_TASK_BUILD_MILESTONE

    def SELECT_TASK_MILESTONE_TYPE(self):
        return self._SELECT_TASK_MILESTONE_TYPE

    def SELECT_TASK_MULTIENTITY_TYPE(self):
        return self._SELECT_TASK_MULTIENTITY_TYPE

    def CREATE_TASK(self):
        return self._CREATE_TASK

    def SEARCH_AND_FETCH_TASK_BY_ID(self, task_id):
        return self._SEARCH_AND_FETCH_TASK_BY_ID.format(task_id=task_id)

    def DELETE_TASK(self, task_id):
        return self._DELETE_TASK.format(task_id=task_id)

    def DELETE_ENTITYSTATUS(self):
        return self._DELETE_ENTITYSTATUS

    def TASK_APPROVAL(self):
        return self._TASK_APPROVAL

    def REMOVE_LOCALIZATION_OR_TRANSLATION(self, task_content_id):
        return self._REMOVE_LOCALIZATION_0R_TRANSLATION.format(task_content_id=task_content_id)

    def GET_PROFILE_QUESTIONS_ANSWERS(self):
        return self._GET_PROFILE_QUESTIONS_ANSWERS

    def ADD_ANSWER_TO_TASK_PROFILE_QUESTION(self, task_id):
        return self._ADD_ANSWER_TO_TASK_PROFILE_QUESTION.format(task_id=task_id)

    def TRANSLATE_CANVAS_TASK(self):
        return self._TRANSLATE_CANVAS_TASK

    def LOCALIZE_TASK(self, task_id):
        return self._LOCALIZE_TASK.format(task_id=task_id)

    def SEARCH_AND_FETCH_BY_ID_IN_SEARCH_BOX(self):
        return self._SEARCH_AND_FETCH_BY_ID_IN_SEARCH_BOX

    def FETCH_PSP_INDEXES(self):
        return self._FETCH_PSP_INDEXES

    def FETCH_ASSERTION(self):
        return self._FETCH_ASSERTIONS

    def UPDATE_TASK(self, task_id):
        return self._UPDATE_TASK.format(task_id=task_id)

    def EXCLUSION_ANSWER_FROM_TASK_PROFILE_QUESTION(self, task_id):
        return self._EXCLUSION_ANSWER_FROM_TASK_PROFILE_QUESTION.format(task_id=task_id)

    def GET_SUPPORT_PANE(self):
        return self._GET_SUPPORT_PANE

    def ADD_EVIDENCE(self):
        return self._ADD_EVIDENCE

    def GET_RELATED_FORMS(self):
        return self._GET_RELATED_FORMS

    def GET_RALATED_TASKS(self):
        return self._GET_RALATED_TASKS

    def TRANSLATE_GUIDANCE_OR_ATTACHMENT(self):
        return self._TRANSLATE_GUIDANCE_OR_ATTACHMENT

    def ADD_ATLAS_GUIDANCE(self):
        return self._ADD_ATLAS_GUIDANCE

    def GUIDANCE_SERVICE(self):
        return self._GUIDANCE_SERVICE

    def MOVE_TASK(self, task_id):
        return self._MOVE_TASK.format(task_id=task_id)

    def REMOVE_ATLAS_GUIDANCE_TRANSLATION(self, guidance_content_id):
        return self._REMOVE_ATLAS_GUIDANCE_TRANSLATION.format(guidance_content_id=guidance_content_id)

    def GET_ANSWER_TO_TASK_PROFILE_QUESTION(self, task_id):
        return self._GET_ANSWER_TO_TASK_PROFILE_QUESTION.format(task_id=task_id)

    def REMOVE_LOCALIZED_PROFILE_QUESTION_ANSWER(self, task_id, profile_id):
        return self._REMOVE_LOCALIZED_PROFILE_QUESTION_ANSWER.format(task_id=task_id, profile_id=profile_id)

    def FETCH_RELATED_FORMS_DETAILS(self, task_id):
        return self._FETCH_RELATED_FORMS_DETAILS.format(task_id=task_id)

    def FETCH_RELATED_TASKS_DETAILS(self, task_id):
        return self._FETCH_RELATED_TASKS_DETAILS.format(task_id=task_id)

    def ADD_SMART_WORKPAPERS(self):
        return self._ADD_SMART_WORKPAPERS

    # API_CG_RISK_FACTORS
    def CREATE_RISK_FACTOR(self):
        return self._CREATE_RISK_FACTOR

    def GET_RISK_FACTORS(self):
        return self._GET_RISK_FACTORS

    def UPDATE_RISK_FACTOR_ID(self, riskfactor_id):
        return self._UPDATE_RISK_FACTOR.format(riskfactor_id=riskfactor_id)

    def TRANSLATE_RISK_FACTOR(self):
        return self._TRANSLATE_RISK_FACTOR

    def REMOVE_TRANSLATE_RISK_FACTOR(self, riskfactor_id):
        return self._REMOVE_TRANSLATE_RISK_FACTOR.format(riskfactor_id=riskfactor_id)

    def APPROVE_RISK_FACTOR(self):
        return self._APPROVE_RISK_FACTOR

    def ADD_ANSWER_TO_RISK_FACTOR_PROFILE_QUESTION(self, riskfactor_id):
        return self._ADD_ANSWER_TO_RISK_FACTOR_PROFILE_QUESTION.format(riskfactor_id=riskfactor_id)

    # API_Artemis_Map
    def CREATE_MAP(self):
        return self._CREATE_MAP

    # API_CG_REPLICA
    def CREATE_REPLICA(self):
        return self._CREATE_REPLICA

    def GET_Publish_Content(self):
        return self._GET_Publish_Content

    # API_CG_MANAGE_ACCESS
    def GET_CHANNELS_LANGUAGES_FOR_USER(self, user_id):
        return self._GET_CHANNELS_LANGUAGES_FOR_USER.format(user_id=user_id)

    # API_CG_Profile

    def CREATE_PROFILE_QUESTION(self):
        return self._CREATE_PROFILE_QUESTION

    def ADD_PROFILE_ANSWERS(self):
        return self._ADD_PROFILE_ANSWERS

    def MOVE_PROFILE_QUESTION(self, profile_question_id):
        return self._MOVE_PROFILE_QUESTION.format(profile_question_id=profile_question_id)


    def PROFILE_QUESTION_ANSWER_INCLUSION_EXCLUSION_TASKS(self,guidance_id):
        return self._PROFILE_QUESTION_ANSWER_INCLUSION_EXCLUSION_TASKS.format(guidance_id=guidance_id)


    def ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION_TASKS(self, guidance_id):
        return self._ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION_TASKS.format(guidance_id=guidance_id)

    def ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION_TASKS(self, guidance_id):
        return self._ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION_TASKS.format(guidance_id=guidance_id)
