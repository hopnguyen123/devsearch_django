from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

# @receiver(post_save,sender=Profile)

# created có giá trị True hoặc False cho biết 1 user được thêm
#   hoặc 1 model (instance) được thêm vào database
# created == True : tạo mới
# created == False : cập nhật 
def profileUpdated(sender,instance,created,**kwargs):
    if created:
        print('New User - New Profile !!!')
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )

        subject = 'Welcome to Devsearch'
        message = 'We are glad you are here'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )

# Khi 1 User được save mới thì Profile mới sẽ được tạo
post_save.connect(profileUpdated,sender=User)

def profileDelete(sender,instance,**kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
    
# Khi 1 Profile delete thì user sẽ delete theo
post_delete.connect(profileDelete,sender=Profile)

# Khi 1 Profile được chỉnh sửa --> Created == False
# thì user sẽ được tự động update theo 
def updateUser(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user
    if created == False:
        print('Update Profile - update user')
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

post_save.connect(updateUser,sender=Profile)