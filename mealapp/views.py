from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db.models import Q,F
from django.http import HttpResponse
from .import models
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db.models import Q,F
from .import models
import datetime
from django.core import serializers
import json
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import random, string, os
from django.contrib.auth.decorators import login_required
import hashlib, socket
from django.db.models import Sum
from django.db.models import Q

def start(request):
    
    return render(request, 'blogapp/home.html')
def homepage(request):
    
    return render(request, 'mealapp/index.html')

def add_member(request):
    if request.method=="POST":
        member_name  = request.POST['member_name']
        email       = request.POST['email']
        mobile      = request.POST['mobile']
        address     = request.POST['address']
        room_no     = request.POST['room_no']
      

        models.MemberInfo.objects.create(member_name = member_name, address = address, mobile =mobile, email =email, room_no =room_no)
        return redirect("/members")
    else:
        return render(request, 'mealapp/add-member.html')
        

def edit_member(request,id):
    if request.method=="POST":
        member_name  = request.POST['member_name']
        email       = request.POST['email']
        mobile      = request.POST['mobile']
        address     = request.POST['address']
        room_no     = request.POST['room_no']

        models.MemberInfo.objects.filter(id=id).update(member_name = member_name, address = address, mobile =mobile, email =email, room_no =room_no)
        return redirect("/members")
    else:
        context = {
            'mem': models.MemberInfo.objects.get(id = id)
        }
        return render(request, 'mealapp/edit-member.html',context)

def delete_member(request,id):
        models.MemberInfo.objects.filter(id=id).delete()
        return redirect("/members")


def member_list(request):
    if request.method =="POST":
        search = request.POST['search']
        search_list = models.MemberInfo.objects.filter(Q(member_name__icontains = search)|Q(mobile__icontains = search))
        context = {
        'search_list': search_list,
        }
        return render(request, 'mealapp/member_list.html', context)

    context = {
        'member': models.MemberInfo.objects.all()
    }
    return render(request, 'mealapp/members.html', context)

def add_meal(request):
    if request.method=="POST":
        member_name  = int(request.POST[('member_name')])
        no_of_meal   = request.POST['no_of_meal']
        add_date     = request.POST['add_date']
        models.DailyMeal.objects.create(member_name_id = member_name, no_of_meal = no_of_meal, add_date = add_date)
        return redirect("/members")
    else:
        return render(request, 'mealapp/add-meal.html')
    context = {
        'member': models.MemberInfo.objects.all()
    }
    return render(request, 'mealapp/add-meal.html', context)

def meal_name_list(request):
    
    meal           = models.MemberInfo.objects.filter(status=True).order_by("id")

    context = {
        
        'meal'    : meal,
    }
    return render(request, 'mealapp/meal-list.html', context)

def meal_list(request, id):
    
    meal_d           = models.DailyMeal.objects.filter(member_name__id = id, status=True)
    tatal_amount     = models.DailyMeal.objects.filter(member_name__id = id,status = True).aggregate(Sum('no_of_meal'))['no_of_meal__sum']
    
    context = {

        'meal_d'    : meal_d,
        'tatal_amount'    : tatal_amount,

        
    }
    return render(request, 'mealapp/meal.html', context)


def add_amount(request):
    if request.method =="POST":
        member_name     = int(request.POST['member_name'])
        amount          = request.POST['amount']

        models.AddAmount.objects.create(member_name_id = member_name, amount = amount)
        return redirect("/amount-list")

    context = {
        'member_lst': models.MemberInfo.objects.all(),
    }
    
    return render(request, 'mealapp/add-money.html', context)

def ammount_name_list(request):
    
    meal           = models.MemberInfo.objects.filter(status=True).order_by("id")

    context = {
        
        'meal'    : meal,
    }
    return render(request, 'mealapp/ammount-list.html', context)


