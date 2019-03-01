from django.db import models

GENDER = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
    ('OTHER', 'OTHER'),
)


class Guardian(models.Model):
    # parent's bio
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    id_number = models.CharField(max_length=255, unique=True, null=True, blank=True)  # noqa E501
    religion = models.CharField(max_length=255, null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDER, null=True, blank=True)  # noqa E501
    profession = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.full_name}'


class Subject(models.Model):
    # subject details
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Teacher(models.Model):
    # teacher's bio
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    id_number = models.CharField(max_length=255, unique=True, null=True, blank=True)  # noqa E501
    religion = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDER, null=True, blank=True)  # noqa E501
    DOB = models.DateField(null=True, blank=True)
    joined_at = models.DateField(null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    active = models.BooleanField(default=True)

    # the underscore is for differentiating it with the subjects column
    def subjects_(self):
        return "\n".join([subject.name for subject in self.subjects.all()])

    def __str__(self):
        return f'{self.full_name}'


class ClassRoom(models.Model):
    # class details
    name = models.CharField(max_length=255, unique=True)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Student(models.Model):
    # student's bio
    full_name = models.CharField(max_length=255)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=255, unique=True, null=True, blank=True)  # noqa E501
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)
    joined_at = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDER, null=True, blank=True)  # noqa E501
    religion = models.CharField(max_length=255, null=True, blank=True)
    guardians = models.ManyToManyField(Guardian, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.full_name}'
