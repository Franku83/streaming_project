from django.contrib import admin
from .models import Account
import datetime
from django.utils import timezone

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """
Configuración del panel de administración para el modelo Account.
    """
    list_display = (
        'client_name',
        'platform',
        'expiration_date',
        'recordatorio', # Renombrado para ser más claro
        'is_expired_display',
        'created_at',
    )
    list_filter = (
        'platform',
        'expiration_date',
    )
    search_fields = (
        'client_name',
        'platform',
        'details',
        'notes',
    )
    date_hierarchy = 'expiration_date'

    fieldsets = (
        (None, {
            'fields': ('client_name', 'platform', 'expiration_date', 'details', 'notes')
        }),
        ('Fechas Importantes', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def recordatorio(self, obj):
        """
Muestra un texto descriptivo para el recordatorio.
        """
        if obj.is_expired():
            return "Vencida"
        elif obj.is_expiring_soon(days=7):
            return "¡Vence pronto!"
        return "Activa"
    recordatorio.short_description = "Recordatorio" # Nombre de la columna

    def is_expired_display(self, obj):
        """
Muestra un indicador si la cuenta ya ha vencido.
        """
        return obj.is_expired()
    is_expired_display.short_description = "Vencida"
    is_expired_display.boolean = True # Mantiene el icono de sí/no aquí

    # Estilo de fila para cuentas vencidas o que vencen pronto
    def get_row_css(self, obj, index):
        if obj.is_expired():
            return 'expired-row'
        elif obj.is_expiring_soon(days=7):
            return 'expiring-soon-row'
        return ''

    # Añadir CSS personalizado al admin para resaltar filas
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        

