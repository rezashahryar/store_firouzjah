from rest_framework import serializers
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from admin_panel import models
from core.models import User
from store.models import City, Mantaghe, Province

# create your serializers here

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        # for gender choices
        elif obj == 'm':
            return 'مرد'
        elif obj == 'f':
            return 'زن'
        # for madrak grade
        elif obj == 'di':
            return 'دیپلم'
        elif obj == 'fd':
            return 'فوق دیپلم'
        elif obj == 'li':
            return 'لیسانس'
        elif obj == 'fl':
            return 'فوق لیسانس'
        elif obj == 'do':
            return 'دکترا'
        # for nezam vazife status
        elif obj == 'mo':
            return 'معاف'
        elif obj == 'et':
            return 'اتمام خدمت'
        # for skill grade
        elif obj == 'vg':
            return 'خیلی خوب'
        elif obj == 'g':
            return 'خوب'
                
        return self._choices[obj]
    

class StaffProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Province
        fields = ['name']


class StaffCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['name']


class StaffMantagheSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mantaghe
        fields = ['name']


class UserPermissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name']


class UserStaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile']


class StaffSerializer(serializers.ModelSerializer):
    gender = ChoiceField(choices=models.Staff.StaffGender)
    madrak_grade = ChoiceField(choices=models.Staff.StaffMadrak)
    nezam_vazife_status = ChoiceField(choices=models.Staff.NezamVazifeStatus)

    english_status = ChoiceField(choices=models.Staff.SkillStatus)
    computer_icdl_status = ChoiceField(choices=models.Staff.SkillStatus)
    accounting = ChoiceField(choices=models.Staff.SkillStatus)
    digital_marketing = ChoiceField(choices=models.Staff.SkillStatus)
    photo_and_movie_skills = ChoiceField(choices=models.Staff.SkillStatus)

    # user_permissions = serializers.SerializerMethodField()

    class Meta:
        model = models.Staff
        fields = [
            'user', 'full_name', 'gender', 'code_melli', 'mobile', 'email', 'madrak_grade', 'nezam_vazife_status',
            'province', 'city', 'mantaghe', 'mahalle', 'address', 'post_code', 'img_personelly', 'kart_melli',
            'shenasname', 'img_madrak', 'police_clearance', 'payan_khedmat_img', 'english_status', 'computer_icdl_status',
            'accounting', 'digital_marketing', 'photo_and_movie_skills', 'areas_of_cooperation',
            'working_conditions', 'minimum_salary_requested'
        ]
        extra_kwargs = {
            'gender': {'required': True}
        }
    
    # def get_user_permissions(self, obj):
    #     print(obj.user.user_permissions.all())
    #     return obj.user.user_permissions.all()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['province'] = StaffProvinceSerializer(instance.province).data
        rep['city'] = StaffCitySerializer(instance.city).data
        rep['mantaghe'] = StaffMantagheSerializer(instance.mantaghe).data
        rep['user'] = UserStaffSerializer(instance.user).data
        rep['user_permissions'] = UserPermissionsSerializer(instance.user.user_permissions.all()[4:], many=True).data

        return rep
    

class ListPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['codename', 'name']
