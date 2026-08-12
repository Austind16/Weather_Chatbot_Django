from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import ChatForm
from .services.chatbot_service import ChatbotService
from .managers.conversation_manager import ConversationManager
from django.http import JsonResponse
from .models import Chat

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

            Chat.objects.create(
            user=request.user,
            user_message=message,
            bot_response=response.get("reply", ""),
            intent=response.get("intent", ""),
            city=response.get("last_city", "") or "",
)

            if response["last_city"]:
                ConversationManager.set_last_city(request, response["last_city"])

        
    return render(request, "index.html", {"form": form, "response": response})

@login_required
def chat_api(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "POST request required."
            },
            status=405
        )

    form = ChatForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid message.",
                "errors": form.errors.get_json_data()
            },
            status=400
        )

    message = form.cleaned_data["message"]

    # Get the city from the previous conversation
    last_city = ConversationManager.get_last_city(request)

    # Send the message through the actual chatbot
    response = ChatbotService.process_message(
        message,
        last_city
    )

    if response.get("last_city"):
        ConversationManager.set_last_city(
            request,
            response["last_city"]
        )

    Chat.objects.create(
        user=request.user,
        user_message=message,
        bot_response=response.get("reply", ""),
        intent=response.get("intent", ""),
        city=response.get("last_city", "") or "",
    )
    return JsonResponse(response)