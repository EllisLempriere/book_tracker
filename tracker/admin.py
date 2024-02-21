from django.contrib import admin

from tracker.models import *

admin.site.register(Series)
admin.site.register(SeriesBook)
admin.site.register(Book)
admin.site.register(ToReadBook)
admin.site.register(InProgressRead)
admin.site.register(FinishedRead)
