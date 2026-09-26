from django import forms
from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Album, Photo, Video


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single = super().clean
        if isinstance(data, (list, tuple)):
            return [single(d, initial) for d in data]
        return [single(data, initial)] if data else []


class AlbumForm(forms.ModelForm):
    bulk_photos = MultipleImageField(
        required=False, label="Upload photos",
        help_text="Select several photos at once. Total upload per save must stay under ~4 MB "
                  "(hosting limit) — upload in batches of 3–5 phone photos.",
    )

    class Meta:
        model = Album
        fields = "__all__"


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0
    fields = ("thumb", "image", "caption", "order")
    readonly_fields = ("thumb",)

    @admin.display(description="Preview")
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px">', obj.image.url)
        return ""


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm
    list_display = ("title", "date", "photo_count", "is_published")
    list_editable = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PhotoInline]

    @admin.display(description="Photos")
    def photo_count(self, obj):
        return obj.photos.count()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        files = form.cleaned_data.get("bulk_photos") or []
        for f in files:
            Photo.objects.create(album=obj, image=f)
        if files:
            messages.success(request, f"Uploaded {len(files)} photo(s).")


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "is_published")
    list_editable = ("is_published",)
