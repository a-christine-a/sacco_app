from django.contrib import admin
from appliction.models import LoanApplication, Contact, UpdateProfile, Repayment
# Register your models here.

def change_user_type(modeladmin, request, queryset):
    queryset.update(user_type = 'staff')

change_user_type.short_description = "Mark Selected as Staff"


class LoanAppliacationAdmin(admin.ModelAdmin):
    list_display = ('user','loan_id','first_name','last_name','phone_number','income_level','amount_applied','guarantor_name','loan_status')
    list_filter=('loan_id','income_level','amount_applied','loan_status')
    #search_fields=('user',)
    ordering=('user', 'loan_status')
    list_per_page=10
class ContactAdmin(admin.ModelAdmin):
    list_display =('name', 'email', 'feedback')
    list_filter=('feedback','email')
    search_fields=('feedback','email')
    list_per_page=10

class UpdateProfileAdmin(admin.ModelAdmin):
    list_display = ('user','user_type','id_number','address','phone_number','date_of_birth')
    list_filter=('user','user_type')
    #search_fields=('user',)
    actions = [change_user_type]
    list_per_page=10
class RepayAdmin(admin.ModelAdmin):
    list_display=('loan_id','intrest','total_payable','amount_paid','balance','transaction_date','transaction_type')
    list_filter=('loan_id','amount_paid','balance','transaction_type','intrest','total_payable')
    ordering=('created_at','transaction_type','transaction_date','intrest')
    list_per_page = 10
    
admin.site.register(LoanApplication, LoanAppliacationAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(UpdateProfile, UpdateProfileAdmin)
admin.site.register(Repayment, RepayAdmin)


admin.site.site_header = "Uwezo Sacco Admin Pannel"