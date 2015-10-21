from .models import Person


def getRole(request):
    print request.user.id
    return Person.objects.get(user_id=request.user.id).type
