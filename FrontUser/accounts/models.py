from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.text import slugify
from django.conf import settings


class CustomUserManager(BaseUserManager):

    def create_user(self, email, role, password=None):
        if not email:
            raise ValueError("Users must have an email address!")
        
        if not role:
            raise ValueError("Users must select a role")
        
        user = self.model(
            email = self.normalize_email(email),
            role = role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, role, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            role = role,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class CustomUser(AbstractBaseUser,PermissionsMixin):
    email           =models.EmailField(verbose_name='email',max_length=60,unique=True)
    username        =models.CharField(verbose_name='username',max_length=60,unique=True,blank=True)
    date_joined     =models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login      =models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin        =models.BooleanField(default=False)
    is_active       =models.BooleanField(default=True)
    is_superuser    =models.BooleanField(default=False)
    is_staff        =models.BooleanField(default=False)
    role_choices    =(("Admin","Admin"),("Parent","Parent"),("Student","Student"),("Teacher","Teacher"))
    role            =models.CharField(max_length=7,choices=role_choices,db_index=True)
    school_name     =models.CharField(max_length=200,blank=True,db_index=True,unique=True,null=True)
    first_name      =models.CharField(verbose_name='first_name',max_length=200,default='N/A',blank=True)
    last_name       =models.CharField(verbose_name='last_name',max_length=200,default='N/A',blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role',]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    

    def has_module_perms(self,app_label):
        return True
    
    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUser'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    

    def get_short_name(self):
        return self.first_name
    


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True,verbose_name='User Profile',related_name='profile')
    profile_picture = models.ImageField(upload_to='images',blank=True,default='images/profile_pic.webp')
    firstname = models.CharField(max_length=100,blank=True)
    lastname = models.CharField(max_length=100,blank=True)
    email = models.EmailField(blank=True)
    #phone_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=255,blank=True,default="N/A")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'User Profile'

    def save(self, *args, **kwargs):
        user = self.user
        user.first_name = self.firstname
        user.last_name = self.lastname
        user.email = self.email
        #user.phone_number = self.phone_number
        user.save()
        super().save(*args, **kwargs)


class SchoolProfile(models.Model):
    tier_choices = (
        ("Tier 1","Tier 1"),
        ("Tier 2","Tier 2"),
        ("Tier 3","Tier 3")
    )
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True,related_name="school",verbose_name="school profile")
    name = models.CharField(max_length=255,blank=True)
    logo = models.URLField(default="https://my-bucket.s3.amazonaws.com/my-folder/my-image.jpg?AWSAccessKeyId=EXAMPLE&Expires=1672531199&Signature=abcdef",
    verbose_name="logo",blank=True,max_length=1000)
    address = models.CharField(max_length=255,blank=True)
    bio = models.TextField(max_length=500,blank=True)
    theme = models.CharField(max_length=7,blank=True)
    tier = models.CharField(choices=tier_choices,max_length=6,verbose_name="tier",default="Tier 1")
    subdomain_url = models.URLField(blank=True,default='http://www.yourschool.domain.com')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        name = self.name
        subdomain = slugify(name).replace(" ","-").lower()
        self.subdomain_url = f"https://www.{subdomain}.domain.com"

        #syncing user data 
        user = self.user
        user.school_name = self.name
        user.save()
        super(SchoolProfile, self).save(*args, **kwargs)