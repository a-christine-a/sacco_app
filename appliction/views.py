from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, UserProfileInfoForm
from django.template.context_processors import csrf
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, ListView,FormView, CreateView, UpdateView, DeleteView
from .models import LoanApplication, Contact, Repayment, UpdateProfile
# from .forms import ApplyLoan
# Create your views here.

def index(request):
    return render(request, 'home.html')

# @login_required
# class Apply(CreateView):
#     fields = ('income_level', 'amount_applied', 'repayment_period_in_months', 'guarantor_id', 'guarantor_name',
#     'guarantor_email', 'gurantor_income_level')
#     model= LoanApplication
#     template_name = 'application/apply.html'
#     def capture(request):
        


#     def get_success_url(self):
@login_required
def apply_loan(request):
    # form = ApplyLoan()
    # fild = ('income_level', 'amount_applied', 'repayment_period_in_months', 'guarantor_id', 'guarantor_name',
    # 'guarantor_email', 'gurantor_income_level')
    if request.method == "POST":
        rperiod = request.POST['repayment_period']
        in_lev = request.POST['income_level']
        amnt = request.POST['amount']
        gid = request.POST['guarantor_id']
        gnm = request.POST['guarantor_name']
        gmal = request.POST['guarantor_email']
        g_in_lv = request.POST['guarantor_income_level']
        user = request.POST['usr']
        user_ob = User.objects.get(id=user)
        uid = request.POST['uid']
        addr = request.POST['addr']
        dob = request.POST['dob'].replace(" ","").replace(",", ".").replace(".", "-")
        y = dob.split("-")[2]
        m = dob.split("-")[0]
        d = dob.split("-")[1]
        if "Dec" in m:
            m = '12'
        elif "Nov" in m:
            m = '11'
        elif "Oct" in m:
            m = '10'
        elif "Sep" in m:
            m = '09'
        elif "Aug" in m:
            m = '08'
        elif "Jul" in m:
            m = '07'
        elif "Jun" in m:
            m = '06'
        elif "May" in m:
            m = '05'
        elif "Apr" in m:
            m = '04'
        elif "Mar" in m:
            m = '03'
        elif "Feb" in m:
            m = '02'
        elif "Jan" in m:
            m = '01'
        if len(d) < 2:
            d = "0" + d
        fdob = f"{y}-{m}-{d}"
        print(fdob)
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        applicatiom = LoanApplication.objects.create(
            income_level=in_lev,
            amount_applied=amnt,
            repayment_period_in_months=rperiod,
            guarantor_id=gid,
            guarantor_name=gnm,
            guarantor_email=gmal, 
            gurantor_income_level=g_in_lv,
            id_number=uid,
            address=addr,
            first_name=fname,
            last_name=lname,
            email=email,
            date_of_birth=fdob,
            phone_number = phone_no,
            user_id=user_ob.id,
            loan_id="USA-" + str(timezone.now()).split(".")[0].replace("-", "").replace(" ", "-").replace(":", "")
        )
        applicatiom.save()
        return redirect('success')
    else:
        return render(request, 'application/apply.html')


def success(request):
    return render(request, 'application/success.html')

class Contact(CreateView):
    fields = ('name','email','feedback')
    model= Contact
    template_name = 'contact.html'

    def get_success_url(self):
        return reverse_lazy('contacts')

def contacts(request):
    return render(request, 'contacts.html')

def settins(request):
    return render(request, 'settings.html')

