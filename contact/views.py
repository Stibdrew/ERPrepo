from .forms import ContactForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import ReplyForm
from django.shortcuts import render
from .models import Message, Reply  # Make sure to import the Reply model

@login_required
def my_replies(request):
    # Get messages sent by the logged-in user
    messages = Message.objects.filter(user=request.user)

    # Fetch replies for each message
    message_replies = {}
    for message in messages:
        message_replies[message] = Reply.objects.filter(message=message)  # Get replies for each message

    return render(request, 'users/replies.html', {'message_replies': message_replies})



@login_required
def all_messages(request):
    messages = Message.objects.all()  # Get all messages
    reply_form = ReplyForm()  # Initialize an empty reply form
    return render(request, 'users/all_messages.html', {'messages': messages, 'reply_form': reply_form})

@login_required
def add_reply(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.user = request.user  # Assign the logged-in user to the reply
            reply.message = message  # Link reply to the specific message
            reply.save()
            return redirect('all_messages')  # Redirect to the message list

    return redirect('all_messages')  # Redirect if the form is invalid or GET request

@login_required  # Ensure that only logged-in users can access this view
def messages_user(request):
    # Retrieve messages sent by the logged-in user
    messages = Message.objects.filter(user=request.user)
    return render(request, 'users/messages.html', {'messages': messages})

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Message.objects.create(user=request.user, content=content)  # Auto-assign the logged-in user
            return redirect('messages_user')  # Redirect to the messages page
    else:
        form = ContactForm()

    return render(request, 'users/contact.html', {'form': form})

def success_view(request):
    return render(request, 'users/success.html')  # Optional, can be removed

def reply(request):
    return render(request, 'users/replies.html')  # Opt