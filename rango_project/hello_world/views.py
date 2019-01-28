from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpRequest
from hello_world.models import category,Page
from hello_world.models import student,UserProfile,User
from django.http import HttpResponseRedirect
from hello_world.forms import CategoryForm,PageForm,EditCategoryForm
from hello_world.forms import UserForm,UserProfileForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from datetime import datetime
from hello_world.bing_search import run_query
from registration.backends.simple.views import RegistrationView
import sqlite3



# Create your views here.

# def index(request):
#     # c=category()
#     # #if request.method == 'POST':
#     # c.name='Viral'
#     # c.save()
#     #return HttpResponse("Hello Gangadhar")
#     return render(request,'design/createpost.html')


#Index Page
def index(request):
    request.session.set_test_cookie()
    category_list = category.objects.order_by('-likes')[:5]
    p = Page.objects.order_by('-views')[:5]
    #p = Page.objects.all()
    context_dict = {'categories':category_list,'pages':p}
    # p = Page.objects.all()
    # context_dict = {'pages':p}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request,'design/index.html',context=context_dict)
    return response
    #return render(request,'design/index.html',context=context_dict)

#End Of Index Page



#INSERT DATA INTO CATEGORY TABLE
def createpost(request):
        if request.method == 'POST':
            if request.POST.get('title'):
                post=category()
                post.name= request.POST.get('title')
                post.save()
                print("Done")
        return render(request,'design/createpost.html')           
#END OF INSERT DATA INTO CATEGORY TABLE


#INSERT DATA INTO STUDENT TABLE
def insert_student(request):
    if request.method == 'POST':
        s=student()
        s.erno=request.POST.get('erno')
        s.name=request.POST.get('name')
        s.city=request.POST.get('city')
        s.dob=request.POST.get('dob')
        s.email=request.POST.get('email')
        s.phone=request.POST.get('phone')
        s.save()
        print("done")
    return render(request,'design/student.html')
#END OF INSERT DATA INTO CATEGORY TABLE



def  show_category(request, category_name_slug):
    context_dict = {}
    try:
        cat = category.objects.get(slug=category_name_slug)
        cat.views = cat.views + 1
        cat.save()
        pages = Page.objects.filter(cat=cat)
        context_dict['pages'] = pages
        context_dict['category'] = cat
        context_dict['query'] = cat.name    
         
    except category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
     
    result_list = []
    
    if request.method == 'POST':
        
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list
    return render(request,'design/category.html',context_dict)

#***** ADD CATEGORY FORM *******
def add_category(request):
    # Cookie
    if request.session.test_cookie_worked():
        print("Worked")
        request.session.delete_test_cookie()
    # END
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save()
            form.save(commit=True)
            return index(request)
        
        else:
            print(form.errors)
    return render(request,'design/add_category.html',{'form':form})


#****** ADD PAGE FORM *******
def add_page(request,category_name_slug):
    try:
        cat1 = category.objects.get(slug=category_name_slug)
    except cat1.DoesNotExist:
        cat1 = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat1:
                page = form.save(commit=False)
                page.cat = cat1
                page.views = 0
                page.save()
                # form.save(commit = True)
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form,'category':cat1}
    return render(request,'design/add_page.html',context_dict)





#********** Register **********
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)

            profile = profile_form.save(commit = False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True

        else:
            print(user_form.errors,profile_form.errors)

    
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'design/register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

#********** End *********

#********** Login **********

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
                
            else:
                return HttpResponse("Your account is disabled.")

        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'design/login.html', {})

#********** End *********


#****** Restricting Access with a Decorator *******

@login_required
def restricted(request):
    '''
    restricted page for the users
    '''
    return HttpResponse("Since you're logged in, you can see this text!")

#********** End *********

#****** Logout *******

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

#********** End *********

