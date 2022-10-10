from distutils.command.upload import upload
from django.db import models
from criminal.models import Criminal
# Create your models here.
class Case(models.Model):
    case_cover = models.FileField(upload_to='case',null=True)
    case_name = models.CharField(max_length=50)
    case_desc = models.TextField(max_length=1000,default="No Case Description added yet.")
    case_date = models.DateTimeField(auto_now_add=True,blank=True )
    criminals = models.ManyToManyField(Criminal)
    # suspects = models.ForeignKey('')

    def __str__(self):
        return str(self.case_name)