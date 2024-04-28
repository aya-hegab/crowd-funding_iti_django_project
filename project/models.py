from django.db import models
from django.contrib.auth.models import User
from category.models import *
from taggit.managers import TaggableManager



class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    title = models.CharField(max_length=255)
    details = models.TextField()
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Add featured stuff
    is_featured=models.BooleanField(default=False)
    category=models.ForeignKey(Category, on_delete= models.CASCADE,default=None)
    tags = TaggableManager(blank=True)

    
    @classmethod
    def project_list(self):
        return self.objects.all()

    @classmethod
    def project_detailes(cls, proid):
        return cls.objects.get(id=proid)
    
    @property
    def donation_percentage(self):
        if self.total_target == 0:
            return 0
        return (self.donation_amount / self.total_target) * 100

    @property
    def is_cancelable(self):
        return self.donation_percentage < 25

    def cancel_project(self):
        if self.is_cancelable:
            self.delete()
            return True
        return False

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project/images/', blank=True, null=True)   

    def project_image_detailes(cls, proid):
        return cls.objects.get(id=proid)

    def getimageurl(self):
        return f'/media/{self.image}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reason = models.TextField()
          

class ReportComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)  # New field
    comment_reason = models.TextField()

#rate projects
class ProjectRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.IntegerField()  
  