def amount_list(request,id):
    if request.method == "POST":
        search = request.POST['search']
        search_bar = models.AddAmount.objects.filter(member_name_id__member_name__icontains = search)
        context = {
        'search_list': search_bar,
        }
        return render(request, 'mealapp/amount_list.html', context)

    context = {
        'amount_lst': models.AddAmount.objects.filter(member_name__id = id,status = True),
        'tatal_amount': models.AddAmount.objects.filter(member_name__id = id,status = True).aggregate(Sum('amount'))['amount__sum'],
    }
    return render(request, 'mealapp/ammount.html', context)

def add_bazar(request):
    if request.method =="POST":
        author        = request.POST['author']
        total_bazar   = request.POST['total_bazar']
        bazar_date    = request.POST['bazar_date']

        models.AddBazar.objects.create(author = author, total_bazar = total_bazar, bazar_date = bazar_date)
        return redirect("/bazar-list")
    
    return render(request, 'mealapp/add-bazar.html')

def bazar_list(request):
    if request.method =="POST":
        search = request.POST['search']
        search_list = models.AddBazar.objects.filter(Q(author__icontains = search)|Q(bazar_date__icontains = search))
        context = {
        'search_list': search_list,
        }
        return render(request, 'mealapp/bazars.html', context)

    context = {
        'bazar_lst': models.AddBazar.objects.filter(status = True),
        'tatal_bazar': models.AddBazar.objects.filter(status = True).aggregate(Sum('total_bazar'))['total_bazar__sum'],
    }
    return render(request, 'mealapp/bazars.html', context)

def login(request):
    if request.method=="POST":
        email     = request.POST['email']
        password  = request.POST['password']

        new_md5_obj = hashlib.md5(password.encode())
        enc_pass    = new_md5_obj.hexdigest()
        user        = models.user_reg.objects.filter(email = email, password = enc_pass)
        if user:
            request.session['email'] = user[0].email
            request.session['id'] = user[0].id
            return redirect("/index/")
    return render(request, "blogapp/login.html")


def user_create(request):
    if request.method=="POST":
        Name        = request.POST['Name']
        email       = request.POST['email']
        phone       = request.POST['phone']
        password    = request.POST['password']
        new_md5_obj     = hashlib.md5(password.encode())
        new_enc_pass    = new_md5_obj.hexdigest()
        cheak_email = models.user_reg.objects.filter(email = email)

        if not cheak_email:
            models.user_reg.objects.create(Name = Name, email = email, phone = phone, password = new_enc_pass)
            messages.success(request, "Registration Successfull")
            return redirect("/mm-login/")
            
        else:
            messages.warning(request, "Already This Email has an Account")
    else:
        messages.warning(request, "")

    return render(request, "blogapp/create.html")



def total(request):
    
    
    tatal_meal     = models.DailyMeal.objects.filter(status = True).aggregate(Sum('no_of_meal'))['no_of_meal__sum']
    tatal_bazar    = models.AddBazar.objects.filter(status = True).aggregate(Sum('total_bazar'))['total_bazar__sum']
    tatal_received = models.AddAmount.objects.filter(status = True).aggregate(Sum('amount'))['amount__sum']
    rest_money     = float(tatal_received) - float(tatal_bazar)
    mil_rate       = float(tatal_bazar) / float(tatal_meal)
    context = {

        'tatal_meal'    : tatal_meal,
        'tatal_bazar'    : tatal_bazar,
        'tatal_received'    : tatal_received,
        'rest_money'    : rest_money,
        'mil_rate'    : mil_rate,

    }
    return render(request, 'mealapp/total.html', context)


def total_name_list(request):
    
    total           = models.MemberInfo.objects.filter(status=True).order_by("id")

    context = {
        
        'total'    : total,
    }
    return render(request, 'mealapp/totalname.html', context)




