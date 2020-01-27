import sys
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
global ins
ins=-1
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
global final_list
final_list=[]
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
                #print(i)
                if form.cleaned_data.get('course %d' %i) in listx:
                    pass
                else:
                    listx.append((course.objects.filter(course_code=(form.cleaned_data.get('course %d' %i)).upper()))[0])
                    try:
                        listx.append((course.objects.filter(course_code=(form.cleaned_data.get('course %d' %i)).upper()+'L'))[0])
                    except:
                        pass
            if form.cleaned_data.get('theory')=='Either Morning or Evening Theory':
                return redirect('/output')
            elif form.cleaned_data.get('theory')=='Morning Only Theory':
                return redirect('/morning_only')
            elif form.cleaned_data.get('theory')=='Evening Only Theory':
                return redirect('/evening_only')
            elif form.cleaned_data.get('theory')=='All':
                return redirect('/any_theory')
            #print(listx)

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
        #if column[0]=='423':
        #print(column)
        if column[3][0]=='L':

            if len(course.objects.filter(course_code=column[1]+'L'))==0:
                s=course.objects.update_or_create(
                    course_code=column[1]+'L',
                    course_title=course.objects.filter(course_code=column[1])[0].course_title,
                    l_credits=0,
                    p_credits=0,
                    t_credits=0,
                    j_credits=0,
                )
            column[1] = course.objects.filter(course_code=(column[1]+'L'))
        else:
            column[1] = course.objects.filter(course_code=(column[1]))
        column[1]=column[1][0]
        column[2] = teacher.objects.filter(name=column[2])
        column[2]=column[2][0]
        column[3]=column[3].split('+')
        for i in range (len(column[3])):
            x = slot.objects.filter(slot_name=column[3][i])
            x=x[0]
            s=offering.objects.update_or_create(
                offer_id=column[0],
                course_code=column[1],
                emp_code=column[2],
            )
            y=offering.objects.filter(offer_id=column[0])
            y=column[0][0]
            s=offer_set.objects.update_or_create(
                offer_id=s[0],
                slot_id=x,
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
        if column[3]!='0':
            s=course.objects.update_or_create(
                course_code=column[0]+'L',
                course_title=column[1],
                l_credits=column[2],
                p_credits=column[3],
                t_credits=column[4],
                j_credits=column[5],
            )
    return redirect('/')
def output(request):
    global listx
    global final_list
    global offer_id
    offer_id = []
    offer_id1=[]

    for i in listx:
        x=offering.objects.filter(course_code=i)
        q=[]
        p=0
        k1=[]
        #print(x)
        for j in x:
            k2=[]
            k=[]
            t=offer_set.objects.filter(offer_id=j)
            #print(j.offer_id,t)

            for c in t:
            #    #print(c.slot_id.slot_name,end=' ')
                y=slot.objects.filter(slot_name=c.slot_id.slot_name)
                if c.slot_id.slot_name not in k2:
                    k2.append(c.slot_id.slot_name)
                for d in y:
                    k.append(int(d.slot_id))

            #print(k2)
            #print(k,q)
            if (k in q) or p==1:
                pass
            else:
                q.append(k)
                k1.append(k2)
        if q!=[]:
            offer_id.append(q)
        if k1!=[]:
            offer_id1.append(k1)
    #print(offer_id)
    lenlistx=len(listx)
    #print(offer_id1,'\n',offer_id)
    global course_list
    course_list=[]
    global course_list2
    course_list2=[]
    global course_list3
    course_list3=[]
    try:
        for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8],offer_id[9],offer_id[10],offer_id[11]):
            #print(j)
            course_list2.append(j)
    except:
        try:
            for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8],offer_id[9],offer_id[10]):
                #print(j)
                course_list2.append(j)
        except:
            try:
                for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8],offer_id[9]):
                    #print(j)
                    course_list2.append(j)
            except:
                try:
                    for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8]):
                        #print(j)
                        course_list2.append(j)
                except:
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
    #print(len(course_list2))
    final_list=[]
    can_list=[]
    final_course_list=[]
    c=0
    global final_courses
    final_courses=[]
    #print(k1)
    #print('hi')
    #print(len(k1))
    try:
    	for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8],offer_id1[9],offer_id1[10],offer_id1[11]):
    		#print(j)
    		course_list3.append(j)
    except:
    	try:
    		for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8],offer_id1[9],offer_id1[10]):
    			#print(j)
    			course_list3.append(j)
    	except:
    		try:
    			for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8],offer_id1[9]):
    				#print(j)
    				course_list3.append(j)
    		except:
    			try:
    				for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8]):
    					#print(j)
    					course_list3.append(j)
    			except:
    				try:
    					for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7]):
    						#print(j)
    						course_list3.append(j)
    				except:
    					try:
    						for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6]):
    							#print(j)
    							course_list3.append(j)
    					except:
    						try:
    							for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5]):
    								#print(j)
    								course_list3.append(j)
    						except:
    							try:
    								for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4]):
    									#print(j)
    									course_list3.append(j)
    							except:
    								try:
    									for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3]):
    										#print(j)
    										course_list3.append(j)
    								except:
    									try:
    										for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2]):
    											#print(j)
    											course_list3.append(j)
    									except:
    										try:
    											for j in it.product(offer_id1[0],offer_id1[1]):
    												#print(j)
    												course_list3.append(j)
    										except:
    											for j in it.product(offer_id1[0]):
    												#print(j)
    												course_list3.append(j)
    #print('hi')
    final_course_list1=[]
    course_list1=[]
    for i in course_list3:
    	x=[]
    	y=[]
    	for j in i:
    		for k in j:
    			x.append(k)
                #   #print(str(i),str(j),str(k))
    			y.append(listx[(i.index(j))])
    	final_course_list1.append(y)
    	course_list1.append(x)


    #print(listx)
    for i in range(lenlistx):
        #print(str(listx[i]))
        listx[i]=str(listx[i])[15:-1:]
    for i in course_list2:
        x=[]
        y=[]
        for j in i:
            for k in j:
                x.append(k)
                y.append(listx[(i.index(j))])
        final_course_list.append(y)
        course_list.append(x)


    del course_list2
    #print(course_list1[0])
    for i in range(len(final_course_list1)-1,-1,-1):
        m=0
        e=0
        for j in course_list1[i]:
            if j[0]!='L' and j[1]=='1':
                m=1
            if j[0]!='L' and j[1]=='2':
                e=1
        if m==1 and e==1:
            final_course_list.pop(i)
            course_list.pop(i)
            course_list1.pop(i)
    #print(course_list)
    #print(len(final_course_list[0]))
    #print(final_course_list,course_list)
    #print(final_course_list)
    for i in range(len(final_course_list)):
        #print(i)
        i_list=[]
        for j in range(len(course_list[i])-1):
            for k in range(len(course_list[i])-1):
                if(course_list[i][k]>course_list[i][k+1]):
                    temp=course_list[i][k]
                    course_list[i][k]=course_list[i][k+1]
                    course_list[i][k+1]=temp
                    temp=final_course_list[i][k]
                    final_course_list[i][k]=final_course_list[i][k+1]
                    final_course_list[i][k+1]=temp
                if(course_list[i][k]==course_list[i][k+1]):
                    i_list.append(i)

        if i_list==[]:
            final_list.append(course_list[i])
            c+=1
            final_courses.append(final_course_list[i])
        # x=set(i)
        # w=list(x)
        # y=list(i)
        # z=sorted(y)
        #print(w,x,y,z)
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
         #    can_list.append(canvas
    if final_list==[]:
        return render(request,'failed2.html')
    #print(c)
    global final_dict
    final_dict=[]
    global final_dict2
    final_dict2=[]
    for i in final_list:
        c=0
        final_dict.append([])
        final_dict2.append([])
        for j in range(1,61):
            if j in i:
                final_dict[len(final_dict)-1].append(1)
                final_dict2[len(final_dict2)-1].append(final_courses[final_list.index(i)][c])
                c+=1
            else:
                final_dict[len(final_dict)-1].append(0)
                final_dict2[len(final_dict2)-1].append('')
    #print(len(final_dict))
    return redirect('/output_page_next/')

