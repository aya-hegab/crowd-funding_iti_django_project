from django.contrib import admin
from .models import Project,ProjectImage,Comment,Report,ReportComment,ProjectRating
# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(ReportComment)
admin.site.register(ProjectRating)