def total_details(request,id):
    
    tatal_meal     = models.DailyMeal.objects.filter(member_name__id = id,status = True).aggregate(Sum('no_of_meal'))['no_of_meal__sum']
    tatal_amount   = models.AddAmount.objects.filter(member_name__id = id,status = True).aggregate(Sum('amount'))['amount__sum']
    tatal_bazar    = models.AddBazar.objects.filter(status = True).aggregate(Sum('total_bazar'))['total_bazar__sum']
    mil_rate       = float(tatal_bazar) / float(tatal_meal)
    cost           = float(mil_rate) * float(tatal_meal)
    final          = float(cost) - float(tatal_amount)

    context = {
        
        'total'    : total,
        'tatal_amount'    : tatal_amount,
        'mil_rate'    : mil_rate,
        'cost'    : cost,
        'final'    : final,
        'tatal_meal'    : tatal_meal,
    }
    return render(request, 'mealapp/totaldetails.html', context)






















































#------------------------------website-----------------------------------------------------
def index(request):
    if request.method == "POST":
        location      = request.POST['location'].strip()
        category      = int(request.POST['category'])
        subcategory   = int(request.POST['subcategory'])
        location1     =  models.Properte.objects.filter(Status=True, location__icontains = location, category_id = category , subcategory_id = subcategory)
        if location1:
            return render(request, "blogapp/properties.html",{ 'location1' : location1,})
        else:
            messages.warning(request, "No records found.Please try another")
    
    seo_contain = models.SeoContent.objects.filter(Status=True).first()
    service  = models.Service.objects.filter(Status=True).order_by("-id")
    agents   = models.Agent.objects.filter(Status=True).all()
    letest   = models.Properte.objects.filter(Status=True).order_by("-propertyID")
    slider   = models.Slider.objects.filter(Status = True).order_by("-id")
    suggest  = models.Properte.objects.filter(feature_property=True).order_by("-propertyID")

    context={
        'service'  : service,
        'agents'   : agents,
        'letest'   : letest,
        'suggest'  : suggest,
        'slider'   : slider,
        'seo_contain' : seo_contain,
    }
    return render(request, "blogapp/index.html",context)


def contact(request):
    if request.method=="POST":
        Name        = request.POST['Name']
        email       = request.POST['email']
        subject     = request.POST['subject']
        massage     = request.POST['massage']
        models.user_massage.objects.create(Name = Name, email = email, subject = subject, massage = massage)
        messages.success(request, "Massage sent to Admin")
    else:
        messages.warning(request, "")

    seo_contain = models.SeoContent.objects.filter(Status=True).first()
    context={
        'seo_contain' : seo_contain,
    }

    return render(request, "blogapp/contact.html",context)

def properties_detail(request, name):
    pro_name = name.replace('-', ' ')
    details = models.Properte.objects.filter(title = pro_name).first()
    models.Properte.objects.filter(title = pro_name).update(view =F('view') + 1)
    context={
        'details' : details,
    }

    return render(request, "blogapp/properties_detail.html",context)

def properties(request):
    if request.method == "POST":
        location      = request.POST['location']
        category      = request.POST['category']
        subcategory   = request.POST['subcategory']
        location1     = models.Properte.objects.filter( Status=True, location__icontains = location, category_id = category, subcategory_id = subcategory)       
        if location1:
            return render(request, "blogapp/properties.html",{ 'location1' : location1,})
        else:
            messages.warning(request, "No records found.Please try another")
        
    if request.method == "GET":
        location      = request.GET.get('propertyID')
        location1     =  models.Properte.objects.filter( propertyID = location )
        if location1:
            return render(request, "blogapp/properties.html",{ 'location1' : location1,})
    
    seo_contain = models.SeoContent.objects.filter(Status=True).first()
    post = models.Properte.objects.filter(Status=True).order_by("-propertyID")
    paginator = Paginator(post, 6) # Show 6 contacts per page

    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post = paginator.page(paginator.num_pages)


    context={
        'post' : post,
        'seo_contain' : seo_contain,
    }

    return render(request, "blogapp/properties.html",context)

