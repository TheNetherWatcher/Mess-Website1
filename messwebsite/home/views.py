from django.shortcuts import render
from .models import Allocation, Cafeteria, Caterer, Contact, longRebate, Period, Rule, shortRebate, Student, Forms
from .models.messperiod import messPeriod
from django.shortcuts import render, redirect
import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages
from django.contrib.auth import logout
# from django.contrib.admin import 
# Create your views here.

def home(request):
    return render(request, "home.html")

def rules(request):
    rules = Rule.objects.all()
    params = {
        "rule": rules,
    }
    print(params)
    return render(request, "rules.html", params)

def services(request):
  all_cafeteria_items = Cafeteria.objects.all()
  context = {
    'cafeteria_items': all_cafeteria_items,
  }
  return render(request, "cafeteria.html", context)

def con(request):
    all_obj = Contact.objects.all()
    context = {
    'contact_items': all_obj,
    }
    return render(request, "contact.html", context)

def caterer(request):
    caterer = Caterer.objects.all()
    context = {
        'caterer': caterer,
    }
    return render(request, "caterer.html", context)

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None and user.is_active:
            auth_login(request,user)
            return render(request,'index.html')
        else:
            messages.error(request,'Invalid Credentials')
    return render(request, "login.html")

def logout(request):
    # if request.user.is_authenticated:
    #     auth_logout(request)
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/home')

def links(request):
    links = Forms.objects.all()
    context = {
        'links': links,
    }
    return render(request, "forms.html", context)

@login_required
def profile(request):
    text = ""
    student = Student.objects.filter(email__iexact=str(request.user.email)).last()
    socialaccount_obj = SocialAccount.objects.filter(provider='google', user_id=request.user.id)
    picture = "not available"
    allocation = Allocation.objects.filter(email=student).last()
    allocation_info = {}
    #improve this alignment of text to be shown on the profile section
    if allocation:
        allocation_info_list = [allocation.student_id, allocation.caterer.name]
        allocation_info = {
            "Allocation ID": allocation.student_id,
            "Caterer": allocation.caterer.name,
            "Jain": "Yes" if allocation.jain else "No",
        }

    try:
        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
    except:
        picture = "not available"
    context = {"text": text,"student":student, "picture":picture,"allocation_info":allocation_info}
    return render(request, "profile.html", context)

@login_required(login_url='/login/')
def allocationForm(request):
    if request.method == 'POST':
        # student_email = request.POST['email']
        choice1_id = request.POST['choice1']
        choice2_id = request.POST['choice2']
        choice3_id = request.POST['choice3']

        st = Student.objects.filter(email__iexact=str(request.user.email)).last()

        print(choice1_id)

        caterer_choices = [
            choice1_id, choice2_id, choice3_id
        ]

        for cat in caterer_choices:
            cat_from_db = Caterer.objects.get(name=cat)
            if cat_from_db.current_no_students < cat_from_db.student_limit:
                cat_from_db.current_no_students += 1
                cat_from_db.save()
                st.caterer_alloted = cat_from_db
                st.alloted_id = cat_from_db.id_tobe_alloted + str(cat_from_db.current_no_students)
                st.save()
                return redirect('/')

        # No space available in any of the choices
        return redirect("/")

    # Render the form if GET request
    cats = Caterer.objects.all()
    student = Student.objects.filter(email__iexact=str(request.user.email)).last()
    return render(request, 'allocation.html', {'caterers': cats})

@login_required(login_url='/login/')
def shortRebateForm (request):
    student_email = Student.objects.filter(email__iexact=str(request.user.email)).last()

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        st = Student.objects.get(email=student_email)
        cat = str(st.caterer_alloted)
        print(cat)
        caterer_alloted = Caterer.objects.get(name=cat)
        rebate_rate = caterer_alloted.rebate_rate
        start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        days_diff = (end_date_obj - start_date_obj).days + 1
        print(start_date_obj)
        mess_period = messPeriod.objects.filter(month=start_date_obj.month).first()
        print(mess_period)
        amount = days_diff * rebate_rate

        try:
            rebate = shortRebate(
                student_applied=st,
                rebating_caterer=caterer_alloted,
                start_date=start_date_obj,
                end_date=end_date_obj,
                amount=amount
            )
            rebate.save()
            print("shortrebate submitted successfully")
        except:
            print("Some error occured")
            return redirect('/')
        
    return render(request, 'shortrebate.html', {'student': Student.objects.get(student_email=student_email), 'rebate': shortRebate.objects.get(student_applied=student_email, )})

@login_required(login_url='/login/')
def longRebateForm(request):
    if request.method == 'POST':
        student_email = request.POST['email']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        # reason = request.POST['reason']
        file = request.FILES.get('file', None)

        st = Student.objects.get(email=student_email)

        # Convert start and end dates to datetime objects
        start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        # Calculate the number of days for the rebate
        days_diff = (end_date_obj - start_date_obj).days + 1

        try:
            rebate = longRebate(
                email=st,
                start_date=start_date_obj,
                end_date=end_date_obj,
                days=days_diff,
                # reason=reason,
                file=file
            )
            rebate.save()
            
            print("logrebate submitted successfully")
        except:
            print("Some error occured")
            return redirect('failure', student_email=student_email)
    # Render the form if GET request
    return render(request, 'longrebate.html')

def adminJobs(request):
    if request.method == 'POST':
        start = request.POST.get('start_datetime')
        end = request.POST.get('end_datetime')

        if start is None and end is not None:
            return redirect('/adminJobs')
        if start is not None and end is None:
            return redirect('/adminJobs')
        
        

    return render(request, 'allocation_schedule.html')


