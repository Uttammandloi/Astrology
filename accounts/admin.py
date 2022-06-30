from django.contrib import admin
from accounts.models import Birthdata, RateyourReading, Contact
# Register your models here.

# Register your models here.


class Birthdataadmin(admin.ModelAdmin):
    list_display = ('screen_name', 'full_name', 'user_id', 'date_of_birth',
                    'time_of_birth', 'birth_city_sate', 'longitude', 'lattitude', 'your_current_location', 'transits_chart_date')


admin.site.register(Birthdata, Birthdataadmin)

# rate your reading  admin..


class RateyourReadingadmin(admin.ModelAdmin):
    list_display = ('screen_name', 'email', 'user_id', 'rate_synchronic',
                    'message',)


admin.site.register(RateyourReading, RateyourReadingadmin)

# contact admin..


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', )
    list_display_links = ('id', 'name', 'email',)


admin.site.register(Contact, ContactAdmin)