def user_ad(request):
    if request.method=="POST":
        category          = int(request.POST[('category')])
        subcategory       = int(request.POST[('subcategory')])
        title             = request.POST['title']
        area              = request.POST['area']
        price             = request.POST['price']
        discription       = request.POST['discription']
        feature1          = request.POST['feature1']
        feature2          = request.POST['feature2']
        feature3          = request.POST['feature3']
        feature4          = request.POST['feature4']
        feature5          = request.POST['feature5']
        feature6          = request.POST['feature6']
        feature7          = request.POST['feature7']
        feature8          = request.POST['feature8']
        feature9          = request.POST['feature9']
        feature10         = request.POST['feature10']
        feature11         = request.POST['feature11']
        feature12         = request.POST['feature12']
        feature13         = request.POST['feature13']
        feature14         = request.POST['feature14']
        feature15         = request.POST['feature15']
        location          = request.POST['location']
        contact_name      = request.POST['contact_name']
        Phone_number      = request.POST['Phone_number']
        mail              = request.POST['mail']

        image1 = ""
        if bool(request.FILES.get('image1', False)) == True:
            file = request.FILES['image1']
            image1 = "property/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"property/"):
                os.mkdir(settings.MEDIA_ROOT+"property/")
            default_storage.save(settings.MEDIA_ROOT+"property/"+file.name, ContentFile(file.read()))
        
        image2 = ""
        if bool(request.FILES.get('image2', False)) == True:
            file = request.FILES['image2']
            image2 = "property/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"property/"):
                os.mkdir(settings.MEDIA_ROOT+"property/")
            default_storage.save(settings.MEDIA_ROOT+"property/"+file.name, ContentFile(file.read()))
        
        image3 = ""
        if bool(request.FILES.get('image3', False)) == True:
            file = request.FILES['image3']
            image3 = "property/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"property/"):
                os.mkdir(settings.MEDIA_ROOT+"property/")
            default_storage.save(settings.MEDIA_ROOT+"property/"+file.name, ContentFile(file.read()))
        
        image4 = ""
        if bool(request.FILES.get('image4', False)) == True:
            file = request.FILES['image4']
            image4 = "property/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"property/"):
                os.mkdir(settings.MEDIA_ROOT+"property/")
            default_storage.save(settings.MEDIA_ROOT+"property/"+file.name, ContentFile(file.read()))
        
        image5 = ""
        if bool(request.FILES.get('image5', False)) == True:
            file = request.FILES['image5']
            image5 = "property/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"property/"):
                os.mkdir(settings.MEDIA_ROOT+"property/")
            default_storage.save(settings.MEDIA_ROOT+"property/"+file.name, ContentFile(file.read()))
        
        models.Properte.objects.create(user_id = int(request.session['id']), mail = mail, area = area, Phone_number = Phone_number,contact_name = contact_name,location = location, category_id = category,
            subcategory_id = subcategory, image1 = image1, image2 = image2, image3 = image3,image4 = image4,
            image5=image5,title=title, price=price,discription=discription,feature1=feature1,feature2=feature2,
            feature3=feature3,feature4=feature4,feature5=feature5,feature6=feature6,feature7=feature7,feature8=feature8,feature9=feature9,feature10=feature10,feature11=feature11,feature12=feature12,feature13=feature13,feature14=feature14, feature15=feature15)
        messages.success(request, "Property sent to Admin.Please wait for Aproved. After Aproved it will automatically publish. ThankYou To stay with us")
    else:
        messages.warning(request, "")

    
    return render(request, "blogapp/user_ad.html")

def user_register(request):
    if request.method=="POST":
        Name        = request.POST['Name']
        email       = request.POST['email']
        phone       = request.POST['phone']
        password    = request.POST['password']
        new_md5_obj     = hashlib.md5(password.encode())
        new_enc_pass    = new_md5_obj.hexdigest()
        cheak_email = models.user_reg.objects.filter(email = email)

        if not cheak_email:
            models.user_reg.objects.create(Name = Name, email = email, phone = phone, password = new_enc_pass)
            messages.success(request, "Registration Successfull")
            
        else:
            messages.warning(request, "Already This Email has an Account")
    else:
        messages.warning(request, "")

    return render(request, "blogapp/register.html")

