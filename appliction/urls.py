from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('success', views.success, name="success"),
    path('contacts', views.contacts, name='contacts'),
    path('settings', views.settins, name='settings'),
    path('profile', views.profile, name='profile'),
    path('profile-update',views.ProfileUpdateView.as_view(), name="update-profile"),
    # path('profile-update',views.ProfileUpdate_ApplyView.as_view(), name="update-profile-apply"),
    path('reports', views.reports, name='reports'),
    path('viewapplicants', views.applicationview, name='applicants'),
    path('viewapplicant', views.application, name='applicant'),
    path('contact', views.Contact.as_view(), name="contact"),
    # path('application',views.Apply.as_view(), name="step_1"),
    path('application',views.apply_loan, name="step_1"),
    path('repay', views.loan_repay, name="repay"),
    #path('repay', views.LoanRepay.as_view(), name="repay"),
    path('fetch_loans', views.fetch_loans, name='fetch-loans'),
]
