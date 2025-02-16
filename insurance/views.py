from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User
from customer import models as CMODEL
from customer import forms as CFORM

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'insurance/index.html')


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if is_customer(request.user):      
        return redirect('customer/customer-dashboard')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
        'total_user':CMODEL.Customer.objects.all().count(),
        'total_policy':models.Policy.objects.all().count(),
        'total_claim':models.Claim.objects.all().count(),
        'total_category':models.Category.objects.all().count(),
        'total_question':models.Question.objects.all().count(),
        'total_policy_holder':models.PolicyRecord.objects.all().count(),
        'approved_policy_holder':models.PolicyRecord.objects.all().filter(status='Approved').count(),
        'disapproved_policy_holder':models.PolicyRecord.objects.all().filter(status='Disapproved').count(),
        'waiting_policy_holder':models.PolicyRecord.objects.all().filter(status='Pending').count(),
        'total_claim_holder':models.ClaimRecord.objects.all().count(),
        'approved_claim_holder':models.ClaimRecord.objects.all().filter(status='Approved').count(),
        'disapproved_claim_holder':models.ClaimRecord.objects.all().filter(status='Disapproved').count(),
        'waiting_claim_holder':models.ClaimRecord.objects.all().filter(status='Pending').count(),
    }
    return render(request,'insurance/admin_dashboard.html',context=dict)



@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers= CMODEL.Customer.objects.all()
    return render(request,'insurance/admin_view_customer.html',{'customers':customers})



@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=CMODEL.User.objects.get(id=customer.user_id)
    userForm=CFORM.CustomerUserForm(instance=user)
    customerForm=CFORM.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=CFORM.CustomerUserForm(request.POST,instance=user)
        customerForm=CFORM.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'insurance/update_customer.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/admin-view-customer')



def admin_category_view(request):
    return render(request,'insurance/admin_category.html')

def admin_add_category_view(request):
    categoryForm=forms.CategoryForm() 
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('admin-view-category')
    return render(request,'insurance/admin_add_category.html',{'categoryForm':categoryForm})

def admin_view_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_view_category.html',{'categories':categories})

def admin_delete_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_delete_category.html',{'categories':categories})
    
def delete_category_view(request,pk):
    category = models.Category.objects.get(id=pk)
    category.delete()
    return redirect('admin-delete-category')

def admin_update_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_update_category.html',{'categories':categories})

@login_required(login_url='adminlogin')
def update_category_view(request,pk):
    category = models.Category.objects.get(id=pk)
    categoryForm=forms.CategoryForm(instance=category)
    
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST,instance=category)
        
        if categoryForm.is_valid():

            categoryForm.save()
            return redirect('admin-update-category')
    return render(request,'insurance/update_category.html',{'categoryForm':categoryForm})
  
  

def admin_policy_view(request):
    return render(request,'insurance/admin_policy.html')

def admin_claim_view(request):
    return render(request,'insurance/admin_claim.html')



def admin_add_policy_view(request):
    policyForm=forms.PolicyForm() 
    
    if request.method=='POST':
        policyForm=forms.PolicyForm(request.POST)
        if policyForm.is_valid():
            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
            return redirect('admin-view-policy')
    return render(request,'insurance/admin_add_policy.html',{'policyForm':policyForm})

def admin_add_claim_view(request):
    claimForm=forms.ClaimForm() 
    
    if request.method=='POST':
        claimForm=forms.ClaimForm(request.POST)
        if claimForm.is_valid():
            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            
            claim = claimForm.save(commit=False)
            claim.category=category
            claim.save()
            return redirect('admin-view-claim')
    return render(request,'insurance/admin_add_claim.html',{'claimForm':claimForm})

def admin_view_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_view_policy.html',{'policies':policies})

def admin_view_claim_view(request):
    claims = models.Claim.objects.all()
    return render(request,'insurance/admin_view_claim.html',{'claims':claims})



def admin_update_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_update_policy.html',{'policies':policies})

def admin_update_claim_view(request):
    claims = models.Claim.objects.all()
    return render(request,'insurance/admin_update_claim.html',{'claims':claims})

@login_required(login_url='adminlogin')
def update_policy_view(request,pk):
    policy = models.Policy.objects.get(id=pk)
    policyForm=forms.PolicyForm(instance=policy)
    
    if request.method=='POST':
        policyForm=forms.PolicyForm(request.POST,instance=policy)
        
        if policyForm.is_valid():

            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
           
            return redirect('admin-update-policy')
    return render(request,'insurance/update_policy.html',{'policyForm':policyForm})
  
@login_required(login_url='adminlogin')
def update_claim_view(request,pk):
    claim = models.Claim.objects.get(id=pk)
    claimForm=forms.ClaimForm(instance=claim)
    
    if request.method=='POST':
        claimForm=forms.ClaimForm(request.POST,instance=claim)
        
        if claimForm.is_valid():

            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            
            claim = claimForm.save(commit=False)
            claim.category=category
            claim.save()
           
            return redirect('admin-update-claim')
    return render(request,'insurance/update_claim.html',{'claimForm':claimForm})
  
  
def admin_delete_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_delete_policy.html',{'policies':policies})

def admin_delete_claim_view(request):
    claims = models.Claim.objects.all()
    return render(request,'insurance/admin_delete_claim.html',{'claims':claims})
    
