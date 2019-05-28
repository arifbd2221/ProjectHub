from django.contrib import admin
from .models import Post,Category, Comments, Images

class ImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image')


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Images, ImageAdmin)