def any_theory(request):
    global listx
    global final_list
    global offer_id
    offer_id = []
    offer_id1=[]

    for i in listx:
        x=offering.objects.filter(course_code=i)
        q=[]
        p=0
        k1=[]
        #print(x)
        for j in x:
            k2=[]
            k=[]
            t=offer_set.objects.filter(offer_id=j)
            #print(j.offer_id,t)

            for c in t:
            #    #print(c.slot_id.slot_name,end=' ')
                y=slot.objects.filter(slot_name=c.slot_id.slot_name)
                if c.slot_id.slot_name not in k2:
                    k2.append(c.slot_id.slot_name)
                for d in y:
                    k.append(int(d.slot_id))

            #print(k2)
            #print(k,q)
            if (k in q) or p==1:
                pass
            else:
                q.append(k)
                k1.append(k2)
        if q!=[]:
            offer_id.append(q)
        if k1!=[]:
            offer_id1.append(k1)
    #print(offer_id)
    lenlistx=len(listx)
    #print(offer_id1,'\n',offer_id)
    global course_list
    course_list=[]
    global course_list2
    course_list2=[]
    global course_list3
    course_list3=[]
    try:
        for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8],offer_id[9],offer_id[10],offer_id[11]):
            #print(j)
            course_list2.append(j)
    except:
        try:
            for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8],offer_id[9],offer_id[10]):
                #print(j)
                course_list2.append(j)
        except:
            try:
                for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8],offer_id[9]):
                    #print(j)
                    course_list2.append(j)
            except:
                try:
                    for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8]):
                        #print(j)
                        course_list2.append(j)
                except:
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
    #print(len(course_list2))
    final_list=[]
    can_list=[]
    final_course_list=[]
    c=0
    global final_courses
    final_courses=[]
    #print(k1)
    #print('hi')
    #print(len(k1))
    #print('hi')
    final_course_list1=[]
    course_list1=[]
    for i in course_list3:
    	x=[]
    	y=[]
    	for j in i:
    		for k in j:
    			x.append(k)
                #   #print(str(i),str(j),str(k))
    			y.append(listx[(i.index(j))])
    	final_course_list1.append(y)
    	course_list1.append(x)


    #print(listx)
    for i in range(lenlistx):
        #print(str(listx[i]))
        listx[i]=str(listx[i])[15:-1:]
    for i in course_list2:
        x=[]
        y=[]
        for j in i:
            for k in j:
                x.append(k)
                y.append(listx[(i.index(j))])
        final_course_list.append(y)
        course_list.append(x)


    del course_list2
    #print(course_list1[0])
    #print(course_list)
    #print(len(final_course_list[0]))
    #print(final_course_list,course_list)
    #print(final_course_list)
    for i in range(len(final_course_list)):
        #print(i)
        i_list=[]
        for j in range(len(course_list[i])-1):
            for k in range(len(course_list[i])-1):
                if(course_list[i][k]>course_list[i][k+1]):
                    temp=course_list[i][k]
                    course_list[i][k]=course_list[i][k+1]
                    course_list[i][k+1]=temp
                    temp=final_course_list[i][k]
                    final_course_list[i][k]=final_course_list[i][k+1]
                    final_course_list[i][k+1]=temp
                if(course_list[i][k]==course_list[i][k+1]):
                    i_list.append(i)

        if i_list==[]:
            final_list.append(course_list[i])
            c+=1
            final_courses.append(final_course_list[i])
        # x=set(i)
        # w=list(x)
        # y=list(i)
        # z=sorted(y)
        #print(w,x,y,z)
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
         #    can_list.append(canvas
    if final_list==[]:
        return render(request,'failed2.html')
    #print(c)
    global final_dict
    final_dict=[]
    global final_dict2
    final_dict2=[]
    for i in final_list:
        c=0
        final_dict.append([])
        final_dict2.append([])
        for j in range(1,61):
            if j in i:
                final_dict[len(final_dict)-1].append(1)
                final_dict2[len(final_dict2)-1].append(final_courses[final_list.index(i)][c])
                c+=1
            else:
                final_dict[len(final_dict)-1].append(0)
                final_dict2[len(final_dict2)-1].append('')
    #print(len(final_dict))
    global ins
    ins=-1
    return redirect('/output_page_next/')
    #print(final_dict,final_dict[0]['0'])