@login_required
def applicationview(request):
    if request.method == "POST":
        selected = request.POST['selected'].split(" ")
        action = request.POST['action']
        selected.pop(len(selected)-1)
        if selected:     
            if 'approve' in action:
                for s in selected:
                    aproval = LoanApplication.objects.get(loan_id=s)
                    aproval.loan_status = "approved"
                    aproval.save()
            elif 'reject' in action:
                for s in selected:
                    aproval = LoanApplication.objects.get(loan_id=s)
                    aproval.loan_status = "rejected"
                    aproval.save()
        return redirect('applicants')
    else:
        pending = LoanApplication.objects.filter(loan_status="pending")
        approved = LoanApplication.objects.filter(loan_status="approved")
        rejected = LoanApplication.objects.filter(loan_status="rejected")
        disbursed = LoanApplication.objects.filter(loan_status="disbursed")
        closed = LoanApplication.objects.filter(loan_status="closed")
        pending_count = pending.count()
        approved_count = approved.count()
        rejected_count = rejected.count()
        disbursed_count = disbursed.count()
        closed_count = closed.count()
        # select = LoanApplication.objects.

        context = {
            # 'select':
            'app':pending,
            'approved':approved,
            'rejected':rejected,
            'disbursed': disbursed,
            'closed': closed,
            'pending_count':pending_count,
            'approved_count':approved_count,
            'rejected_count':rejected_count,
            'disbursed_count':disbursed_count,
            'closed_count':closed_count,
        }
        return render(request, 'report/applicatnts.html',context)


@login_required
def application(request):
    if request.method == "POST":
        print("Iwant to aprove someone")
        d_select = request.POST['d_select'].split(" ")
        d_select.pop(len(d_select) -1)
        if d_select:
            print(d_select)
            for s in d_select:
                aproval = LoanApplication.objects.get(loan_id=s)
                aproval.loan_status = "disbursed"
                aproval.save()
        return redirect('applicants')
    else:
        return redirect('applicants')

@login_required
def profile(request):
    return render(request, 'profile.html')

def fetch_loans(request):
    if request.method == "POST":
        user_id = request.POST['u_id']
        loans = LoanApplication.objects.filter(user=user_id)
        return render(request, 'repayment/repay.html',{'loans':loans})

def loan_repay(request):
    if request.method == "POST":
        l_id = request.POST['loans'].strip()
        amount = request.POST['amount_paid']
        loan_obj = LoanApplication.objects.get(loan_id=l_id)
        debt = loan_obj.amount_applied
        rate = 0.12
        intres = float(debt) * float(rate)
        total_payable = float(debt) + float(intres)
        balace = float(total_payable) - float(amount)
        print(balace)
        print(intres)
        myloan = Repayment.objects.create(
            loan_id=loan_obj,
            amount_paid=amount,
            balance=balace,
            intrest=intres,
            total_payable = total_payable,
        )        
        myloan.save()
        messages.success(request, "Your Payment was successfully sent")
        return redirect('index')
    else:  
        return render(request, 'repayment/repay.html')


def reports(request):
    pending = LoanApplication.objects.filter(loan_status="pending")
    approved = LoanApplication.objects.filter(loan_status="approved")
    rejected = LoanApplication.objects.filter(loan_status="rejected")
    disbursed = LoanApplication.objects.filter(loan_status="disbursed")
    closed = LoanApplication.objects.filter(loan_status="closed")
    pending_count = pending.count()
    approved_count = approved.count()
    rejected_count = rejected.count()
    disbursed_count = disbursed.count()
    closed_count = closed.count()
    total_approved = approved_count + disbursed_count + closed_count
    context = {
        'app':pending,
        'approved':approved,
        'rejected':rejected,
        'disbursed': disbursed,
        'closed': closed,
        'pending_count':pending_count,
        'approved_count':approved_count,
        'rejected_count':rejected_count,
        'disbursed_count':disbursed_count,
        'closed_count':closed_count,
        'total_approved':total_approved,
    }
    return render(request, 'report/reports.html',context)

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = UserProfileInfoForm
    template_name = 'profile_update.html'

    def post(self, request):
        post_data = request.POST or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = UserProfileInfoForm(post_data, instance=request.user.updateprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile was successfully updated! ')
            return HttpResponseRedirect(reverse_lazy('step_1'))
        context = self.get_context_data(
            user_form = user_form,
            profile_form = profile_form
        )
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
