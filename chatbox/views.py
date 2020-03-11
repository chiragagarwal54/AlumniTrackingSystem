from django.shortcuts import render, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from chatbox.models import *
from datetime import datetime
from chatbox.forms import MessageForm
# Create your views here.

@login_required(login_url='/login')
def Chat(request):
    if request.method == 'GET':
        form = MessageForm()
        messages = Message.objects.order_by('id')[:200]
        context = {'messages':messages,'form':form}
        return render(request, "chatbox/chat.html", context)
    elif request.method == 'POST':
        form = MessageForm(request.POST)
        new_message = Message()
        if form.is_valid():
            new_message.message_text = form.cleaned_data.get('content')
            new_message.pub_date = datetime.now()
            new_message.sent_by = request.user
            new_message.save()
        messages = Message.objects.order_by('-id')[:200]
        context = {'messages':messages, 'form':form}
        return render(request, "chatbox/chat.html", context)


