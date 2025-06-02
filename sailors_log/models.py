from django.db import models

class Boat(models.Model):
    name = models.CharField(max_length=100)
    info_url = models.URLField("Weitere Informationen", blank=True)

    year_built = models.PositiveIntegerField("Baujahr", null=True, blank=True)
    length_m = models.FloatField("Länge (m)", null=True, blank=True)
    beam_m = models.FloatField("Breite (m)", null=True, blank=True)
    draft_m = models.FloatField("Tiefgang (m)", null=True, blank=True)
    displacement_kg = models.PositiveIntegerField("Verdrängung (kg)", null=True, blank=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    title = models.CharField(max_length=200)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    date = models.DateField()
    gpx_file = models.FileField(upload_to='tracks/')
    description = models.TextField(blank=True)

    # automatisch befüllt beim Upload
    distance_nm = models.FloatField("Distanz (Seemeilen)", null=True, blank=True)
    duration = models.DurationField("Dauer", null=True, blank=True)

    def __str__(self):
        return f"{self.date} – {self.title}"