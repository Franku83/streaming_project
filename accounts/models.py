from django.db import models
import datetime
from django.utils import timezone

class Account(models.Model):
    """
    Modelo para gestionar las cuentas de streaming.
    """
    PLATFORM_CHOICES = (
        ('Netflix', 'Netflix'),
        ('HBO Max', 'HBO Max'),
        ('Disney+', 'Disney+'),
        ('Amazon Prime Video', 'Amazon Prime Video'),
        ('Spotify', 'Spotify'),
        ('YouTube Premium', 'YouTube Premium'),
        ('Apple TV+', 'Apple TV+'),
        ('Apple Music', 'Apple Music'),
        ('Star+', 'Star+'),
        ('Crunchyroll', 'Crunchyroll'),
        ('Paramount+', 'Paramount+'),
        ('Otro', 'Otro')
    )

    client_name = models.CharField(max_length=100, verbose_name="Nombre del Cliente")
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, verbose_name="Plataforma")
    expiration_date = models.DateField(verbose_name="Fecha de Vencimiento")
    details = models.TextField(verbose_name="Detalles de la Cuenta (Usuario/Contraseña/Notas)")
    notes = models.TextField(verbose_name="Notas Adicionales", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    def __str__(self):
        return f"{self.client_name} - {self.platform}"

    def is_expiring_soon(self, days=7):
        """
        Verifica si la cuenta expira en los próximos 'días'.
        """
        return self.expiration_date <= timezone.now().date() + datetime.timedelta(days=days)

    def is_expired(self):
        """
Verifica si la cuenta ya ha vencido.
        """
        return self.expiration_date < timezone.now().date()

    class Meta:
        ordering = ['expiration_date']
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"


