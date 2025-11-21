from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from .models import Claim, ClaimHistory, Notification, AdminActivity, FAQ
from .forms import ClaimForm, ClaimSearchForm, ClaimFilterForm, ClaimUpdateForm, FAQForm
import csv
from datetime import datetime


def is_admin(user):
    """Verificar si el usuario es administrador"""
    return user.is_staff or user.is_superuser


def index(request):
    """Página de inicio - RF1: Permitir sin login"""
    faqs = FAQ.objects.filter(is_active=True)[:3]
    return render(request, "claims/index.html", {"faqs": faqs})


def register_claim(request):
    """Registrar reclamo sin necesidad de login - RF1, RF2, RF3, RF4, RF5, RF6"""
    if request.method == "POST":
        form = ClaimForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            # RF2: Asociar automáticamente si está logueado
            if request.user.is_authenticated:
                claim.created_by = request.user
            claim.save()
            
            # Registrar actividad si es admin
            if request.user.is_authenticated and is_admin(request.user):
                AdminActivity.objects.create(
                    user=request.user,
                    claim=claim,
                    action="Reclamo creado",
                    description=f"Reclamo {claim.number} creado"
                )
            
            # Crear notificación inicial
            _create_notification(claim, f"Tu reclamo {claim.number} ha sido registrado exitosamente.")
            
            # RF20: Mostrar mensaje de confirmación
            messages.success(request, f"¡Reclamo registrado correctamente! Tu número de reclamo es: {claim.number}")
            return redirect("claims:claim_detail_public", pk=claim.pk)
    else:
        form = ClaimForm()

    return render(request, "claims/register_claim.html", {"form": form})


def claim_detail_public(request, pk):
    """Ver detalles del reclamo - RF7: Ver estado"""
    claim = get_object_or_404(Claim, pk=pk)
    history = claim.history.all()
    return render(request, "claims/claim_detail_public.html", {"claim": claim, "history": history})


def claim_detail(request, pk):
    """Ver detalles del reclamo para usuarios autenticados"""
    if request.user.is_authenticated:
        claim = get_object_or_404(Claim, pk=pk)
        if claim.created_by != request.user and not is_admin(request.user):
            messages.error(request, "No tienes permiso para ver este reclamo")
            return redirect("claims:index")
        history = claim.history.all()
        return render(request, "claims/claim_detail.html", {"claim": claim, "history": history})
    return redirect("claims:login")


def search_claim(request):
    """Buscar reclamo - RF21: Por número de reclamo o pedido"""
    form = ClaimSearchForm()
    results = []
    
    if request.method == "GET" and request.GET.get("query"):
        query = request.GET.get("query")
        results = Claim.objects.filter(
            Q(number__icontains=query) | Q(order_number__icontains=query)
        )
    
    return render(request, "claims/search.html", {"form": form, "results": results})


@login_required
def my_claims(request):
    """Ver mis reclamos - RF15: Historial para clientes"""
    claims = Claim.objects.filter(created_by=request.user)
    return render(request, "claims/my_claims.html", {"claims": claims})


@login_required
def admin_list(request):
    """Panel del administrador - RF11, RF12: Ver y filtrar reclamos"""
    if not is_admin(request.user):
        messages.error(request, "No tienes permisos para acceder a este panel")
        return redirect("claims:index")
    
    claims = Claim.objects.all()
    form = ClaimFilterForm(request.GET)
    
    # Aplicar filtros
    if form.is_valid():
        if form.cleaned_data.get('status'):
            claims = claims.filter(status=form.cleaned_data['status'])
        if form.cleaned_data.get('priority'):
            claims = claims.filter(priority=form.cleaned_data['priority'])
        if form.cleaned_data.get('zone'):
            claims = claims.filter(zone__icontains=form.cleaned_data['zone'])
        if form.cleaned_data.get('date_from'):
            claims = claims.filter(created_at__date__gte=form.cleaned_data['date_from'])
        if form.cleaned_data.get('date_to'):
            claims = claims.filter(created_at__date__lte=form.cleaned_data['date_to'])
    
    return render(request, "claims/admin_list.html", {"claims": claims, "form": form})


@login_required
@require_http_methods(["POST"])
def update_claim_status(request, pk):
    """Actualizar estado del reclamo - RF13, RF14: Cambiar estado y guardar historial"""
    if not is_admin(request.user):
        return JsonResponse({'error': 'No permitido'}, status=403)
    
    claim = get_object_or_404(Claim, pk=pk)
    new_status = request.POST.get('status')
    assigned_to_id = request.POST.get('assigned_to')
    
    if new_status not in dict(Claim.STATUS_CHOICES):
        return JsonResponse({'error': 'Estado inválido'}, status=400)
    
    old_status = claim.status
    claim.status = new_status
    
    # RF18: Asignar a empleado
    if assigned_to_id:
        try:
            assigned_user = User.objects.get(id=assigned_to_id, is_staff=True)
            claim.assigned_to = assigned_user
        except User.DoesNotExist:
            pass
    
    claim.save()
    
    # Crear registro en historial - RF14
    ClaimHistory.objects.create(
        claim=claim,
        old_status=old_status,
        new_status=new_status,
        changed_by=request.user
    )
    
    # Registrar actividad del admin - RF23
    AdminActivity.objects.create(
        user=request.user,
        claim=claim,
        action=f"Estado cambió de {old_status} a {new_status}",
        description=f"Cambio de estado realizado"
    )
    
    # RF8: Enviar notificación
    status_label = dict(Claim.STATUS_CHOICES).get(new_status)
    _create_notification(
        claim,
        f"El estado de tu reclamo {claim.number} ha cambiado a: {status_label}"
    )
    
    messages.success(request, "Estado actualizado correctamente")
    return redirect("claims:admin_list")


