from django.contrib import admin

from terminology.models import Spravochnik, Element


class ElementInline(admin.TabularInline):
    model = Element
    extra = 1

@admin.register(Spravochnik)
class SpravochnikAdmin(admin.ModelAdmin):
    """Детализация настроек админки для справочников"""

    list_display = ('__str__', 'date_created',)
    inlines = (ElementInline,)


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    """Детализация настроек админки для элементов"""

    list_display = ('code', 'elem_value', 'spravochnik')
    list_filter = ('spravochnik',)
    list_per_page = 100
