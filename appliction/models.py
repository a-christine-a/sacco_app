from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class LoanApplication(models.Model):
    # select = models.BooleanField(null=True, blank=True, default=False)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    loan_id = models.CharField(max_length=50, primary_key=True)
    id_number =models.PositiveSmallIntegerField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    address = models.CharField(max_length=200, blank=True)
    phone_number = models.PositiveSmallIntegerField()
    date_of_birth = models.DateField()
    repayment_period_in_months = models.DecimalField(max_digits=2, decimal_places=0)
    income_level = models.DecimalField(max_digits=8, decimal_places=2)
    amount_applied = models.DecimalField(max_digits=8, decimal_places=2)
    #time_applied = models.DateTimeField(auto_created=True, auto_now=True, auto_now_add=True)
    pending = 'pending'
    approved = 'approved'
    disbursed = 'disbursed'
    rejected = 'rejected'
    closed = 'closed'

    loan_status = [
        (pending, 'pending'),
        (approved, 'approved'),
        (disbursed, 'disbursed'),
        (rejected, 'rejected'),
        (closed, 'closed')
    ]
    loan_status = models.CharField(max_length=20, choices=loan_status, default=pending)
    guarantor_id = models.PositiveSmallIntegerField()
    guarantor_name = models.CharField(max_length=60)
    guarantor_email = models.EmailField(max_length=200)
    gurantor_income_level = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.loan_id

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length= 200)
    feedback = models.TextField()

class UpdateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    member = 'member'
    staff = 'staff'
    guest = 'guest'

    user_types = [
        (member, 'member'),
        (staff, 'staff'),
        (guest, 'guest'),
    ]
    user_type = models.CharField(max_length=20, choices=user_types, default=guest)
    id_number = models.PositiveSmallIntegerField(default=0)
    address = models.CharField(max_length=200, blank=True, default="")
    phone_number = models.IntegerField(default=0)
    date_of_birth = models.DateField(default="2000-01-01")
    profile_pic = models.ImageField(upload_to="Profile/", default="undraw_profile.svg")
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        UpdateProfile.objects.create(user=instance)

class Repayment(models.Model):
    loan_id = models.OneToOneField(LoanApplication, on_delete=models.DO_NOTHING)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    intrest = models.DecimalField(max_digits=8,decimal_places=2)
    total_payable = models.DecimalField(max_digits=8, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)

    debit = 'debit'
    credit = 'credit'
    trans_type=[
        (debit, 'debit'),
        (credit, 'credit'),
    ]
    transaction_type = models.CharField(max_length=50, choices=trans_type, default=debit)
    
    # def __str__(self):
    #     return self.str(amount_paid)