from django.contrib import admin
from juapp.models import Diario, Pagina, TermoParaBusca, LocalParaBusca

admin.site.register(LocalParaBusca)
admin.site.register(TermoParaBusca)
admin.site.register(Diario)
admin.site.register(Pagina)


# class DiarioAdmin(admin.ModelAdmin):
#     list_display = ('nome', 'quantidade_total', 'data')
#
# admin.site.register(Diario, DiarioAdmin)
#
# @admin.register(Page)
# class PageAdmin(admin.ModelAdmin):
#     pass