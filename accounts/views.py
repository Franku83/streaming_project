from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Account
from .forms import AccountForm

# Función auxiliar para generar el mensaje
def generate_message(account):
    """
    Genera un mensaje de recordatorio para el cliente.
    """
    expiration_date_str = account.expiration_date.strftime("%d/%m/%Y")
    if account.is_expired():
        # Mensaje para cuentas vencidas
        message = (
            f"Hola {account.client_name}, tu suscripción de {account.platform} "
            f"se venció el {expiration_date_str}. Por favor, renueva para continuar "
            f"disfrutando del servicio. ¡Gracias!"
        )
    else:
        # Mensaje para cuentas activas
        message = (
            f"Hola {account.client_name}, tu suscripción de {account.platform} "
            f"vence el {expiration_date_str}. ¡Recuerda renovarla a tiempo!"
        )
    return message


def account_list(request):
    """
    Vista para listar todas las cuentas y resaltar las que vencen pronto.
    """
    today = timezone.now().date()
    # Cuentas que vencen en los próximos 7 días (o menos, incluyendo hoy)
    expiring_soon_accounts = Account.objects.filter(
        expiration_date__gte=today,
        expiration_date__lte=today + timedelta(days=7)
    ).order_by('expiration_date')

    # Cuentas vencidas
    expired_accounts = Account.objects.filter(expiration_date__lt=today).order_by('-expiration_date')

    # Todas las demás cuentas
    other_accounts = Account.objects.exclude(
        id__in=[acc.id for acc in expiring_soon_accounts] + [acc.id for acc in expired_accounts]
    ).order_by('expiration_date')

    # Agregamos los mensajes a cada cuenta en las listas
    for account in expiring_soon_accounts:
        account.message = generate_message(account)
    for account in expired_accounts:
        account.message = generate_message(account)
    for account in other_accounts:
        account.message = generate_message(account)

    context = {
        'expiring_soon_accounts': expiring_soon_accounts,
        'expired_accounts': expired_accounts,
        'other_accounts': other_accounts,
    }
    return render(request, 'accounts/account_list.html', context)

def account_create(request):
    """
Vista para crear una nueva cuenta.
    """
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('account_list')
    else:
        form = AccountForm()
    return render(request, 'accounts/account_form.html', {'form': form, 'title': 'Crear Nueva Cuenta'})

def account_update(request, pk):
    """
Vista para actualizar una cuenta existente.
    """
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cuenta actualizada exitosamente!')
            return redirect('account_list')
    else:
        form = AccountForm(instance=account)
    return render(request, 'accounts/account_form.html', {'form': form, 'title': 'Editar Cuenta'})

def account_delete(request, pk):
    """
Vista para eliminar una cuenta.
    """
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Cuenta eliminada exitosamente.')
        return redirect('account_list')
    return render(request, 'accounts/account_confirm_delete.html', {'account': account})
    



