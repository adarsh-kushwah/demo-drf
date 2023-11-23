from rest_framework.reverse import reverse


def fully_qualified_URL(view_name, request):
    """
    creating full url
    """
    full_url = reverse(view_name, kwargs={"pk": request.user.id}, request=request)
    return full_url
