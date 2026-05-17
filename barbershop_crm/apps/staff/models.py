from django.db import models
from django.contrib.auth.models import User


class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Master(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='master_profile'
    )
    display_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='staff/photos/', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    specializations = models.ManyToManyField(Specialization, blank=True)
    color = models.CharField(
        max_length=7, default='#c9a84c',
        help_text='Hex color used in calendar'
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    is_active = models.BooleanField(default=True)
    hire_date = models.DateField(null=True, blank=True)
    calendar_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['calendar_order', 'display_name']

    def __str__(self):
        return self.display_name

    @property
    def rating_stars(self):
        """Returns (filled_count, empty_count) for 5-star display."""
        filled = round(float(self.rating))
        return filled, 5 - filled


class WorkSchedule(models.Model):
    WEEKDAYS = [
        (0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'),
        (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота'), (6, 'Воскресенье'),
    ]
    master = models.ForeignKey(
        Master, on_delete=models.CASCADE, related_name='schedules'
    )
    weekday = models.SmallIntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_day_off = models.BooleanField(default=False)

    class Meta:
        unique_together = ('master', 'weekday')
        ordering = ['weekday', 'start_time']

    def __str__(self):
        return f"{self.master} — {self.get_weekday_display()}"


class DayOff(models.Model):
    master = models.ForeignKey(
        Master, on_delete=models.CASCADE, related_name='days_off'
    )
    date = models.DateField()
    reason = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('master', 'date')

    def __str__(self):
        return f"{self.master} — {self.date}"
