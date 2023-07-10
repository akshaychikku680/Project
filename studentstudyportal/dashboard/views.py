from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.views.generic import TemplateView,DetailView,View
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"Please Login First!!!")
            return redirect("login")
    return inner

dec=[signin_required,never_cache]

# Create your views here.

class Home(TemplateView):
    template_name = 'dashboard/home.html'

@method_decorator(dec,name='dispatch')
class Note(View):
    def get(self,request,*args,**kwargs):
        form = NotesForm()
        notes = Notes.objects.filter(user=request.user)
        return render(request,'dashboard/notes.html',{'notes':notes,'form':form})
    
    def post(self,request,*args,**kwargs):
        us = request.user.username
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
            messages.success(request,"Notes Added from "+ us +" Successfully")
            return redirect("notes")
        else:
          return render(request,'dashboard/notes.html',{'form':form,'notes':notes})

# def notes(request):
#     if request.method == "POST":
#         form = NotesForm(request.POST)
#         if form.is_valid():
#             notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
#             notes.save()
#         messages.success(request,f"Notes Added from {request.user.username} Successfully")
#     else:
#         form = NotesForm()
#     notes = Notes.objects.filter(user=request.user)
#     context = {'notes':notes,'form':form}
#     return render(request,'dashboard/notes.html',context)

dec
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

@method_decorator(dec,name='dispatch')
class NotesDetailView(DetailView):
    model = Notes

@method_decorator(dec,name='dispatch')
class Hwork(View):
    def get(self,request,*args,**kwargs):
        form = HomeworkForm()
        homeworks = Homework.objects.filter(user=request.user)
        homeworks_done = 0
        if len(homeworks) == 0:
            homeworks_done = True
        else:
            homeworks_done == False
        context = {'homeworks':homeworks,'form':form,'homeworks_done':homeworks_done}
        return render(request,'dashboard/homework.html',context)
    
    def post(self,request,*args,**kwargs):
        us = request.user.username
        form = HomeworkForm(request.POST)
        homeworks = []
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished == False
            except:
                finished = False
            homeworks = Homework(user=request.user,subject=request.POST['subject'],title=request.POST['title'],description=request.POST['description'],due=request.POST['due'])
            homeworks.save()
            messages.success(request,'Homework Added from '+ us + '!!')
            return redirect('homework')
        else:
            context = {'homeworks':homeworks,'form':form}
            return render(request,'dashboard/homework.html',context)

# def homework(request):
#     if request.method == "POST":
#         form = HomeworkForm(request.POST)
#         if form.is_valid():
#             try:
#                 finished = request.POST['is_finished']
#                 if finished == 'on':
#                     finished = True
#                 else:
#                     finished == False
#             except:
#                 finished = False
#             homework = Homework(user=request.user,subject=request.POST['subject'],title=request.POST['title'],description=request.POST['description'],due=request.POST['due'])
#             homework.save()
#             messages.success(request,f'Homework Added from {request.user.username} !!')

#     else:
#         form = HomeworkForm()
#     homework = Homework.objects.filter(user=request.user)
#     homeworks_done = 0
#     if len(homework) == 0:
#         homeworks_done = True
#     else:
#         homeworks_done == False

#     context = {'homeworks':homework,'homeworks_done':homeworks_done,'form':form} 
#     return render(request,'dashboard/homework.html',context)

dec
def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

dec
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

