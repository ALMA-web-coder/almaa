from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Application, CertificateDocuments, CertificateEducational, Contact, MastersDocuments, MastersEducational, Other, Status, WorkExperience, Documents


class DocumentsInline(admin.StackedInline):
    model = Documents
    extra = 0
    can_delete= False
    max_num = 1

class ContactInline(admin.StackedInline):  
    model = Contact
    extra = 0
    can_delete= False
    max_num = 1
    
class MastersEducationalInline(admin.StackedInline):  
    model = MastersEducational
    extra = 1 
    
class MastersDocumentsInline(admin.StackedInline): 
    model =  MastersDocuments
    extra = 0
    can_delete= False
    max_num = 1
    
class CertificateEducationalInline(admin.StackedInline):  
    model = CertificateEducational
    extra = 1 
    
class CertificateDocumentsInline(admin.StackedInline): 
    model =  CertificateDocuments
    extra = 0
    can_delete= False
    max_num = 1

class WorkExperienceInline(admin.StackedInline):  
    model = WorkExperience
    extra = 1  

class OtherInline(admin.StackedInline): 
    model = Other
    extra = 0
    can_delete= False
    max_num = 1
    
class StatusInline(admin.StackedInline): 
    model = Status
    extra = 0
    can_delete = False
    max_num = 1


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'application_type')
    search_fields = ('first_name', 'last_name', 'user__username')  
    inlines = [
        DocumentsInline,
        ContactInline,
        MastersEducationalInline,
        CertificateEducationalInline,
        MastersDocumentsInline,
        CertificateDocumentsInline,
        WorkExperienceInline,
        OtherInline,
        StatusInline,
    ]


admin.site.register(Application, ApplicationAdmin)