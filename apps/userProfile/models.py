# This is models.py for a new user profile that you would like to create.
 
"""
this gist gets an id from django-social-auth and based on that saves the photo from social networks into your model. This is one of the best ways to extend User model because this way, you don't need to redefine a CustomUser as explained in the doc for django-social-auth. this is a new implementation based on https://gist.github.com/1248728
"""
import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django_resized import ResizedImageField
from django.utils.translation import ugettext_lazy as _

def get_image_path(instance, filename):
    return os.path.join('users', str(instance.id), filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    GENDER_CHOICES = (
        (_('male'), _('Male')),
        (_('female'), _('Female')),
        (_('other'), _('Other')),
        ('', '')
        )
    profile_photo = ResizedImageField(upload_to="users/", max_width=100, max_height=80, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES, verbose_name=_("Gender"))
    image_url = models.URLField(blank=True, verbose_name=_("Avatar Picture"))
    description = models.TextField(blank=True, verbose_name=_("Description"), help_text=_("Tell us about yourself!"))
    def __str__(self):  
        return "%s's profile" % self.user  
    class Meta:
        app_label = 'userProfile'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


from social_auth.backends.facebook import FacebookBackend
from social_auth.backends import google
from social_auth.signals import socialauth_registered
from social_auth.signals import pre_update

def new_users_handler(sender, user, response, details, **kwargs):
    user.is_new = True
    if user.is_new:
        if "id" in response:
            from urllib2 import urlopen, HTTPError
            from django.template.defaultfilters import slugify
            from django.core.files.base import ContentFile
            
            try:
                url = None
                if sender == FacebookBackend:
                    url = "http://graph.facebook.com/%s/picture?type=large" \
                                % response["id"]
                elif sender == google.GoogleOAuth2Backend and "picture" in response:
                    url = response["picture"]
    
                if url:
                    avatar = urlopen(url)
                    profile = UserProfile.objects.get(user=user)
                    #profile = user.get_profile()
                    if sender == FacebookBackend:
                        profile.image_url = 'https://graph.facebook.com/' + user.username+ '/picture'
                        #profile.profile_photo.save(slugify(user.username + " social") + '.jpg', ContentFile(avatar.read()))              
                                    
                    profile.save()
    
            except HTTPError:
                pass
    
    return False
 
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0]) 
pre_update.connect(new_users_handler, sender=FacebookBackend)