#****** Edit Category *******
def edit_category(request,category_name_slug):
    '''
        Add a Category
    '''
    cat2 = None
    cat2 = category.objects.get(slug=category_name_slug)
    # try:
    
    # except cat2.DoesNotExist:
    #     cat2 = None

    form =  EditCategoryForm()
    if request.method == 'POST':
        form =  EditCategoryForm(request.POST,instance=cat2)
        if form.is_valid():
            if cat2:
                form = form.save(commit=False)
                form.save()
                return index(request)

        else:
            print(form.errors)
    contxt_dict = {'form':form,'category':cat2}
    return render(request,'design/edit_category.html',contxt_dict)

#****** End *******


#******* VISIT PAGE ******* 

def get_server_side_cookie(request,cookie,default_val=None):
    '''
        Get Sever Site Cookies
    '''
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    '''
        This is a function to handle visitor cookie
    '''
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    if(datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits






# def visitor_cookie_handler(request,response):
#     visits = int(request.COOKIES.get('visits','1'))
#     last_visit_cookie = request.COOKIES.get('last_visit',str(datetime.now()))
#     last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
#     if(datetime.now() - last_visit_time).days > 0:
#         visits = visits + 1
#         response.set_cookie('last_visit',str(datetime.now()))
#     else:
#         visits = 1
#         response.set_cookie('last_visit',last_visit_cookie)
#     response.set_cookie('visits',visits)


#******* END VISIT PAGE ******* 


def about(request):
    '''
        This is a about page function
    '''
    category_list = category.objects.order_by('name')[:1]
    context_dict = {'cat':category_list}
    return render(request,'design/about.html',context_dict)

def about1(request):
    '''
        This is a about page function'''
    return render(request,'design/about1.html')

def dashboard(request):
    category_list = category.objects.order_by('-likes')[:5]
    p = Page.objects.order_by('-views')[:5]
    #p = Page.objects.all()
    context_dict = {'categories':category_list,'pages':p}
    return render(request,'design/dashboard.html',context_dict)


def track_url(request):
    '''
        Update Page views
    '''
    p_id = None
    url = ''
    if request.method == 'GET':
        if 'p_id' in request.GET:
            p_id = request.GET['p_id']
            try:
                p = Page.objects.get(id=p_id)
                p.views = p.views + 1
                url = p.url
                p.save()
            except:
                pass
    return redirect(url)




def search(request):
    result_list = []
    query = ''
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
    return render(request,'design/search.html',{'result_list':result_list,'query':query})



@login_required
def register_profile(request):
    '''
        User Profile Registration Code
    '''
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
    context_dict = {'form':form}
    return render(request,'design/profile_registration.html',context_dict)


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user): 
        return reverse('register_profile')


@login_required
def profile(request,username):
    ''' 
        View and Update User Profile
    '''
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': userprofile.website,'picture': userprofile.picture})
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile',user.username)
        else:
            print(form.errors)
    return render(request,'design/profile.html',{'userprofile':userprofile,'selecteduser':user,'form':form})


@login_required
def profiles_list(request):
    ''' Profile List of Registered Users '''
    userprofile_list = UserProfile.objects.all()
    return render(request,'design/profile_list.html',{'userprofile_list':userprofile_list})

@login_required
def like_category(request):
    '''
        Like Catgeory Function 
    '''
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
    likes = 0
    if cat_id:
        cat = category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)

def get_category_list(max_results=0, starts_with=''):
    '''
        Get list of categories name from the Catgeory Model
    '''
    cat_list = []
    if starts_with:
        cat_list = category.objects.filter(name__istartswith=starts_with)
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list

@login_required
def suggest_category(request):
    '''
        Show suggestion according to the category name
    '''
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(8,starts_with)
    return render(request,'design/cats.html',{'cats':cat_list})

def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET.get('category_id')
        url = request.GET.get('url')
        title = request.GET.get('title')
        if cat_id:
            cat1 = category.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(cat = cat1,title=title,url=url)
            pages = Page.objects.filter(cat=cat1).order_by('-views')
            context_dict['pages'] = pages
    return render(request,'design/page_list.html',context_dict)
