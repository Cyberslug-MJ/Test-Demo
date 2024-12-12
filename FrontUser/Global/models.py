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
    title = models.CharField(max_length=128)
    body = models.TextField(max_length=150)
    audiences = models.CharField(max_length=8,choices=audience,default="Everyone")
    scheduled_for = models.DateField(default=datetime.datetime.now)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "Announcements"
    
    def __str__(self):
        return self.title
    
class subclasses(models.Model):
    name = models.CharField(max_length=100,unique=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="date created")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="last modified")
    
class StudentClasses(models.Model):
    name = models.CharField(max_length=50,unique=True)
    subclasses = models.ForeignKey(subclasses,on_delete=models.CASCADE,verbose_name='subclass')
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = "student classes"


class subjects(models.Model):
    name = models.CharField(verbose_name='name of subject',max_length=100,unique=True)
    classes = models.ManyToManyField(StudentClasses,verbose_name="Classes")
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
    

class Assessments(models.Model):
    name = models.CharField(max_length=125,verbose_name='Name of Assessment')
    use_for_assessment = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "assessments"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    fullname = models.CharField(max_length=255,blank=True,default='',verbose_name="fullname")
    student_class = models.ForeignKey(StudentClasses,on_delete=models.CASCADE,null=True)
    student_id = models.CharField(max_length=20,blank=True)
    passkey = models.CharField(max_length=16,unique=True,blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        #Generating the passkey
        self.passkey = uuid.uuid4().hex[:6]
        while Student.objects.filter(passkey=self.passkey).exists():
            unique_id = uuid.uuid4().hex[:6]
            self.passkey = unique_id

        #Student ID generation
        count = self.fullname
        self.student_id = f"STU/000{count}"

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
    teacher_class = models.ManyToManyField(StudentClasses,related_name="teacher_class")
    subject = models.ForeignKey(subjects,on_delete=models.CASCADE,verbose_name='subject taught',null=True)

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
    wards = models.ManyToManyField(Student,blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname
    
    def save(self, *args, **kwargs):
        user = self.user 
        self.fullname = f"{user.first_name} {user.last_name}"    
        super(Guardian, self).save(*args, **kwargs)


class Assessment_records(models.Model):
    tags = (
        ('Exams','Exams'),
        ('Class Assessment','Class Assessment')
    )
    assessment_tag = models.CharField(max_length=25,verbose_name='Tag',blank=True,choices=tags)
    assessment = models.ForeignKey(Assessments,on_delete=models.RESTRICT,verbose_name='assessment')
    student = models.ForeignKey(Student,on_delete=models.RESTRICT,verbose_name='student',null=True)
    subject = models.ForeignKey(subjects,on_delete=models.RESTRICT,verbose_name="subject",null=True)
    total_score = models.IntegerField(verbose_name="Total marks",null=True)
    score = models.IntegerField(verbose_name='score in the assessement')
    academic_year = models.ForeignKey(academic,on_delete=models.RESTRICT,verbose_name='academic year',null=True,default=academic.is_active==True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['assessment', 'student', 'subject','academic_year'],
                name='Student Must have a unique assessment subject and academic year'
            )
        ]

        verbose_name_plural = "Assessment Records"

    def __str__(self):
        return self.assessment.name
 

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