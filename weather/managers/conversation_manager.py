class ConversationManager:

    SESSION_KEY = "conversation"

    @classmethod
    def get_last_city(cls, request):

        conversation = request.session.get(cls.SESSION_KEY, {})

        return conversation.get("last_city")


    @classmethod
    def set_last_city(cls, request, city):

        conversation = request.session.get(cls.SESSION_KEY, {})

        conversation["last_city"] = city

        request.session[cls.SESSION_KEY] = conversation


    @classmethod
    def clear(cls, request):

        if cls.SESSION_KEY in request.session:
            del request.session[cls.SESSION_KEY]