from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

class Claim(models.Model):
    PRIORITY_CHOICES = (
        ('normal', 'Normal'),
        ('urgent', 'Urgente'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('processing', 'En proceso'),
        ('resolved', 'Resuelto'),
        ('closed', 'Cerrado'),
    )

    number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    order_number = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    contact = models.CharField(max_length=200)
    description = models.TextField()
    evidence = models.ImageField(upload_to='evidences/', blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    zone = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='claims'
    )
    assigned_to = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_claims'
    )

    def __str__(self):
        return f"{self.number} - {self.full_name}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['number']),
            models.Index(fields=['order_number']),
            models.Index(fields=['status']),
            models.Index(fields=['zone']),
        ]


class ClaimHistory(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    change_date = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.claim.number} - {self.old_status} → {self.new_status}"
    
    class Meta:
        ordering = ['-change_date']


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('email', 'Correo'),
        ('sms', 'SMS'),
        ('in_app', 'En la App'),
    )

    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='notifications')
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=20, blank=True, null=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    message = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.notification_type} - {self.claim.number}"
    
    class Meta:
        ordering = ['-created_at']


class AdminActivity(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='activities')
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, null=True, blank=True, related_name='admin_activities')
    action = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.claim.number if self.claim else 'N/A'}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Admin Activities"


class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "FAQs"

