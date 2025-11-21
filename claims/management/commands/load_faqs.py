from django.core.management.base import BaseCommand
from claims.models import FAQ

class Command(BaseCommand):
    help = 'Carga preguntas frecuentes iniciales'

    def handle(self, *args, **options):
        faqs_data = [
            {
                'question': '¿Cómo registrar un reclamo?',
                'answer': 'Para registrar un reclamo:\n1. Haz clic en "Registrar Reclamo"\n2. Completa el formulario con tus datos personales\n3. Describe detalladamente tu problema\n4. Adjunta evidencia si es posible\n5. Haz clic en "Registrar Reclamo"\n\nRecuerda guardar tu número de reclamo para futuras consultas.',
                'order': 1
            },
            {
                'question': '¿Necesito crear una cuenta para registrar un reclamo?',
                'answer': 'No es obligatorio. Puedes registrar un reclamo sin tener una cuenta. Solo necesitas proporcionar un correo electrónico o número de teléfono para que podamos contactarte.\n\nSi tienes una cuenta, tu reclamo se asociará automáticamente a tu perfil.',
                'order': 2
            },
            {
                'question': '¿Cómo buscar mi reclamo?',
                'answer': 'Puedes buscar tu reclamo de dos formas:\n1. Usando el número de reclamo (ej: R-ABC12345) que recibiste al registrarlo\n2. Usando el número de pedido relacionado con tu reclamo\n\nAmbas opciones están disponibles en la sección "Buscar Reclamo".',
                'order': 3
            },
            {
                'question': '¿Cuáles son los estados posibles de un reclamo?',
                'answer': 'Un reclamo puede tener los siguientes estados:\n• Pendiente: Acaba de ser registrado\n• En Proceso: Estamos revisando tu reclamo\n• Resuelto: Tu reclamo ha sido solucionado\n• Cerrado: El reclamo se ha cerrado',
                'order': 4
            },
            {
                'question': '¿Cómo recibo notificaciones sobre mi reclamo?',
                'answer': 'Te enviaremos notificaciones cuando:\n• Tu reclamo sea registrado\n• El estado de tu reclamo cambie\n• Tu reclamo sea resuelto\n\nLas notificaciones se enviarán al correo o teléfono que proporcionaste.',
                'order': 5
            },
            {
                'question': '¿Puedo adjuntar una foto a mi reclamo?',
                'answer': 'Sí, puedes adjuntar fotos o capturas de pantalla como evidencia. Esto ayuda a agilizar el proceso de revisión. Las imágenes deben estar en formatos comunes como JPG, PNG, etc.',
                'order': 6
            },
            {
                'question': '¿Qué es la prioridad de un reclamo?',
                'answer': 'La prioridad indica la urgencia del reclamo:\n• Normal: Casos regulares que se resuelven en tiempo estándar\n• Urgente: Casos que requieren atención inmediata (ej: servicios no prestados, situaciones críticas)\n\nLos reclamos urgentes pueden recibir una llamada telefónica adicional.',
                'order': 7
            },
            {
                'question': '¿Cuánto tiempo tarda en resolverse un reclamo?',
                'answer': 'El tiempo de resolución depende de la naturaleza del reclamo:\n• Reclamos urgentes: 24-48 horas\n• Reclamos normales: 5-10 días hábiles\n\nTe mantendremos informado sobre el progreso de tu reclamo.',
                'order': 8
            },
            {
                'question': '¿Puedo editar mi reclamo después de registrarlo?',
                'answer': 'Una vez que registres un reclamo, no puedes editarlo directamente. Sin embargo, puedes contactar a nuestro equipo de soporte para proporcionar información adicional o aclaraciones.',
                'order': 9
            },
            {
                'question': '¿Hay costo por registrar un reclamo?',
                'answer': 'No, el servicio de reclamos es completamente gratuito. No hay cargos de ningún tipo por registrar, revisar o resolver tu reclamo.',
                'order': 10
            }
        ]

        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults={
                    'answer': faq_data['answer'],
                    'order': faq_data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ FAQ creado: {faq_data["question"][:50]}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ FAQ ya existe: {faq_data["question"][:50]}'))

        self.stdout.write(self.style.SUCCESS('✓ Todos los FAQs han sido cargados'))