def signin(request):
    if request.method=="POST":
        email     = request.POST['email']
        password  = request.POST['password']

        new_md5_obj = hashlib.md5(password.encode())
        enc_pass    = new_md5_obj.hexdigest()
        user        = models.user_reg.objects.filter(email = email, password = enc_pass)
        if user:
            request.session['email'] = user[0].email
            request.session['id'] = user[0].id
            return redirect("/user-ac/")
    return render(request, "blogapp/signin.html")

def forgot_pass(request):
    if request.method=="POST":
        email     = request.POST['email']
        password  = request.POST['password']

        new_md5_obj = hashlib.md5(password.encode())
        enc_pass    = new_md5_obj.hexdigest()
        user        = models.user_reg.objects.filter(email = email).update( password = enc_pass)
        return redirect("/login/")
    return render(request, "blogapp/forgot_pass.html")

def user_ac(request):
    user_post = models.Properte.objects.filter( user_id = request.session['id'])

    context={
        'user_post' : user_post,
    }   
    return render(request, "blogapp/user_ac.html", context)

def logout(request):
    request.session['email'] = False
    return redirect("/login/")

def delete_post(request, id):
    models.Properte.objects.filter(propertyID = id).delete()
    return redirect("/user-ac/")

def edit_post(request, id):
    edit    = models.Properte.objects.get(propertyID = id)

    if request.method=="POST":
        category          = int(request.POST[('category')])
        subcategory       = int(request.POST[('subcategory')])
        title             = request.POST['title']
        area              = request.POST['area']
        price             = request.POST['price']
        discription       = request.POST['discription']
        feature1          = request.POST['feature1']
        feature2          = request.POST['feature2']
        feature3          = request.POST['feature3']
        feature4          = request.POST['feature4']
        feature5          = request.POST['feature5']
        feature6          = request.POST['feature6']
        feature7          = request.POST['feature7']
        feature8          = request.POST['feature8']
        feature9          = request.POST['feature9']
        feature10         = request.POST['feature10']
        feature11         = request.POST['feature11']
        feature12         = request.POST['feature12']
        feature13         = request.POST['feature13']
        feature14         = request.POST['feature14']
        feature15         = request.POST['feature15']
        location          = request.POST['location']
        contact_name      = request.POST['contact_name']
        Phone_number      = request.POST['Phone_number']
        mail              = request.POST['mail']

        
        image1 = edit.image1
        if bool(request.FILES.get('image1', False)) == True:
            property = models.Properte.objects.get(propertyID = id)
            if os.path.exists('/static/mealapp/media/property/'+str(property.title)):
                os.remove('/static/mealapp/media/property/'+str(property.title))

            file = request.FILES['image1']
            image1 = "property/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"property/"):
                os.mkdir(settings.MEDIA_ROOT+"property/")

            default_storage.save(settings.MEDIA_ROOT+"property/"+file.name, ContentFile(file.read()))

        if edit.image2:  
            image2 = edit.image2
        else:
            image2 = " "
            
        if bool(request.FILES.get('image2', False)) == True:
            property = models.Properte.objects.get(propertyID = id)
            if os.path.exists('/static/mealapp/media/property/'+str(property.title)):
                os.remove('/static/mealapp/media/property/'+str(property.title))

            file = request.FILES['image2']
            image2 = "property/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"property/"):
                os.mkdir(settings.MEDIA_ROOT+"property/")

            default_storage.save(settings.MEDIA_ROOT+"property/"+file.name, ContentFile(file.read()))



        if edit.image3:  
            image3 = edit.image3
        else:
            image3 = " "
            
        if bool(request.FILES.get('image3', False)) == True:
            property = models.Properte.objects.get(propertyID = id)
            if os.path.exists('/static/mealapp/media/property/'+str(property.title)):
                os.remove('/static/mealapp/media/property/'+str(property.title))

            file = request.FILES['image3']
            image3 = "property/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"property/"):
                os.mkdir(settings.MEDIA_ROOT+"property/")

            default_storage.save(settings.MEDIA_ROOT+"property/"+file.name, ContentFile(file.read()))



        if edit.image4:  
            image4 = edit.image4
        else:
            image4 = " "
            
        if bool(request.FILES.get('image4', False)) == True:
            property = models.Properte.objects.get(propertyID = id)
            if os.path.exists('/static/mealapp/media/property/'+str(property.title)):
                os.remove('/static/mealapp/media/property/'+str(property.title))

            file = request.FILES['image4']
            image4 = "property/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"property/"):
                os.mkdir(settings.MEDIA_ROOT+"property/")

            default_storage.save(settings.MEDIA_ROOT+"property/"+file.name, ContentFile(file.read()))




        if edit.image5:  
            image5 = edit.image5
        else:
            image5 = ""            
        if bool(request.FILES.get('image5', False)) == True:
            property = models.Properte.objects.get(propertyID = id)
            if os.path.exists('/static/mealapp/media/property/'+str(property.title)):
                os.remove('/static/mealapp/media/property/'+str(property.title))

            file = request.FILES['image5']
            image5 = "property/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"property/"):
                os.mkdir(settings.MEDIA_ROOT+"property/")

            default_storage.save(settings.MEDIA_ROOT+"property/"+file.name, ContentFile(file.read()))



        models.Properte.objects.filter(propertyID = id).update(user_id = int(request.session['id']), mail = mail, area = area, Phone_number = Phone_number,contact_name = contact_name,location = location, category_id = category,
            subcategory_id = subcategory, image1 = image1, image2 = image2, image3 = image3,image4 = image4,
            image5=image5,title=title, price=price,discription=discription,feature1=feature1,feature2=feature2,
            feature3=feature3,feature4=feature4,feature5=feature5,feature6=feature6,feature7=feature7,feature8=feature8,feature9=feature9,feature10=feature10,feature11=feature11,feature12=feature12,feature13=feature13,feature14=feature14, feature15=feature15)
        return redirect("/user-ac/")
    edit    = models.Properte.objects.get(propertyID = id)
    context={
        'edit' : edit,
    }
    return render(request, "blogapp/edit_post.html",context)


