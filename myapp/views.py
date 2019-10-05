import itertools as it
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core import serializers
from .models import *
from .forms import *
import csv,io

from .readslots import read
#stripe.api_key = settings.STRIPE_SECRET_KEY
global form
form=0
global n
n=0
global i
i=0
global list
listx=[]
global offer_id
global course_list
global course_list2
# Create your views here.

def rslots(request):
    a=read('slot list.csv',2)
    for i in range(len(data)):
        s=slot(data[i][0],(data[i][1]))
        s.save()
    return(redirect('/'))
def rteachers(request):
    a=read('teachers.csv',3)
    for i in range(len(data)):
        s=teachers(data[i][0],(data[i][1]),data[i][2])
        s.save()
    return(redirect('/'))
def home(request):
    global offer_id
    global course_list
    global course_list2
    offer_id=[]
    course_list=[]
    course_list2=[]
    return render(request,'home.html')
def input2(request):
    global n
    global listx
    if request.method == 'POST':
        form=input2form(n,request.POST)
        if form.is_valid():
            #print(n,'hi')
            for i in range (int(n)):
                if form.cleaned_data.get('course %d' %i) in listx:
                    pass
                else:
                    listx.append(form.cleaned_data.get('course %d' %i))
            #print(listx)
            return redirect('/output')
    else:
        form=input2form(n)
        #print(form)
    return render(request, 'input2.html', {
        'form': form
    })
def input1(request):
    global n
    if request.method == 'POST':
        form = input1form(request.POST)
        if form.is_valid():
            n=int(form.cleaned_data.get('num'))
            #print(n)
        return(redirect('/input2'))
    else:
        form = input1form()
        #print(form)
    return render(request, 'input1.html', {
        'form': form
    })
#@permission_required('admin.can_add_log_entry')
def slot_up(request):
    if request.method=='GET':
        return render(request,'slot_up.html')
    csv_file=request.FILES['file']
    dataset=csv_file.read().decode('UTF-8')
    io_string=io.StringIO(dataset)
    next(io_string)
    for column in csv.reader(io_string,delimiter=',',quotechar="|"):
        s=slot.objects.update_or_create(
            slot_id=column[0],
            slot_name=column[1]
        )
    return redirect('/')
def teacher_up(request):
    if request.method=='GET':
        return render(request,'slot_up.html')
    csv_file=request.FILES['file']
    dataset=csv_file.read().decode('UTF-8')
    io_string=io.StringIO(dataset)
    next(io_string)
    for column in csv.reader(io_string,delimiter=',',quotechar="|"):
        s=teacher.objects.update_or_create(
            name=column[0],
            emp_code=column[1],
            school=column[2]
        )
    return redirect('/')
def offer_up(request):
    if request.method=='GET':
        return render(request,'slot_up.html')
    csv_file=request.FILES['file']
    dataset=csv_file.read().decode('UTF-8')
    io_string=io.StringIO(dataset)
    next(io_string)
    for column in csv.reader(io_string,delimiter=','):
        #print(str(column[3]))
         # considering you post user_list of usernames as 'username1,username2,username3'
        column[3] = slot.objects.filter(slot_name=column[3])
        column[3]=column[3][0]
        column[1] = course.objects.filter(course_code=column[1])
        column[1]=column[1][0]
        column[2] = teacher.objects.filter(emp_code=column[2])
        column[2]=column[2][0]
        s=offering.objects.update_or_create(
            offer_id=column[0],
            course_code=column[1],
            emp_code=column[2],
        )
        column[0]=offering.objects.filter(offer_id=column[0])
        column[0]=column[0][0]
        s=offer_set.objects.update_or_create(
            offer_id=column[0],
            slot_id=column[3]
        )
    return redirect('/')
def course_up(request):
    if request.method=='GET':
        return render(request,'slot_up.html')
    csv_file=request.FILES['file']
    dataset=csv_file.read().decode('UTF-8')
    io_string=io.StringIO(dataset)
    next(io_string)
    for column in csv.reader(io_string,delimiter=',',quotechar="|"):
        s=course.objects.update_or_create(
            course_code=column[0],
            course_title=column[1],
            l_credits=column[2],
            p_credits=column[3],
            t_credits=column[4],
            j_credits=column[5],
        )
    return redirect('/')
def output(request):
    global listx
    global offer_id
    offer_id = []
    for i in listx:
        x=offering.objects.filter(course_code=i)
        q=[]
        for j in x:
            k=[]
            t=offer_set.objects.filter(offer_id=j)
            t=list(t)
            for c in t:
                k.append(int(c.slot_id.slot_id))
            q.append(k)
        offer_id.append(q)
    #print(offer_id)
    listx=[]
    global course_list
    course_list=[]
    global course_list2
    course_list2=[]
    try:
        for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7]):
            #print(j)
            course_list2.append(j)
    except:
        try:
            for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6]):
                #print(j)
                course_list2.append(j)
        except:
            try:
                for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5]):
                    #print(j)
                    course_list2.append(j)
            except:
                try:
                    for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4]):
                        #print(j)
                        course_list2.append(j)
                except:
                    try:
                        for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3]):
                            #print(j)
                            course_list2.append(j)
                    except:
                        try:
                            for j in it.product(offer_id[0],offer_id[1],offer_id[2]):
                                #print(j)
                                course_list2.append(j)
                        except:
                            try:
                                for j in it.product(offer_id[0],offer_id[1]):
                                    #print(j)
                                    course_list2.append(j)
                            except:
                                for j in it.product(offer_id[0]):
                                    #print(j)
                                    course_list2.append(j)

    if course_list2==[]:
        return render(request,'failed.html')
    final_list=[]
    can_list=[]
    c=0
    for i in course_list2:
        x=[]
        for j in i:
            for k in j:
                x.append(k)
        course_list.append(x)
    #print(course_list)
    for i in course_list:
        x=set(i)
        w=list(x)
        y=list(i)
        z=sorted(y)
        #print(w,x,y,z)
        if(w!=z):
            pass
        else:
         #    for j in range(1,6,1):
         #        for k in range(1,6,1):
         #            canvas=tk.Canvas(width=500,height=200,bg='yellow')
         #            canvas.create_rectangle(240,0,260,200,outline='black',fill='white')
         #            if j*k in x:
         #                col='green'
         #            else:
         #                col='yellow'
         #    canvas.create_rectangle((j-1)*40,(k-1)*40,j*40,k*40,outline='black',fill=col)
         #    canvas.postscript(file ='p'+str(c)+ '.eps')
         # # use PIL to convert to PNG
         #    img = Image.open('p'+str(c)+'.eps')
         #    img.save('p'+str(c)+'.png','png')
         #    can_list.append(canvas)
            final_list.append(x)
            c+=1
    if final_list==[]:
        return render(request,'failed2.html')
    final_dict_mor=[]
    final_dict_eve=[]
    for i in final_list:
        x=[]
        for j in range(1,31,1):
            if(j%6)==1:
                x.append([])
            if j in i:
                x[len(x)-1].append(1)
            else:
                x[len(x)-1].append(0)

        final_dict_mor.append(x)
        x=[]
        for j in range(31,61,1):
            if(j%6)==1:
                x.append([])
            if j in i:
                x[len(x)-1].append(1)
            else:
                x[len(x)-1].append(0)

        final_dict_eve.append(x)

    i=0

    #print(final_dict,final_dict[0]['0'])
    return render(request,'output.html',{
        'final':final_list,
        'final_dict_mor':final_dict_mor,
        'final_dict_eve':final_dict_eve,
        #'canvas':can_list
    })
