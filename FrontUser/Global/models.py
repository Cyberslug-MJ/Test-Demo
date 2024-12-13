from django.db import models
from django.db import models
import datetime
from accounts.models import CustomUser as User
import uuid 


class Announcements(models.Model):
    audience = (
    ("Parents","Parents"),
    ("Teachers","Teachers"),
    ("Students","Students"),
    ("Everyone","Everyone"),
    )
    LEVEL = (
        ("HIGH","HIGH"),
        ("LOW","LOW"),
        ("MEDIUM","MEDIUM")
    )
    title = models.CharField(max_length=128)
    body = models.TextField(max_length=150)
    audiences = models.CharField(max_length=8,choices=audience,default="Everyone")
    scheduled_for = models.DateField(default=datetime.datetime.now)
    priority = models.CharField(max_length=6,choices=LEVEL,verbose_name='priority',default="LOW")
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "Announcements"
    
    def __str__(self):
        return self.title


class StudentClasses(models.Model):
    name = models.CharField(max_length=50,unique=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = "student classes"
    

class subclasses(models.Model):
    name = models.CharField(max_length=100,unique=True)
    Grade = models.ForeignKey(StudentClasses,on_delete=models.CASCADE,verbose_name='associated grade',null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="date created")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="last modified")

    def __str__(self):
        return f"{self.Grade.name}-{self.name}"


class subjects(models.Model):
    name = models.CharField(verbose_name='name of subject',max_length=100,unique=True)
    classes = models.ManyToManyField(subclasses,verbose_name="Classes")
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "subjects"


class academic(models.Model):
    name = models.CharField(verbose_name='Academic Year',max_length=105,unique=True)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    fullname = models.CharField(max_length=255,blank=True,default='',verbose_name="fullname")
    student_class = models.ForeignKey(subclasses,on_delete=models.CASCADE,verbose_name='Student class')
    passkey = models.CharField(max_length=16,unique=True,blank=True,editable=False)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        #Generating the passkey
        self.passkey = uuid.uuid4().hex[:6]
        while Student.objects.filter(passkey=self.passkey).exists():
            unique_id = uuid.uuid4().hex[:6]
            self.passkey = unique_id

        # Syncing user data
        user = self.user
        self.fullname = f"{user.first_name} {user.last_name}"
        super(Student, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.fullname
    
    class Meta:
        verbose_name_plural = "Students"


class staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='staff')
    fullname = models.CharField(max_length=255,blank=True,default='',verbose_name="fullname")
    teacher_class = models.ManyToManyField(subclasses,related_name="teacher_class")
    subject = models.ForeignKey(subjects,on_delete=models.CASCADE,verbose_name='subject taught')
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname
    
    def save(self, *args, **kwargs):
        user = self.user 
        self.fullname = f"{user.first_name} {user.last_name}"
        super(staff, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'staff'


class Guardian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='parent')
    fullname = models.CharField(max_length=255,blank=True,default='',verbose_name="fullname")
    wards = models.ManyToManyField(Student)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname
    
    def save(self, *args, **kwargs):
        user = self.user 
        self.fullname = f"{user.first_name} {user.last_name}"    
        super(Guardian, self).save(*args, **kwargs)


class Standards(models.Model):
    name = models.CharField(max_length=100,verbose_name='label')
    greater_than = models.IntegerField(verbose_name="Should be Greater than")
    less_than = models.IntegerField(verbose_name="Should be Less than")

    def __str__(self):
        return self.name


class Assessment_records(models.Model):
    student = models.ForeignKey(Student,on_delete=models.RESTRICT,verbose_name='student')
    subject = models.ForeignKey(subjects,on_delete=models.RESTRICT,verbose_name="subject")
    exams_score = models.IntegerField(verbose_name="Exams Score")
    class_score = models.IntegerField(verbose_name="Class Score")
    total_score = models.IntegerField(verbose_name="Total Score")
    academic_year = models.ForeignKey(academic,on_delete=models.RESTRICT,verbose_name='academic year',default=academic.is_active==True)
    grade_relation = models.OneToOneField(Standards,on_delete=models.RESTRICT,verbose_name='grade')
    grade = models.CharField(max_length=100,blank=True,editable=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject','academic_year'],
                name='Student Must have a unique assessment subject and academic year'
            )
        ]

        verbose_name_plural = "Assessment Records"

    def __str__(self):
        return f"{self.student.fullname} - {self.subject.name}"


    def save(self, *args, **kwargs):
    # enforcing the integerfields 
        if not (0 <= self.class_score <= 100):
            raise ValueError("Class score must be between 0 and 100.")
        if not (0 <= self.exams_score <= 100):
            raise ValueError("Exams score must be between 0 and 100.")

    #calculating the total score
        self.total_score = self.class_score + self.exams_score

    #Automatic grade calculation
        if self.grade_relation and self.grade_relation.greater_than < self.total_score < self.grade_relation.less_than:
            self.grade = self.grade_relation.name
        else:
            self.grade = "Undefined" #In case the range does not exist
        super(Assessment_records, self).save(*args, **kwargs)


class Approvals(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='user',related_name='approvals',null=True)
    fullname = models.CharField(max_length=255,blank=True,default='',verbose_name="fullname")
    email = models.EmailField()
    approved = models.BooleanField()

    class Meta:
        verbose_name_plural = 'approvals'

    def __str__(self):
        return self.fullname
    
    def save(self, *args, **kwargs):
        user = self.user
        self.fullname = f"{user.first_name} {user.last_name}"
        if user.approved != self.approved:
            user.approved = self.approved
            user.save(update_fields=['approved'])
        super(Approvals, self).save(*args, **kwargs)


class Events(models.Model):
    tags =  (
        ("examination", "Examination"),
        ("holiday", "Holiday"),
        ("meeting", "Meeting"),
        ("extracurricular", "Extracurricular"),
        ("workshop", "Workshop"),
        ("graduation", "Graduation"),
        ("festival", "Festival"),
    )
    name = models.CharField(unique=True,max_length=100)
    description = models.TextField(max_length=100,default='')
    event_tags = models.CharField(choices=tags,max_length=15)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=100,blank=True,default='N/A')

    class Meta:
        verbose_name_plural = "Events"
    
    def __str__(self):
        return self.name