def delete_policy_view(request,pk):
    policy = models.Policy.objects.get(id=pk)
    policy.delete()
    return redirect('admin-delete-policy')

def delete_claim_view(request,pk):
    claim = models.Claim.objects.get(id=pk)
    claim.delete()
    return redirect('admin-delete-claim')

def admin_view_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all()
    return render(request,'insurance/admin_view_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_claim_holder_view(request):
    claimrecords = models.ClaimRecord.objects.all()
    return render(request,'insurance/admin_view_claim_holder.html',{'claimrecords':claimrecords})

def admin_view_approved_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Approved')
    return render(request,'insurance/admin_view_approved_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_approved_claim_holder_view(request):
    claimrecords = models.ClaimRecord.objects.all().filter(status='Approved')
    return render(request,'insurance/admin_view_approved_claim_holder.html',{'claimrecords':claimrecords})

def admin_view_disapproved_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Disapproved')
    return render(request,'insurance/admin_view_disapproved_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_disapproved_claim_holder_view(request):
    claimrecords = models.ClaimRecord.objects.all().filter(status='Disapproved')
    return render(request,'insurance/admin_view_disapproved_claim_holder.html',{'claimrecords':claimrecords})

def admin_view_waiting_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Pending')
    return render(request,'insurance/admin_view_waiting_policy_holder.html',{'policyrecords':policyrecords})

def admin_view_waiting_claim_holder_view(request):
    claimrecords = models.ClaimRecord.objects.all().filter(status='Pending')
    return render(request,'insurance/admin_view_waiting_claim_holder.html',{'claimrecords':claimrecords})

def approve_policy_request_view(request,pk):
    policyrecords = models.PolicyRecord.objects.get(id=pk)
    policyrecords.status='Approved'
    policyrecords.save()
    return redirect('admin-view-policy-holder')

def approve_claim_request_view(request,pk):
    claimrecords = models.ClaimRecord.objects.get(id=pk)
    claimrecords.status='Approved'
    claimrecords.save()
    return redirect('admin-view-claim-holder')


def disapprove_policy_request_view(request,pk):
    policyrecords = models.PolicyRecord.objects.get(id=pk)
    policyrecords.status='Disapproved'
    policyrecords.save()
    return redirect('admin-view-policy-holder')

def disapprove_claim_request_view(request,pk):
    claimrecords = models.ClaimRecord.objects.get(id=pk)
    claimrecords.status='Disapproved'
    claimrecords.save()
    return redirect('admin-view-claim-holder')


def admin_question_view(request):
    questions = models.Question.objects.all()
    return render(request,'insurance/admin_question.html',{'questions':questions})

def update_question_view(request,pk):
    question = models.Question.objects.get(id=pk)
    questionForm=forms.QuestionForm(instance=question)
    
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST,instance=question)
        
        if questionForm.is_valid():

            admin_comment = request.POST.get('admin_comment')
            
            
            question = questionForm.save(commit=False)
            question.admin_comment=admin_comment
            question.save()
           
            return redirect('admin-question')
    return render(request,'insurance/update_question.html',{'questionForm':questionForm})







def aboutus_view(request):
    return render(request,'insurance/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'insurance/contactussuccess.html')
    return render(request, 'insurance/contactus.html', {'form':sub})

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import sqlite3

def generate_pdf_report(request, customer_id):
    # Fetch data from the database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            c.id AS customer_id, 
            c.address, 
            c.mobile, 
            u.username AS customer_name,
            p.id AS policy_id, 
            p.policy_name, 
            p.sum_assurance, 
            p.premium, 
            p.tenure, 
            p.creation_date AS policy_creation_date,
            pr.status AS policy_status,
            cl.id AS claim_id, 
            cl.claim_name, 
            cl.claim_amount, 
            cl.premium AS claim_premium, 
            cl.claim_date,
            cr.status AS claim_status,
            q.description AS question, 
            q.admin_comment, 
            q.asked_date
        FROM 
            customer_customer c
        JOIN 
            auth_user u ON c.user_id = u.id
        LEFT JOIN 
            insurance_policyrecord pr ON c.id = pr.customer_id
        LEFT JOIN 
            insurance_policy p ON pr.Policy_id = p.id
        LEFT JOIN 
            insurance_claimrecord cr ON c.id = cr.customer_id
        LEFT JOIN 
            insurance_claim cl ON cr.Claim_id = cl.id
        LEFT JOIN 
            insurance_question q ON c.id = q.customer_id
        WHERE 
            c.id = ?;
    """, (customer_id,))

    data = cursor.fetchall()
    conn.close()

    # Organize data for the template
    customer_name = data[0][3]
    address = data[0][1]
    mobile = data[0][2]
    policies = [row[4:10] for row in data]
    claims = [row[10:15] for row in data]
    questions = [row[15:18] for row in data]

    # Render HTML template
    html_string = render_to_string('insurance/report_template.html', {
        'customer_name': customer_name,
        'address': address,
        'mobile': mobile,
        'policies': policies,
        'claims': claims,
        'questions': questions
    })

    # Generate PDF
    pdf = HTML(string=html_string).write_pdf()

    # Return PDF as a response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="insurance_report_{customer_id}.pdf"'
    return response