def evening_only(request):
    global listx
    global final_list
    global offer_id
    offer_id = []
    offer_id1=[]

    for i in listx:
        x=offering.objects.filter(course_code=i)
        q=[]
        p=0
        k1=[]
        #print(x)
        for j in x:
            k2=[]
            k=[]
            t=offer_set.objects.filter(offer_id=j)
            #print(j.offer_id,t)

            for c in t:
            #    #print(c.slot_id.slot_name,end=' ')
                y=slot.objects.filter(slot_name=c.slot_id.slot_name)
                if c.slot_id.slot_name not in k2:
                    k2.append(c.slot_id.slot_name)
                for d in y:
                    k.append(int(d.slot_id))

            #print(k2)
            #print(k,q)
            if (k in q) or p==1:
                pass
            else:
                q.append(k)
                k1.append(k2)
        if q!=[]:
            offer_id.append(q)
        if k1!=[]:
            offer_id1.append(k1)
    #print(offer_id)
    lenlistx=len(listx)
    #print(offer_id1,'\n',offer_id)
    global course_list
    course_list=[]
    global course_list2
    course_list2=[]
    global course_list3
    course_list3=[]
    try:
        for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8],offer_id[9],offer_id[10],offer_id[11]):
            #print(j)
            course_list2.append(j)
    except:
        try:
            for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8],offer_id[9],offer_id[10]):
                #print(j)
                course_list2.append(j)
        except:
            try:
                for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8],offer_id[9]):
                    #print(j)
                    course_list2.append(j)
            except:
                try:
                    for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8]):
                        #print(j)
                        course_list2.append(j)
                except:
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
        print('fail1')
        return render(request,'failed.html')
        #pri    nt(len(course_list2))
    final_list=[]
    can_list=[]
    final_course_list=[]
    c=0
    global final_courses
    final_courses=[]
    #print(k1)
    #print('hi')
    #print(len(k1))
    try:
    	for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8],offer_id1[9],offer_id1[10],offer_id1[11]):
    		#print(j)
    		course_list3.append(j)
    except:
    	try:
    		for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8],offer_id1[9],offer_id1[10]):
    			#print(j)
    			course_list3.append(j)
    	except:
    		try:
    			for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8],offer_id1[9]):
    				#print(j)
    				course_list3.append(j)
    		except:
    			try:
    				for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8]):
    					#print(j)
    					course_list3.append(j)
    			except:
    				try:
    					for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7]):
    						#print(j)
    						course_list3.append(j)
    				except:
    					try:
    						for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6]):
    							#print(j)
    							course_list3.append(j)
    					except:
    						try:
    							for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5]):
    								#print(j)
    								course_list3.append(j)
    						except:
    							try:
    								for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4]):
    									#print(j)
    									course_list3.append(j)
    							except:
    								try:
    									for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3]):
    										#print(j)
    										course_list3.append(j)
    								except:
    									try:
    										for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2]):
    											#print(j)
    											course_list3.append(j)
    									except:
    										try:
    											for j in it.product(offer_id1[0],offer_id1[1]):
    												#print(j)
    												course_list3.append(j)
    										except:
    											for j in it.product(offer_id1[0]):
    												#print(j)
    												course_list3.append(j)
    #print('hi')
    final_course_list1=[]
    course_list1=[]
    for i in course_list3:
    	x=[]
    	y=[]
    	for j in i:
    		for k in j:
    			x.append(k)
                #   #print(str(i),str(j),str(k))
    			y.append(listx[(i.index(j))])
    	final_course_list1.append(y)
    	course_list1.append(x)


    #print(listx)
    for i in range(lenlistx):
        #print(str(listx[i]))
        listx[i]=str(listx[i])[15:-1:]
    for i in course_list2:
        x=[]
        y=[]
        for j in i:
            for k in j:
                x.append(k)
                y.append(listx[(i.index(j))])
        final_course_list.append(y)
        course_list.append(x)


    del course_list2
    #print(course_list1[0])
    for i in range(len(final_course_list1)-1,-1,-1):
        m=0
        e=0
        #print(course_list1[i])
        for j in course_list1[i]:
            if j[0]!='L' and j[len(j)-1]=='1':
                m=1
            if j[0]!='L' and j[len(j)-1]=='2':
                e=1
        if m==1:
            print(course_list1[i])
            final_course_list.pop(i)
            course_list.pop(i)
            course_list1.pop(i)
    #print(course_list)
    #print(len(final_course_list[0]))
    #print(final_course_list,course_list)
    #print(final_course_list)
    for i in range(len(final_course_list)):
        #print(i)
        i_list=[]
        for j in range(len(course_list[i])-1):
            for k in range(len(course_list[i])-1):
                if(course_list[i][k]>course_list[i][k+1]):
                    temp=course_list[i][k]
                    course_list[i][k]=course_list[i][k+1]
                    course_list[i][k+1]=temp
                    temp=final_course_list[i][k]
                    final_course_list[i][k]=final_course_list[i][k+1]
                    final_course_list[i][k+1]=temp
                if(course_list[i][k]==course_list[i][k+1]):
                    i_list.append(i)

        if i_list==[]:
            final_list.append(course_list[i])
            c+=1
            final_courses.append(final_course_list[i])
        # x=set(i)
        # w=list(x)
        # y=list(i)
        # z=sorted(y)
        #print(w,x,y,z)
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
         #    can_list.append(canvas
    if final_list==[]:
        print('fail2')
        return render(request,'failed2.html')

    #print(c)
    global final_dict
    final_dict=[]
    global final_dict2
    final_dict2=[]
    for i in final_list:
        c=0
        final_dict.append([])
        final_dict2.append([])
        for j in range(1,61):
            if j in i:
                final_dict[len(final_dict)-1].append(1)
                final_dict2[len(final_dict2)-1].append(final_courses[final_list.index(i)][c])
                c+=1
            else:
                final_dict[len(final_dict)-1].append(0)
                final_dict2[len(final_dict2)-1].append('')
    #print(len(final_dict))
    global ins
    ins=-1
    return redirect('/output_page_next/')
