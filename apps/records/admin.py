from django.contrib import admin

from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_by", "created_at")
    list_filter = ("status",)
    search_fields = ("title",)
    readonly_fields = ("created_at", "updated_at")
