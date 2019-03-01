from django.contrib import admin

from .models import Guardian, Teacher, Student, Subject, ClassRoom


class GuardianModel(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone',
        'email',
    )

    list_filter = (
        'gender',
        'active'
    )

    list_display_links = ('full_name', )
    search_fields = (
        'full_name',
        'phone',
        'email',
        'id_number',
        'religion',
        'DOB',
        'profession',
    )

    fieldsets = (
        ('BIO', {
            'fields': ('full_name',
                       'email', 'phone', 'id_number', 'religion', 'DOB',
                       'gender', 'profession', 'active')
        }),

    )


class TeacherModel(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone',
        'email',
        'subjects_',
    )
    list_filter = ('gender', 'active', 'joined_at', 'subjects')

    list_display_links = ('full_name', )
    search_fields = (
        'full_name',
        'phone',
        'email',
        'id_number',
        'religion',
        'DOB',
        'joined_at',
        'subjects',
    )

    fieldsets = (('BIO', {
        'fields': ('full_name', 'email', 'phone', 'id_number', 'religion',
                   'DOB', 'gender', 'joined_at', 'subjects', 'active')
    }), )


class StudentModel(admin.ModelAdmin):
    list_display = (
        'full_name',
        'registration_number',
        'class_room',
    )

    list_filter = ('gender', 'class_room', 'active')

    list_display_links = ('full_name', 'registration_number')
    search_fields = (
        'full_name',
        'class_room',
        'registration_number',
        'phone',
        'email',
        'religion',
        'DOB',
        'joined_at',
        'guardians',
    )

    fieldsets = (('BIO', {
        'fields':
        ('full_name', 'class_room', 'registration_number', 'email', 'phone',
         'religion', 'DOB', 'gender', 'guardians', 'active')
    }), )


class SubjectModel(admin.ModelAdmin):
    pass


class ClassModel(admin.ModelAdmin):
    pass


admin.site.register(Guardian, GuardianModel)
admin.site.register(Teacher, TeacherModel)
admin.site.register(Student, StudentModel)
admin.site.register(Subject, SubjectModel)
admin.site.register(ClassRoom, ClassModel)