def morning_only(request):
    global listx
    global final_list
    global offer_id
    offer_id = []
    offer_id1=[]

    for i in listx:
        x=offering.objects.filter(course_code=i)
        q=[]
        p=0
        k1=[]
        #print(x)
        for j in x:
            k2=[]
            k=[]
            t=offer_set.objects.filter(offer_id=j)
            #print(j.offer_id,t)

            for c in t:
            #    #print(c.slot_id.slot_name,end=' ')
                y=slot.objects.filter(slot_name=c.slot_id.slot_name)
                if c.slot_id.slot_name not in k2:
                    k2.append(c.slot_id.slot_name)
                for d in y:
                    k.append(int(d.slot_id))

            #print(k2)
            #print(k,q)
            if (k in q) or p==1:
                pass
            else:
                q.append(k)
                k1.append(k2)
        if q!=[]:
            offer_id.append(q)
        if k1!=[]:
            offer_id1.append(k1)
    #print(offer_id)
    lenlistx=len(listx)
    #print(offer_id1,'\n',offer_id)
    global course_list
    course_list=[]
    global course_list2
    course_list2=[]
    global course_list3
    course_list3=[]
    try:
        for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8],offer_id[9],offer_id[10],offer_id[11]):
            #print(j)
            course_list2.append(j)
    except:
        try:
            for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8],offer_id[9],offer_id[10]):
                #print(j)
                course_list2.append(j)
        except:
            try:
                for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8],offer_id[9]):
                    #print(j)
                    course_list2.append(j)
            except:
                try:
                    for j in it.product(offer_id[0],offer_id[1],offer_id[2],offer_id[3],offer_id[4],offer_id[5],offer_id[6],offer_id[7],offer_id[8]):
                        #print(j)
                        course_list2.append(j)
                except:
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
    #print(len(course_list2))
    final_list=[]
    can_list=[]
    final_course_list=[]
    c=0
    global final_courses
    final_courses=[]
    #print(k1)
    #print('hi')
    #print(len(k1))
    try:
    	for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8],offer_id1[9],offer_id1[10],offer_id1[11]):
    		#print(j)
    		course_list3.append(j)
    except:
    	try:
    		for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8],offer_id1[9],offer_id1[10]):
    			#print(j)
    			course_list3.append(j)
    	except:
    		try:
    			for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8],offer_id1[9]):
    				#print(j)
    				course_list3.append(j)
    		except:
    			try:
    				for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7],offer_id1[8]):
    					#print(j)
    					course_list3.append(j)
    			except:
    				try:
    					for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6],offer_id1[7]):
    						#print(j)
    						course_list3.append(j)
    				except:
    					try:
    						for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5],offer_id1[6]):
    							#print(j)
    							course_list3.append(j)
    					except:
    						try:
    							for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4],offer_id1[5]):
    								#print(j)
    								course_list3.append(j)
    						except:
    							try:
    								for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3],offer_id1[4]):
    									#print(j)
    									course_list3.append(j)
    							except:
    								try:
    									for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2],offer_id1[3]):
    										#print(j)
    										course_list3.append(j)
    								except:
    									try:
    										for j in it.product(offer_id1[0],offer_id1[1],offer_id1[2]):
    											#print(j)
    											course_list3.append(j)
    									except:
    										try:
    											for j in it.product(offer_id1[0],offer_id1[1]):
    												#print(j)
    												course_list3.append(j)
    										except:
    											for j in it.product(offer_id1[0]):
    												#print(j)
    												course_list3.append(j)
    #print('hi')
    final_course_list1=[]
    course_list1=[]
    for i in course_list3:
    	x=[]
    	y=[]
    	for j in i:
    		for k in j:
    			x.append(k)
                #   #print(str(i),str(j),str(k))
    			y.append(listx[(i.index(j))])
    	final_course_list1.append(y)
    	course_list1.append(x)


    #print(listx)
    for i in range(lenlistx):
        #print(str(listx[i]))
        listx[i]=str(listx[i])[15:-1:]
    for i in course_list2:
        x=[]
        y=[]
        for j in i:
            for k in j:
                x.append(k)
                y.append(listx[(i.index(j))])
        final_course_list.append(y)
        course_list.append(x)


    del course_list2
    #print(course_list1[0])
    for i in range(len(final_course_list1)-1,-1,-1):
        m=0
        e=0
        for j in course_list1[i]:
            if j[0]!='L' and j[1]=='1':
                m=1
            if j[0]!='L' and j[1]=='2':
                e=1
        if e==1:
            final_course_list.pop(i)
            course_list.pop(i)
            course_list1.pop(i)
    #print(course_list)
    #print(len(final_course_list[0]))
    #print(final_course_list,course_list)
    #print(final_course_list)
    for i in range(len(final_course_list)):
        #print(i)
        i_list=[]
        for j in range(len(course_list[i])-1):
            for k in range(len(course_list[i])-1):
                if(course_list[i][k]>course_list[i][k+1]):
                    temp=course_list[i][k]
                    course_list[i][k]=course_list[i][k+1]
                    course_list[i][k+1]=temp
                    temp=final_course_list[i][k]
                    final_course_list[i][k]=final_course_list[i][k+1]
                    final_course_list[i][k+1]=temp
                if(course_list[i][k]==course_list[i][k+1]):
                    i_list.append(i)

        if i_list==[]:
            final_list.append(course_list[i])
            c+=1
            final_courses.append(final_course_list[i])
        # x=set(i)
        # w=list(x)
        # y=list(i)
        # z=sorted(y)
        #print(w,x,y,z)
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
         #    can_list.append(canvas
    if final_list==[]:
        return render(request,'failed2.html')
    #print(c)
    global final_dict
    final_dict=[]
    global final_dict2
    final_dict2=[]
    for i in final_list:
        c=0
        final_dict.append([])
        final_dict2.append([])
        for j in range(1,61):
            if j in i:
                final_dict[len(final_dict)-1].append(1)
                final_dict2[len(final_dict2)-1].append(final_courses[final_list.index(i)][c])
                c+=1
            else:
                final_dict[len(final_dict)-1].append(0)
                final_dict2[len(final_dict2)-1].append('')
    #print(len(final_dict))
    global ins
    ins=-1
    return redirect('/output_page_next/')
    #print(final_dict,final_dict[0]['0'])
