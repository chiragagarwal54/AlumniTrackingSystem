from django.shortcuts import render

# Create your views here.
def room(request):
    return render(request, 'chat/room.html', {
        'room_name': 'room'
    })