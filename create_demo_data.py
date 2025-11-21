import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reclamos_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from claims.models import Claim, FAQ
from datetime import datetime, timedelta
import random

def create_demo_data():
    """Crear datos de demostración para pruebas"""
    
    print("🔄 Creando datos de demostración...")
    
    # 1. Crear usuario admin si no existe
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@reclamos.com', 'admin123')
        print("✅ Usuario admin creado: admin/admin123")
    else:
        print("✅ Usuario admin ya existe")
    
    # 2. Crear usuarios staff
    for i in range(1, 4):
        username = f'empleado{i}'
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=f'{username}@reclamos.com',
                password='empleado123',
                first_name=f'Empleado',
                last_name=f'{i}'
            )
            user.is_staff = True
            user.save()
            print(f"✅ Usuario staff creado: {username}/empleado123")
    
    # 3. Crear clientes
    for i in range(1, 4):
        username = f'cliente{i}'
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=f'cliente{i}@email.com',
                password='cliente123'
            )
            print(f"✅ Usuario cliente creado: {username}/cliente123")
    
    # 4. Crear reclamos de prueba
    zones = ['Centro', 'Norte', 'Sur', 'Este', 'Oeste', 'Barrio Latino', 'Zona Industrial']
    statuses = ['pending', 'processing', 'resolved', 'closed']
    priorities = ['normal', 'urgent']
    
    admin = User.objects.get(username='admin')
    
    for i in range(1, 11):
        claim_number = f'R-{chr(65 + (i % 26))}{chr(66 + ((i+1) % 26))}{chr(67 + ((i+2) % 26))}{1000 + i}'
        
        if not Claim.objects.filter(number=claim_number).exists():
            claim = Claim.objects.create(
                number=claim_number,
                full_name=f'Cliente Prueba {i}',
                email=f'cliente{i}@prueba.com',
                phone=f'555-{1000 + i}',
                contact=f'cliente{i}@prueba.com',
                description=f'Problema de prueba número {i}. Este es un reclamo generado automáticamente para demostración.',
                order_number=f'PED-{10000 + i}',
                priority=random.choice(priorities),
                zone=random.choice(zones),
                status=random.choice(statuses),
                created_at=datetime.now() - timedelta(days=random.randint(0, 30)),
                created_by=admin if i % 2 == 0 else None,
                assigned_to=random.choice(User.objects.filter(is_staff=True, is_superuser=False))
            )
            print(f"✅ Reclamo creado: {claim.number}")
    
    # 5. Cargar FAQs si no existen
    faqs_count = FAQ.objects.filter(is_active=True).count()
    if faqs_count == 0:
        from claims.management.commands.load_faqs import Command
        Command().handle()
        print("✅ FAQs cargadas correctamente")
    else:
        print(f"✅ FAQs ya existen ({faqs_count})")
    
    print("\n" + "="*60)
    print("🎉 DATOS DE DEMOSTRACIÓN CREADOS EXITOSAMENTE")
    print("="*60)
    print("\n📋 USUARIOS DISPONIBLES PARA PRUEBA:\n")
    print("ADMINISTRADOR:")
    print("  Usuario: admin")
    print("  Contraseña: admin123")
    print("  Email: admin@reclamos.com\n")
    
    print("EMPLEADOS (Staff):")
    for i in range(1, 4):
        print(f"  Usuario: empleado{i}")
        print(f"  Contraseña: empleado123")
        print(f"  Email: empleado{i}@reclamos.com")
    
    print("\nCLIENTES:")
    for i in range(1, 4):
        print(f"  Usuario: cliente{i}")
        print(f"  Contraseña: cliente123")
        print(f"  Email: cliente{i}@email.com")
    
    print("\n" + "="*60)
    print("🚀 Para probar la aplicación:")
    print("="*60)
    print("\n1. Inicia el servidor:")
    print("   python manage.py runserver\n")
    print("2. Accede a: http://127.0.0.1:8000/\n")
    print("3. Prueba las siguientes funciones:\n")
    print("   • Registrar reclamo (sin login)")
    print("   • Buscar reclamo (con número)")
    print("   • Iniciar sesión como cliente")
    print("   • Ver 'Mis reclamos'")
    print("   • Iniciar sesión como admin")
    print("   • Acceder a 'Panel Admin'")
    print("   • Filtrar reclamos")
    print("   • Cambiar estado")
    print("   • Generar reportes (CSV/PDF)")
    print("\n" + "="*60)

if __name__ == '__main__':
    create_demo_data()