def output_page_next(request):
    global ins
    global final_dict
    global final_dict2
    global final_courses
    print(final_dict2)
    #print(final_dict)

    if request.method=='POST':
        form=gotoform(request.POST)
        if form.is_valid():
            ins=int(form.cleaned_data.get('num'))
            ins-=2
    else:
        form=gotoform()
    ins+=1
    if ins==len(final_dict):
        ins=0
    #print(ins)
    return render(request,'output.html',{
        'form':form,
        'i':ins+1,
        'n':len(final_dict),
        'k1':final_dict[ins][0],
        'k2':final_dict[ins][1],
        'k3':final_dict[ins][2],
        'k4':final_dict[ins][3],
        'k5':final_dict[ins][4],
        'k6':final_dict[ins][5],
        'k7':final_dict[ins][6],
        'k8':final_dict[ins][7],
        'k9':final_dict[ins][8],
        'k10':final_dict[ins][9],
        'k11':final_dict[ins][10],
        'k12':final_dict[ins][11],
        'k13':final_dict[ins][12],
        'k14':final_dict[ins][13],
        'k15':final_dict[ins][14],
        'k16':final_dict[ins][15],
        'k17':final_dict[ins][16],
        'k18':final_dict[ins][17],
        'k19':final_dict[ins][18],
        'k20':final_dict[ins][19],
        'k21':final_dict[ins][20],
        'k22':final_dict[ins][21],
        'k23':final_dict[ins][22],
        'k24':final_dict[ins][23],
        'k25':final_dict[ins][24],
        'k26':final_dict[ins][25],
        'k27':final_dict[ins][26],
        'k28':final_dict[ins][27],
        'k29':final_dict[ins][28],
        'k30':final_dict[ins][29],
        'k31':final_dict[ins][30],
        'k32':final_dict[ins][31],
        'k33':final_dict[ins][32],
        'k34':final_dict[ins][33],
        'k35':final_dict[ins][34],
        'k36':final_dict[ins][35],
        'k37':final_dict[ins][36],
        'k38':final_dict[ins][37],
        'k39':final_dict[ins][38],
        'k40':final_dict[ins][39],
        'k41':final_dict[ins][40],
        'k42':final_dict[ins][41],
        'k43':final_dict[ins][42],
        'k44':final_dict[ins][43],
        'k45':final_dict[ins][44],
        'k46':final_dict[ins][45],
        'k47':final_dict[ins][46],
        'k48':final_dict[ins][47],
        'k49':final_dict[ins][48],
        'k50':final_dict[ins][49],
        'k51':final_dict[ins][50],
        'k52':final_dict[ins][51],
        'k53':final_dict[ins][52],
        'k54':final_dict[ins][53],
        'k55':final_dict[ins][54],
        'k56':final_dict[ins][55],
        'k57':final_dict[ins][56],
        'k58':final_dict[ins][57],
        'k59':final_dict[ins][58],
        'k60':final_dict[ins][59],

        'l1':final_dict2[ins][0],
        'l2':final_dict2[ins][1],
        'l3':final_dict2[ins][2],
        'l4':final_dict2[ins][3],
        'l5':final_dict2[ins][4],
        'l6':final_dict2[ins][5],
        'l7':final_dict2[ins][6],
        'l8':final_dict2[ins][7],
        'l9':final_dict2[ins][8],
        'l10':final_dict2[ins][9],
        'l11':final_dict2[ins][10],
        'l12':final_dict2[ins][11],
        'l13':final_dict2[ins][12],
        'l14':final_dict2[ins][13],
        'l15':final_dict2[ins][14],
        'l16':final_dict2[ins][15],
        'l17':final_dict2[ins][16],
        'l18':final_dict2[ins][17],
        'l19':final_dict2[ins][18],
        'l20':final_dict2[ins][19],
        'l21':final_dict2[ins][20],
        'l22':final_dict2[ins][21],
        'l23':final_dict2[ins][22],
        'l24':final_dict2[ins][23],
        'l25':final_dict2[ins][24],
        'l26':final_dict2[ins][25],
        'l27':final_dict2[ins][26],
        'l28':final_dict2[ins][27],
        'l29':final_dict2[ins][28],
        'l30':final_dict2[ins][29],
        'l31':final_dict2[ins][30],
        'l32':final_dict2[ins][31],
        'l33':final_dict2[ins][32],
        'l34':final_dict2[ins][33],
        'l35':final_dict2[ins][34],
        'l36':final_dict2[ins][35],
        'l37':final_dict2[ins][36],
        'l38':final_dict2[ins][37],
        'l39':final_dict2[ins][38],
        'l40':final_dict2[ins][39],
        'l41':final_dict2[ins][40],
        'l42':final_dict2[ins][41],
        'l43':final_dict2[ins][42],
        'l44':final_dict2[ins][43],
        'l45':final_dict2[ins][44],
        'l46':final_dict2[ins][45],
        'l47':final_dict2[ins][46],
        'l48':final_dict2[ins][47],
        'l49':final_dict2[ins][48],
        'l50':final_dict2[ins][49],
        'l51':final_dict2[ins][50],
        'l52':final_dict2[ins][51],
        'l53':final_dict2[ins][52],
        'l54':final_dict2[ins][53],
        'l55':final_dict2[ins][54],
        'l56':final_dict2[ins][55],
        'l57':final_dict2[ins][56],
        'l58':final_dict2[ins][57],
        'l59':final_dict2[ins][58],
        'l60':final_dict2[ins][59],
    })
