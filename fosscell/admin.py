from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Institution,ProgramMode,ProgramType,AudienceType,Activity,Category,UniversityBoard,InstitutionReg,FossAdvisor,Members
# Register your models here.
class UserAdmin(BaseUserAdmin):
    fieldsets=(
        (None,{'fields':('institution','email','password','name','last_login')}),
        ('Permissions',{'fields':(
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets=(
        (
            None,
            {
                'classes':('wide',),
                'fields':('institution','email','password1','password2')
            }
        ),
    )

    list_display = ('email','institution','name', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
admin.site.register(Institution)
admin.site.register(ProgramMode)
admin.site.register(ProgramType)
admin.site.register(AudienceType)
admin.site.register(Activity)
admin.site.register(Category)
admin.site.register(UniversityBoard)
admin.site.register(InstitutionReg)
admin.site.register(FossAdvisor)
admin.site.register(Members)
