from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.
class course(models.Model):
    course_code=models.CharField(primary_key=True,max_length=8)
    course_title=models.CharField(max_length=120)
    l_credits=models.IntegerField()
    t_credits=models.IntegerField()
    p_credits=models.IntegerField()
    j_credits=models.IntegerField()

class teacher(models.Model):
    name=models.CharField(max_length=120)
    emp_code=models.CharField(max_length=5,primary_key=True)
    school=models.CharField(max_length=3)
class slot(models.Model):
    class Meta:
        unique_together = (('slot_name', 'slot_id'))
    slot_id=models.CharField(max_length=2)
    slot_name=models.CharField(max_length=5)
class offering(models.Model):
    offer_id=models.IntegerField(primary_key=True)
    emp_code=models.ForeignKey(teacher,on_delete=models.CASCADE)
    course_code=models.ForeignKey(course,on_delete=models.CASCADE)
class offer_set(models.Model):
    class Meta:
        unique_together = (('offer_id', 'slot_id'))
    slot_id=models.ForeignKey(slot,on_delete=models.CASCADE)
    offer_id=models.ForeignKey(offering,on_delete=models.CASCADE)
