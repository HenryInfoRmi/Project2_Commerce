from django.contrib import admin
from .models import User,auct_list,bid,comment_auct,category
# Register your models here.
admin.site.register(User)
admin.site.register(auct_list)
admin.site.register(bid)
admin.site.register(comment_auct)
admin.site.register(category)