def output_page_prev(request):
    global ins
    global final_dict
    global final_dict2
    global final_courses
    form=gotoform()
    #print(final_dict)
    ins-=1
    if ins==-1:
        ins=len(final_dict)-1

    if request.method=='POST':
        form=gotoform(request.POST)
        if form.is_valid():
            ins=int(form.cleaned_data.get('num'))
            ins-=2
    else:
        form=gotoform()
    return render(request,'output.html',{
        'form':form,
        'i':ins+1,
        'n':len(final_dict),
        'k1':final_dict[ins][0],
        'k2':final_dict[ins][1],
        'k3':final_dict[ins][2],
        'k4':final_dict[ins][3],
        'k5':final_dict[ins][4],
        'k6':final_dict[ins][5],
        'k7':final_dict[ins][6],
        'k8':final_dict[ins][7],
        'k9':final_dict[ins][8],
        'k10':final_dict[ins][9],
        'k11':final_dict[ins][10],
        'k12':final_dict[ins][11],
        'k13':final_dict[ins][12],
        'k14':final_dict[ins][13],
        'k15':final_dict[ins][14],
        'k16':final_dict[ins][15],
        'k17':final_dict[ins][16],
        'k18':final_dict[ins][17],
        'k19':final_dict[ins][18],
        'k20':final_dict[ins][19],
        'k21':final_dict[ins][20],
        'k22':final_dict[ins][21],
        'k23':final_dict[ins][22],
        'k24':final_dict[ins][23],
        'k25':final_dict[ins][24],
        'k26':final_dict[ins][25],
        'k27':final_dict[ins][26],
        'k28':final_dict[ins][27],
        'k29':final_dict[ins][28],
        'k30':final_dict[ins][29],
        'k31':final_dict[ins][30],
        'k32':final_dict[ins][31],
        'k33':final_dict[ins][32],
        'k34':final_dict[ins][33],
        'k35':final_dict[ins][34],
        'k36':final_dict[ins][35],
        'k37':final_dict[ins][36],
        'k38':final_dict[ins][37],
        'k39':final_dict[ins][38],
        'k40':final_dict[ins][39],
        'k41':final_dict[ins][40],
        'k42':final_dict[ins][41],
        'k43':final_dict[ins][42],
        'k44':final_dict[ins][43],
        'k45':final_dict[ins][44],
        'k46':final_dict[ins][45],
        'k47':final_dict[ins][46],
        'k48':final_dict[ins][47],
        'k49':final_dict[ins][48],
        'k50':final_dict[ins][49],
        'k51':final_dict[ins][50],
        'k52':final_dict[ins][51],
        'k53':final_dict[ins][52],
        'k54':final_dict[ins][53],
        'k55':final_dict[ins][54],
        'k56':final_dict[ins][55],
        'k57':final_dict[ins][56],
        'k58':final_dict[ins][57],
        'k59':final_dict[ins][58],
        'k60':final_dict[ins][59],
        'l1':final_dict2[ins][0],
        'l2':final_dict2[ins][1],
        'l3':final_dict2[ins][2],
        'l4':final_dict2[ins][3],
        'l5':final_dict2[ins][4],
        'l6':final_dict2[ins][5],
        'l7':final_dict2[ins][6],
        'l8':final_dict2[ins][7],
        'l9':final_dict2[ins][8],
        'l10':final_dict2[ins][9],
        'l11':final_dict2[ins][10],
        'l12':final_dict2[ins][11],
        'l13':final_dict2[ins][12],
        'l14':final_dict2[ins][13],
        'l15':final_dict2[ins][14],
        'l16':final_dict2[ins][15],
        'l17':final_dict2[ins][16],
        'l18':final_dict2[ins][17],
        'l19':final_dict2[ins][18],
        'l20':final_dict2[ins][19],
        'l21':final_dict2[ins][20],
        'l22':final_dict2[ins][21],
        'l23':final_dict2[ins][22],
        'l24':final_dict2[ins][23],
        'l25':final_dict2[ins][24],
        'l26':final_dict2[ins][25],
        'l27':final_dict2[ins][26],
        'l28':final_dict2[ins][27],
        'l29':final_dict2[ins][28],
        'l30':final_dict2[ins][29],
        'l31':final_dict2[ins][30],
        'l32':final_dict2[ins][31],
        'l33':final_dict2[ins][32],
        'l34':final_dict2[ins][33],
        'l35':final_dict2[ins][34],
        'l36':final_dict2[ins][35],
        'l37':final_dict2[ins][36],
        'l38':final_dict2[ins][37],
        'l39':final_dict2[ins][38],
        'l40':final_dict2[ins][39],
        'l41':final_dict2[ins][40],
        'l42':final_dict2[ins][41],
        'l43':final_dict2[ins][42],
        'l44':final_dict2[ins][43],
        'l45':final_dict2[ins][44],
        'l46':final_dict2[ins][45],
        'l47':final_dict2[ins][46],
        'l48':final_dict2[ins][47],
        'l49':final_dict2[ins][48],
        'l50':final_dict2[ins][49],
        'l51':final_dict2[ins][50],
        'l52':final_dict2[ins][51],
        'l53':final_dict2[ins][52],
        'l54':final_dict2[ins][53],
        'l55':final_dict2[ins][54],
        'l56':final_dict2[ins][55],
        'l57':final_dict2[ins][56],
        'l58':final_dict2[ins][57],
        'l59':final_dict2[ins][58],
        'l60':final_dict2[ins][59],

    })
