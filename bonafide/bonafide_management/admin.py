from django.contrib import admin
from django.contrib import admin
from .models import Student, CustomUser, Student_Registration



class StudentAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Fathers_Name', 'Email', 'Department_Choice', 'Passing_Year', 'Application_Status')
    search_fields = ('Name', 'Fathers_Name', 'Email', 'University_Roll_Number')
    actions = ['mark_as_approved']

    fieldsets = (
        ('Basic Information', {
            'fields': ('Name', 'Fathers_Name', 'Email', 'Phone', 'University_Roll_Number'),
        }),
        ('Academic Details', {
            'fields': ('Department_Choice', 'Passing_Year'),
        }),
        ('Purpose', {
            'fields': ('Write_Purpose',),
        }),
        ('Status', {
            'fields': ('Application_Status',),
        }),
    )
    readonly_fields = ('Application_Status',)

    def mark_as_approved(modeladmin, request, queryset):
        queryset.update(Application_Status=1)
    mark_as_approved.short_description = "Mark selected entries as approved"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.Application_Status = 0
        super().save_model(request, obj, form, change)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # ... rest of the code ...
    list_display = ('Name', 'Fathers_Name', 'Email', 'Department_Choice', 'Passing_Year', 'Application_Status')
    search_fields = ('Name', 'Fathers_Name', 'Email', 'University_Roll_Number')
    actions = ['mark_as_approved']

# Custom admin class for CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'student_id', 'email', 'is_staff', 'is_active', 'date_joined')

admin.site.register(CustomUser)

class Student_RegistrationAdmin(admin.ModelAdmin):
    list_display = ('Name','email')

admin.site.register(Student_Registration)