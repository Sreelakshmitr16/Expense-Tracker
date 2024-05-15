from django.shortcuts import render,redirect
from django.views.generic import View
from budget.forms import TransactionForm,RegistrationForm,LoginForm
from budget.models import Transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from django.db.models import Sum,Count
from budget.decorator import signin_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.cache import never_cache
decs=[signin_required,never_cache]

# Create your views here.

# --------USER CREATION VIEW(SIGN UP VIEW)------------
# url:localhost:8000/budget/register/
# method:get,post
    
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,'register.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # data=form.cleaned_data
            # User.objects.create(**data)
            # User.objects.create_user(**form.cleaned_data)
            form.save()
            # print('register success')
            messages.success(request,'registration success')
            return redirect('signin')
        messages.error(request,'registration failed')
        return render(request,"register.html",{'form':form})
    

# ------------USER SIGNINVIEW-------------------
# url:localhost:8000/budget/signin/
# method:get,post
    
class SignInview(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{'form':form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            uname=data.get('username')
            pwd=data.get('password')
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                messages.success(request,'login success')
                return redirect('transaction-list')
        return render(request,'login.html',{'form':form})
    
#------------------USER SIGNOUTVIEW----------------------   
@method_decorator(decs,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request) 
        return redirect('signin')
    
# -------------TRANSACTION CREATE VIEW------------
# url:localhost:8000/budget/transactions/add/
# methor:get,post

@method_decorator([signin_required,never_cache],name="dispatch")
class TransactionCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TransactionForm()
        return render(request,"transaction_add.html",{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=TransactionForm(request.POST)
        if form.is_valid():
            form.instance.user_object=request.user
            form.save()
            messages.success(request,'transaction added successfully')
            return redirect('transaction-list')
        messages.error(request,'transaction adding failed')
        return render(request,"transaction_add.html",{'form':form})
    
# ------------TRANSACTION LISTING-----------------
# url:localhost:8000/budget/transactions/all/
# method:get
    
@method_decorator(decs,name="dispatch")
class TransactionListView(View):
    def get(self,request,*args,**kwargs):

        if not request.user.is_authenticated:
            return redirect('signin')
        
        qs=Transaction.objects.filter(user_object=request.user)
        cur_month=timezone.now().month
        cur_year=timezone.now().year
        group_by_qs=Transaction.objects.filter(   #to get the sum of incomes and expences in current mnth iin this year
            
            user_object=request.user,
            created_date__month=cur_month,
            created_date__year=cur_year
        ).values("type").annotate(type_sum=Sum('amount'),type_count=Count('type'))
        # print(group_by_qs)
        group_by_category_qs=Transaction.objects.filter(
            user_object=request.user,
            created_date__month=cur_month,
            created_date__year=cur_year
        ).values('category').annotate(cat_sum=Sum('amount'),cat_count=Count('category'))
        # print(group_by_category_qs)
        return render(request,'transaction_list.html',{'data':qs,'type_total':group_by_qs,'category_total':group_by_category_qs})
    


# -------------TRANSACTION-UPDATE-----------------
# url:localhost:8000/budget/transactions/{id}/change/
# method:get,post

@method_decorator(decs,name="dispatch")
class TransactionUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        transaction_object=Transaction.objects.get(id=id)
        form=TransactionForm(instance=transaction_object)
        return render(request,"transaction_edit.html",{'form':form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        transaction_object=Transaction.objects.get(id=id)
        form=TransactionForm(request.POST,instance=transaction_object)
        if form.is_valid():
            form.save()
            messages.success(request,'transaction updated successfully!!!')
            return redirect('transaction-list')
        messages.error(request,'transaction update failed')
        return render(request,"transaction_edit.html",{'form':form})


# -------------TRANSACTION-DELETE-----------
# url:localhost:8000/budget/transactions/{id}/remove/
# method:get
    
@method_decorator(decs,name="dispatch")
class TransactionDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Transaction.objects.get(id=id).delete()
        messages.success(request,'deleted sussessfully!!!')
        return redirect('transaction-list')
    

# ------------------TRANSACTION-DETAIL-------------
@method_decorator(decs,name="dispatch")
class TransactionDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Transaction.objects.get(id=id)
        return render(request,"transaction_detail.html",{'data':qs})
    



