from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.PROTECT, related_name='services'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.PositiveSmallIntegerField(help_text='Duration in minutes')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)
    masters = models.ManyToManyField(
        'staff.Master', blank=True, related_name='services'
    )

    class Meta:
        ordering = ['category__order', 'order', 'name']

    def __str__(self):
        return f"{self.name} ({self.duration} мин)"

    @property
    def duration_display(self):
        if self.duration >= 60:
            h = self.duration // 60
            m = self.duration % 60
            return f"{h}ч {m}мин" if m else f"{h}ч"
        return f"{self.duration} мин"
