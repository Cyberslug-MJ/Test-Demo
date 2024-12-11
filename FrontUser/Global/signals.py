from accounts.models import CustomUser as User 
from django.db.models.signals import post_save
from . models import *
from django.dispatch import receiver

@receiver(post_save,sender=User)
def Creator(sender,created,instance,**kwargs):
    if created:

        
        if instance.role == "Parent":
            Guardian.objects.create(
                user=instance,
                firstname = instance.first_name,
                lastname = instance.last_name
            )
        
        if instance.role == "Student":
            Student.objects.create(
                user=instance,
                firstname = instance.first_name,
                lastname = instance.last_name
            )
        
        if instance.role=="Teacher":
            staff.objects.create(
                user=instance,
                firstname = instance.first_name,
                lastname = instance.last_name
            )
            
            Approvals.objects.create(
                user=instance,
                firstname = instance.first_name,
                lastname = instance.last_name,
                email = instance.email,
                approved = instance.approved
            )
    
    else:
        

        if instance.role == "Parent":
            instance.parent.firstname = instance.first_name 
            instance.parent.lastname = instance.last_name
            instance.parent.wards.set(instance.parent.wards.all()) # add new wards or just update the old ones
            instance.parent.save()


        if instance.role == "Student":
            instance.student.firstname = instance.first_name
            instance.student.lastname = instance.last_name 
            instance.student.student_class = instance.student.student_class
            instance.student.save()


        if instance.role == "Teacher":
            instance.staff.firstname = instance.first_name 
            instance.staff.lastname = instance.last_name
            instance.staff.teacher_class.set(instance.staff.teacher_class.all()) # this is because it is a Many-to-Manyfield
            instance.staff.subject = instance.staff.subject
            instance.staff.save()
            instance.approvals.firstname = instance.first_name 
            instance.approvals.lastname = instance.last_name
            instance.approvals.email = instance.email
            instance.approvals.approved = instance.approved
            instance.approvals.save()