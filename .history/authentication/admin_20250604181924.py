from django.contrib import admin
from .models import Application, CertificateDocuments, CertificateEducational, Contact, MastersDocuments, MastersEducational, Other, Status, WorkExperience, Documents, ApplicationPayments, GeneralPayments, Acca, FocusArea
from django.urls import reverse
from django.utils.html import format_html
from .models import Download
from core.admin import custom_admin_site


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


custom_admin_site.register(Application, ApplicationAdmin)




class DownloadAdmin(admin.ModelAdmin):
    list_display = ['button_link']

    def button_link(self, obj):
        url = reverse('application_list')  # Ensure this is your actual URL name
        return format_html(
            '<a class="button" href="{}" style="padding: 6px 12px; background-color: #007BFF; color: white; border-radius: 4px; text-decoration: none;">Download Files in Excel or Word format here</a>',
            url
        )
    button_link.short_description = 'Action'

custom_admin_site.register(Download, DownloadAdmin)


class ApplicationPaymentsAdmin(admin.ModelAdmin):
    list_display = ('paynow_reference', 'status', 'customer_name', 'customer_email', 'amount', 'created_at')
    list_filter = ('status', 'payment_type', 'created_at')
    search_fields = ('paynow_reference', 'customer_name', 'customer_email', 'customer_phone', 'redirect_url')
    readonly_fields = ('created_at',)  # Make created_at read-only
    fieldsets = (
        ('Payment Details', {
            'fields': ('application', 'paynow_reference', 'status', 'amount', 'reference', 'redirect_url')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

custom_admin_site.register(ApplicationPayments, ApplicationPaymentsAdmin)


class GeneralPaymentsAdmin(admin.ModelAdmin):
    list_display = ('paynow_reference', 'customer_name', 'customer_email', 'amount', 'created_at', 'redirect_url')
    list_filter = ('payment_type', 'status', 'created_at')
    search_fields = ('paynow_reference', 'customer_name', 'customer_email', 'customer_phone', 'redirect_url')
    readonly_fields = ('created_at',)  # Make created_at read-only
    fieldsets = (
        ('Payment Details', {
            'fields': ('paynow_reference', 'amount', 'reference', 'status', 'redirect_url')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

custom_admin_site.register(GeneralPayments, GeneralPaymentsAdmin)

class AccaAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'level', 'get_focus_areas')
    search_fields = ('name', 'description', 'level', 'focus_areas__name')  # Search focus areas by name
    filter_horizontal = ('focus_areas', 'description',)  # Provides a nice UI for many-to-many selection

    def get_focus_areas(self, obj):
        # Return a comma-separated list of focus area names
        return ", ".join([focus.name for focus in obj.focus_areas.all()])
    get_focus_areas.short_description = 'Focus Areas'

# Register your model admin
custom_admin_site.register(Acca, AccaAdmin)

class FocusAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
custom_admin_site.register(FocusArea, FocusAreaAdmin)