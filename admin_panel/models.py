from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import User
from store.models import City, Mantaghe, Province

# Create your models here.


class Staff(models.Model):

    class StaffGender(models.TextChoices):
        MALE = 'm', _('مرد')
        FEMALE = 'f', _('زن')

    class StaffMadrak(models.TextChoices):
        DIPLOM = 'di', _('دیپلم')
        FOQ_DIPLOM = 'fd', _('فوق دیپلم')
        LISANS = 'li', _('لیسانس')
        FOQ_LISANS = 'fl', _('فوق لیسانس')
        DOCTORA = 'do', _('دکترا')

    class NezamVazifeStatus(models.TextChoices):
        MOAAF = 'mo', _('معاف')
        ETMAM_KHEDMAT = 'et', _('اتمام خدمت')

    class SkillStatus(models.TextChoices):
        VERY_GOOD = 'vg', _('خیلی خوب')
        GOOD = 'g', _('خوب')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staffs', null=True)

    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=StaffGender.choices)
    code_melli = models.CharField(max_length=10)
    mobile = models.CharField(max_length=11)
    email = models.EmailField()
    madrak_grade = models.CharField(max_length=2, choices=StaffMadrak.choices)
    nezam_vazife_status = models.CharField(max_length=3, choices=NezamVazifeStatus.choices)

    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    mantaghe = models.ForeignKey(Mantaghe, on_delete=models.SET_NULL, null=True)
    mahalle = models.CharField(max_length=255)
    address = models.CharField(max_length=600)
    post_code = models.CharField(max_length=10)

    img_personelly = models.ImageField(upload_to='admin_panel/staffs/img_personelly/%Y/%m/%d/')
    kart_melli = models.ImageField(upload_to='admin_panel/staffs/kart_melli/%Y/%m/%d/')
    shenasname = models.ImageField(upload_to='admin_panel/staffs/shenasname/%Y/%m/%d/')
    img_madrak = models.ImageField(upload_to='admin_panel/staffs/img_madrak/%Y/%m/%d/')
    police_clearance = models.ImageField(upload_to='admin_panel/staffs/police_clearance/%Y/%m/%d/')
    payan_khedmat_img = models.ImageField(upload_to='admin_panel/staffs/payan_khedmat_img/%Y/%m/%d/')

    english_status = models.CharField(max_length=2, choices=SkillStatus.choices)
    computer_icdl_status = models.CharField(max_length=2, choices=SkillStatus.choices)
    accounting = models.CharField(max_length=2, choices=SkillStatus.choices)
    digital_marketing = models.CharField(max_length=2, choices=SkillStatus.choices)
    photo_and_movie_skills = models.CharField(max_length=2, choices=SkillStatus.choices)
    areas_of_cooperation = models.CharField(max_length=25)
    working_conditions = models.CharField(max_length=555)
    minimum_salary_requested = models.IntegerField()
    
    class Meta:
        permissions = [
            ('web_mail', 'you can access to web mail page')
        ]
