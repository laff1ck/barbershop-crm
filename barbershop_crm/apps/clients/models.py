from django.db import models


class LoyaltyTier(models.TextChoices):
    BRONZE   = 'bronze',   'Бронза'
    SILVER   = 'silver',   'Серебро'
    GOLD     = 'gold',     'Золото'
    PLATINUM = 'platinum', 'Платина'


TIER_THRESHOLDS = {
    LoyaltyTier.PLATINUM: 50000,
    LoyaltyTier.GOLD:     20000,
    LoyaltyTier.SILVER:   5000,
}

TIER_COLORS = {
    LoyaltyTier.BRONZE:   '#cd7f32',
    LoyaltyTier.SILVER:   '#c0c0c0',
    LoyaltyTier.GOLD:     '#c9a84c',
    LoyaltyTier.PLATINUM: '#e5e4e2',
}


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    phone      = models.CharField(max_length=20, unique=True)
    email      = models.EmailField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photo      = models.ImageField(upload_to='clients/photos/', blank=True)

    loyalty_tier    = models.CharField(
        max_length=20, choices=LoyaltyTier.choices, default=LoyaltyTier.BRONZE
    )
    loyalty_points  = models.PositiveIntegerField(default=0)
    total_spent     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    visit_count     = models.PositiveIntegerField(default=0)
    notes           = models.TextField(blank=True)
    preferred_master = models.ForeignKey(
        'staff.Master', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='preferred_clients',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_visit = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['last_name', 'first_name']),
        ]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        # last_name = "Иванов", first_name = "Иван Иванович"
        return f"{self.last_name} {self.first_name}"

    @property
    def short_name(self):
        """Иванов И.И."""
        parts = self.first_name.split()
        initials = ''.join(p[:1] + '.' for p in parts)
        return f"{self.last_name} {initials}"

    @property
    def initials(self):
        last = self.last_name[:1] if self.last_name else ''
        first = self.first_name[:1] if self.first_name else ''
        return (last + first).upper()

    @property
    def tier_color(self):
        return TIER_COLORS.get(self.loyalty_tier, '#c9a84c')

    def recalculate_tier(self):
        spent = float(self.total_spent)
        if spent >= TIER_THRESHOLDS[LoyaltyTier.PLATINUM]:
            self.loyalty_tier = LoyaltyTier.PLATINUM
        elif spent >= TIER_THRESHOLDS[LoyaltyTier.GOLD]:
            self.loyalty_tier = LoyaltyTier.GOLD
        elif spent >= TIER_THRESHOLDS[LoyaltyTier.SILVER]:
            self.loyalty_tier = LoyaltyTier.SILVER
        else:
            self.loyalty_tier = LoyaltyTier.BRONZE
        self.save(update_fields=['loyalty_tier'])