class Youtube(View):
    def get(self,request,*args,**kwargs):
        form = DashboardForm()
        return render(request,"dashboard/youtube.html",{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = DashboardForm()
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list =[]
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {'form':form,'results':result_list}
        return render(request,"dashboard/youtube.html",context)

# def youtube(request):
#     if request.method == "POST":
#         form = DashboardForm(request.POST)
#         text = request.POST['text']
#         video = VideosSearch(text,limit=10)
#         result_list =[]
#         for i in video.result()['result']:
#             result_dict = {
#                 'input':text,
#                 'title':i['title'],
#                 'duration':i['duration'],
#                 'thumbnail':i['thumbnails'][0]['url'],
#                 'channel':i['channel']['name'],
#                 'link':i['link'],
#                 'views':i['viewCount']['short'],
#                 'published':i['publishedTime'],
#             }
#             desc = ''
#             if i['descriptionSnippet']:
#                 for j in i['descriptionSnippet']:
#                     desc += j['text']
#             result_dict['description'] = desc
#             result_list.append(result_dict)
#             context = {'form':form,'results':result_list}
#         return render(request,"dashboard/youtube.html",context)
#     else:
#         form = DashboardForm()
#     context = {'form':form}
#     return render(request,"dashboard/youtube.html",context)

@method_decorator(dec,name='dispatch')
class Todos(View):
    def get(self,request,*args,**kwargs):
        form = TodoForm()
        todo = Todo.objects.filter(user=request.user)
        if len(todo) == 0:
            todos_done = True
        else:
            todos_done = False
        context = {'todos':todo,'form':form,"todos_done":todos_done}
        return render(request,'dashboard/todo.html',context)
    
    def post(self,request,*args,**kwargs):
        us = request.user.username
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(user=request.user,title=request.POST['title'],is_finished=finished)
            todos.save()
            messages.success(request,f"Todo added from "+ us + "!!")
            return redirect('todo')
        else: 
            context = {'todos':todos,'form':form}
            return render(request,'dashboard/todo.html',context)
    
# def todo(request):
#     if request.method == "POST":
#         form = TodoForm(request.POST)
#         if form.is_valid():
#             try:
#                 finished = request.POST["is_finished"]
#                 if finished == 'on':
#                     finished = True
#                 else:
#                     finished = False
#             except:
#                 finished = False
#             todos = Todo(user=request.user,title=request.POST['title'],is_finished=finished)
#             todos.save()
#             messages.success(request,f"Todo added from {request.user.username}!!")
#     else:
#         form = TodoForm()
#     todo = Todo.objects.filter(user=request.user)
#     if len(todo) == 0:
#         todos_done = True
#     else:
#         todos_done = False
#     context = {'todos':todo,'form':form,"todos_done":todos_done}
#     return render(request,'dashboard/todo.html',context)

dec
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

dec
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

class Book(View):
    def get(self,request,*args,**kwargs):
        form = DashboardForm()
        return render(request,"dashboard/books.html",{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list =[]
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
            context = {'form':form,'results':result_list}
        return render(request,"dashboard/books.html",context)
    
# def books(request):
#     if request.method == "POST":
#         form = DashboardForm(request.POST)
#         text = request.POST['text']
#         url = "https://www.googleapis.com/books/v1/volumes?q="+text
#         r = requests.get(url)
#         answer = r.json()
#         result_list =[]
#         for i in range(10):
#             result_dict = {
#                 'title':answer['items'][i]['volumeInfo']['title'],
#                 'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
#                 'description':answer['items'][i]['volumeInfo'].get('description'),
#                 'count':answer['items'][i]['volumeInfo'].get('pageCount'),
#                 'categories':answer['items'][i]['volumeInfo'].get('categories'),
#                 'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
#                 'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
#                 'preview':answer['items'][i]['volumeInfo'].get('previewLink')
#             }
#             result_list.append(result_dict)
#             context = {'form':form,'results':result_list}
#         return render(request,"dashboard/books.html",context)
#     else:
#         form = DashboardForm()
#     context = {'form':form}
#     return render(request,"dashboard/books.html",context)

class Dictionary(View):
    def get(self,request,*args,**kwargs):
        form = DashboardForm()
        return render(request,"dashboard/books.html",{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context = {
                'form':form,
                'input':''
            }
        return render(request,"dashboard/dictionary.html",context)

# def dictionary(request):
#     if request.method == "POST":
#         form = DashboardForm(request.POST)
#         text = request.POST['text']
#         url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
#         r = requests.get(url)
#         answer = r.json()
#         try:
#             phonetics = answer[0]['phonetics'][0]['text']
#             audio = answer[0]['phonetics'][0]['audio']
#             definition = answer[0]['meanings'][0]['definitions'][0]['definition']
#             example = answer[0]['meanings'][0]['definitions'][0]['example']
#             synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
#             context = {
#                 'form':form,
#                 'input':text,
#                 'phonetics':phonetics,
#                 'audio':audio,
#                 'definition':definition,
#                 'example':example,
#                 'synonyms':synonyms
#             }
#         except:
#             context = {
#                 'form':form,
#                 'input':''
#             }
#         return render(request,"dashboard/dictionary.html",context)
#     else:
#         form = DashboardForm()
#         context = {'form':form}
#     return render(request,'dashboard/dictionary.html',context)

class Wiki(View):
    def get(self,request,*args,**kwargs):
        form = DashboardForm()
        return render(request,"dashboard/wiki.html",{'form':form})
    
    def post(self,request,*args,**kwargs):
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,"dashboard/wiki.html",context)

# def wiki(request):
#     if request.method == "POST":
#         text = request.POST['text']
#         form = DashboardForm(request.POST)
#         search = wikipedia.page(text)
#         context = {
#             'form':form,
#             'title':search.title,
#             'link':search.url,
#             'details':search.summary
#         }
#         return render(request,"dashboard/wiki.html",context)
#     else:
#         form = DashboardForm()
#         context = {'form':form}
#     return render(request,"dashboard/wiki.html",context)

class Conversion(View):
    def get(self,request,*args,**kwargs):
        form = ConversionForm()
        context = {
            'form':form,
            'input':False
        }
        return render(request,"dashboard/conversion.html",context)
    
    def post(self,request,*args,**kwargs):
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot' :
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard' :
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }

        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram' :
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound' :
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
        return render(request,"dashboard/conversion.html",context)

# def conversion(request):
#     if request.method == "POST":
#         form = ConversionForm(request.POST)
#         if request.POST['measurement'] == 'length':
#             measurement_form = ConversionLengthForm()
#             context = {
#                 'form':form,
#                 'm_form':measurement_form,
#                 'input':True
#             }
#             if 'input' in request.POST:
#                 first = request.POST['measure1']
#                 second = request.POST['measure2']
#                 input = request.POST['input']
#                 answer = ''
#                 if input and int(input) >= 0:
#                     if first == 'yard' and second == 'foot' :
#                         answer = f'{input} yard = {int(input)*3} foot'
#                     if first == 'foot' and second == 'yard' :
#                         answer = f'{input} foot = {int(input)/3} yard'
#                 context = {
#                     'form':form,
#                     'm_form':measurement_form,
#                     'input':True,
#                     'answer':answer
#                 }
#         if request.POST['measurement'] == 'mass':
#             measurement_form = ConversionMassForm()
#             context = {
#                 'form':form,
#                 'm_form':measurement_form,
#                 'input':True
#             }
#             if 'input' in request.POST:
#                 first = request.POST['measure1']
#                 second = request.POST['measure2']
#                 input = request.POST['input']
#                 answer = ''
#                 if input and int(input) >= 0:
#                     if first == 'pound' and second == 'kilogram' :
#                         answer = f'{input} pound = {int(input)*0.453592} kilogram'
#                     if first == 'kilogram' and second == 'pound' :
#                         answer = f'{input} kilogram = {int(input)*2.20462} pound'
#                 context = {
#                     'form':form,
#                     'm_form':measurement_form,
#                     'input':True,
#                     'answer':answer
#                 }
#     else:
#         form = ConversionForm()
#         context = {
#             'form':form,
#             'input':False
#         }
#     return render(request,"dashboard/conversion.html",context)

class Register(View):
    def get(self,request,*args,**kwargs):
        form = UserRegistractionForm()
        context = {'form':form}
        return render(request,"dashboard/conversion.html",context)
    
    def post(self,request,*args,**kwargs):
        form = UserRegistractionForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Account Created for {username}!!")
            return redirect('login')

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistractionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             messages.success(request,f"Account Created for {username}!!")
#             return redirect('login)
#     else:
#         form = UserRegistractionForm()
#     context = {'form':form}
#     return render(request,"dashboard/register.html",context)

dec  
def Profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {'homeworks':homeworks,'todos':todos,'homework_done':homework_done,'todos_done':todos_done}
    return render(request,"dashboard/profile.html",context)