@login_required
def admin_reports(request):
    """Generar reportes - RF16: Por zonas, fechas, prioridades"""
    if not is_admin(request.user):
        messages.error(request, "No tienes permisos para acceder a este panel")
        return redirect("claims:index")
    
    export_format = request.GET.get('export')
    
    claims = Claim.objects.all()
    zone_filter = request.GET.get('zone')
    priority_filter = request.GET.get('priority')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if zone_filter:
        claims = claims.filter(zone__icontains=zone_filter)
    if priority_filter:
        claims = claims.filter(priority=priority_filter)
    if date_from:
        claims = claims.filter(created_at__date__gte=date_from)
    if date_to:
        claims = claims.filter(created_at__date__lte=date_to)
    
    if export_format == 'csv':
        return _export_csv(claims)
    elif export_format == 'pdf':
        return _export_pdf(claims)
    
    return render(request, "claims/admin_reports.html", {"claims": claims})


def _export_csv(claims):
    """RF17: Exportar a CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reclamos.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Número', 'Nombre', 'Pedido', 'Contacto', 'Zona', 'Prioridad', 'Estado', 'Fecha'])
    
    for claim in claims:
        writer.writerow([
            claim.number,
            claim.full_name,
            claim.order_number or '',
            claim.contact,
            claim.zone,
            claim.get_priority_display(),
            claim.get_status_display(),
            claim.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response


def _export_pdf(claims):
    """RF17: Exportar a PDF"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from io import BytesIO
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
        )
        
        # Título
        title = Paragraph("Reporte de Reclamos", title_style)
        elements.append(title)
        
        # Tabla
        data = [['Número', 'Nombre', 'Zona', 'Prioridad', 'Estado', 'Fecha']]
        for claim in claims:
            data.append([
                claim.number,
                claim.full_name,
                claim.zone,
                claim.get_priority_display(),
                claim.get_status_display(),
                claim.created_at.strftime('%Y-%m-%d')
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reclamos.pdf"'
        return response
    except ImportError:
        messages.error(None, "ReportLab no está instalado. Instálalo con: pip install reportlab")
        return redirect("claims:admin_reports")


@login_required
def admin_activities(request):
    """Ver historial de actividades del admin - RF23"""
    if not is_admin(request.user):
        messages.error(request, "No tienes permisos")
        return redirect("claims:index")
    
    activities = AdminActivity.objects.all()
    return render(request, "claims/admin_activities.html", {"activities": activities})


def faq_list(request):
    """Lista de preguntas frecuentes - RF24"""
    faqs = FAQ.objects.filter(is_active=True)
    return render(request, "claims/faq_list.html", {"faqs": faqs})


@login_required
def manage_faqs(request):
    """Gestionar FAQs para administrador - RF24"""
    if not is_admin(request.user):
        return redirect("claims:index")
    
    faqs = FAQ.objects.all()
    return render(request, "claims/manage_faqs.html", {"faqs": faqs})


@login_required
def add_faq(request):
    """Agregar FAQ"""
    if not is_admin(request.user):
        return redirect("claims:index")
    
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "FAQ agregado exitosamente")
            return redirect("claims:manage_faqs")
    else:
        form = FAQForm()
    
    return render(request, "claims/add_faq.html", {"form": form})


@login_required
def edit_faq(request, pk):
    """Editar FAQ"""
    if not is_admin(request.user):
        return redirect("claims:index")
    
    faq = get_object_or_404(FAQ, pk=pk)
    
    if request.method == "POST":
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, "FAQ actualizado exitosamente")
            return redirect("claims:manage_faqs")
    else:
        form = FAQForm(instance=faq)
    
    return render(request, "claims/edit_faq.html", {"form": form})


@login_required
def delete_faq(request, pk):
    """Eliminar FAQ"""
    if not is_admin(request.user):
        return redirect("claims:index")
    
    faq = get_object_or_404(FAQ, pk=pk)
    faq.delete()
    messages.success(request, "FAQ eliminado exitosamente")
    return redirect("claims:manage_faqs")


def _create_notification(claim, message):
    """Crear notificación para un reclamo - RF8, RF9, RF10"""
    email = claim.email or claim.contact if '@' in claim.contact else None
    phone = claim.phone or claim.contact if claim.contact and '@' not in claim.contact else None
    
    if email:
        Notification.objects.create(
            claim=claim,
            user_email=email,
            notification_type='email',
            message=message
        )
        # Aquí se enviaría el email en producción
    
    if claim.priority == 'urgent' and phone:
        Notification.objects.create(
            claim=claim,
            user_phone=phone,
            notification_type='sms',
            message=message
        )
        # Aquí se enviaría el SMS en producción


# ---------------------------
#  SISTEMA DE AUTENTICACIÓN
# ---------------------------

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("claims:index")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "claims/login.html")


def user_logout(request):
    logout(request)
    return redirect("claims:index")


def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        # Validaciones
        if not username or not email or not password:
            messages.error(request, "Todos los campos son obligatorios")
            return render(request, "claims/registrer.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe")
            return render(request, "claims/registrer.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado")
            return render(request, "claims/registrer.html")

        if password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "claims/registrer.html")

        if len(password) < 8:
            messages.error(request, "La contraseña debe tener al menos 8 caracteres")
            return render(request, "claims/registrer.html")

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Cuenta creada exitosamente. ¡Inicia sesión!")
            return redirect("claims:login")
        except Exception as e:
            messages.error(request, f"Error al crear la cuenta: {str(e)}")
            return render(request, "claims/registrer.html")

    return render(request, "claims/registrer.html")
