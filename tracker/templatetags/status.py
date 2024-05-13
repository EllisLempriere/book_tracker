from django import template
from django.contrib.contenttypes.models import ContentType

from tracker.models import ToReadBook, InProgressRead, FinishedRead

register = template.Library()


@register.simple_tag(name='status', takes_context=True)
def status(context):
    book_type = ContentType.objects.get_for_model(context['user_book'])
    if book_type == ContentType.objects.get_for_model(ToReadBook):
        return 'To Read'
    elif book_type == ContentType.objects.get_for_model(InProgressRead):
        return 'In Progress'
    elif book_type == ContentType.objects.get_for_model(FinishedRead):
        return 'Finished'
