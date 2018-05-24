from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    funds_raised = models.IntegerField()

    def __str__(self):
        return self.name
