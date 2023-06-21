from django.contrib import admin

# Register your models here.
from account.models import Account, Transaction, Category

admin.site.register(Account)

admin.site.register(Transaction)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