def about_us(request):
    about_us = models.About_us.objects.filter(Status = True).first()
    speach   = models.speach.objects.filter(Status=True).order_by("-id").first()
    seo_contain = models.SeoContent.objects.filter(Status=True).first()
    context={
        'seo_contain' : seo_contain,
        'about_us' : about_us,
        'speach'   : speach,
    } 
    return render(request, "blogapp/about_us.html",context)

def blog(request):
    if request.method == "POST":
        search        = request.POST['title']
        blogsearch    = models.blog.objects.filter( Status=True, title__icontains = search)
        if blogsearch:
            return render(request, "blogapp/blog.html",{ 'blogsearch' : blogsearch,})
        else:
            messages.warning(request, "No records found.Please try another")
    blog = models.blog.objects.filter(Status=True).order_by("-id")
    seo_contain = models.SeoContent.objects.filter(Status=True).first()
    paginator = Paginator(blog, 6) # Show 6 contacts per page

    page = request.GET.get('page')
    try:
        blog = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blog = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blog = paginator.page(paginator.num_pages)


    context={
        'seo_contain' : seo_contain,
        'blog' : blog,
    }
    return render(request, "blogapp/blog.html",context)

def blog_detail(request, name):
    pro_name = name.replace('-', ' ')
    details = models.blog.objects.filter(title = pro_name).first()
    models.blog.objects.filter(title = pro_name).update(view =F('view') + 1)

    context={
        'details' : details,
    }

    return render(request, "blogapp/blog_detail.html",context)


