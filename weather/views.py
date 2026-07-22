from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import ChatForm
from .services.chatbot_service import ChatbotService
from .managers.conversation_manager import ConversationManager

@login_required
def home(request):

    form = ChatForm()
    response = None

    if request.method == "POST":
        form = ChatForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data["message"]
            last_city = ConversationManager.get_last_city(request)

            response = ChatbotService.process_message(message, last_city)

            if response["last_city"]:
                ConversationManager.set_last_city(request, response["last_city"])

        
    return render(request, "index.html", {"form": form, "response": response})