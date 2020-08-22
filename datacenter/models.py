from django.db import models
import django.utils.timezone


def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds // 60) % 60
    return f"{hours:02d}:{minutes:02d}"


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )

    def get_duration(self):
        leaved_at = django.utils.timezone.localtime(self.leaved_at) if self.leaved_at else django.utils.timezone.now()
        delta = leaved_at - django.utils.timezone.localtime(self.entered_at)
        total_seconds = delta.total_seconds()
        return int(total_seconds)

    def is_long(self, minutes=60):
        duration = self.get_duration()
        if duration // 60 > minutes:
            return True
        return False
