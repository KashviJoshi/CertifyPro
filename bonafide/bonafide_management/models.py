from django.db import models
from django.conf import settings
# Create your models here.
from django.contrib.auth.models import User, Group , AbstractUser
from django.db import models
from phone_field import PhoneField
# from datetime import date, timezone
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.CharField(max_length=100, blank=True, null=True)
    # Add other fields as needed

    def __str__(self):
        return self.email 

class Student(models.Model):
    Name = models.CharField(max_length=100)
    Fathers_Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    DEPARTMENT_CHOICES = [
        ('computer_science', 'Computer_Science'),
        ('electronics_and_communication', 'Electronics_and_Communication'),
        ('master_of_computer_application', 'Master_of_Computer_Application'),
    ]

    Department_Choice = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default='computer_science',  # You can set a default option if needed
    )
    PASSING_YEAR = [
        ('2024', '2024'),
        ('2023', '2023'),
        ('2022', '2022'),
        ('2021', '2021'),
        ('2020', '2020'),
    ]

    Passing_Year = models.CharField(
        max_length=20,
        choices=PASSING_YEAR,
        default='2024',  # You can set a default option if needed
    )
    Phone = PhoneField(blank=True, help_text="Contact phone number")
    # Date = models.DateTimeField(default=timezone.now)
    University_Roll_Number=models.IntegerField()
    Write_Purpose=models.CharField(max_length=225)

    Application_Date = models.DateTimeField(default=timezone.now)  # Rename Date to application_date

    APPLICATION_STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Approved'),
        (-1, 'Rejected'),
    ]
    Application_Status = models.IntegerField(default=0, choices=APPLICATION_STATUS_CHOICES)
    # 0 => pending    # 1 => approved     # -1 => rejected
    
    # Add more fields as per your requirements
    def __str__(self):
        return self.Name
    

class Student_Registration(models.Model):
    UserName = models.CharField(max_length=100, default='')
    Password = models.CharField(max_length=100)
    Email = models.EmailField(default='')
    # Phone = PhoneField(blank=True, help_text="Conatct number")

    def __str__(self) :
        return self.UserName


class Role(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role_choices = [
        ("student", "Student"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=role_choices)

    def __str__(self):
        return f"{self.user.username}'s role: {self.role}"

# Group.objects.get_or_create(name="associate")
# Group.objects.get_or_create(name="student")
# Group.objects.get_or_create(name="admin")


class BonafideManagementPermissions(models.Model):
    class Meta:
        permissions = [
            ("create_bonafide", "Can create bonafide"),
            ("update_bonafide", "Can update bonafide"),
            ("delete_bonafide", "Can delete bonafide"),
        ]


