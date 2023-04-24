from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
import requests, webbrowser
from bs4 import BeautifulSoup
import speech_recognition as sr
from django.contrib import messages

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'index.html')

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'studentclick.html')

#for showing signup/login button for teacher
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'adminclick.html')



def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'adminsignup.html',{'form':form})



def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'studentsignup.html',context=mydict)




def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'adminafterlogin.html')
    else:
        return render(request,'studentafterlogin.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    # now it is empty book form for sending to html
    form = forms.BookForm()
    if request.method == 'POST':
        # now this form have data from html
        form = forms.BookForm(request.POST)
        if form.is_valid():
            book_info = form.save(commit=False)
            book_name = book_info.book_name
            book_author = book_info.book_author
            res1 = "Education"
            google_link = 0
            final_elements_list = -1

            google_search = requests.get("https://www.google.com/search?tbm=bks&q=" + book_name + book_author)

            soup = BeautifulSoup(google_search.text, 'html.parser')
            search_results = soup.select('.kCrYT a')

            for link in search_results[:1]:
                google_link = link.get('href')
                #webbrowser.open(google_link)

            if google_link != 0:
                second_search = requests.get(google_link)
                soup1 = BeautifulSoup(second_search.text, 'html.parser')

                forId = soup1.find('link', rel="canonical")
                # print(forId)
                import re
                allStrings = re.findall(r'"(.*?)"', str(forId))
                # print(allStrings[0])

                final_link = requests.get(allStrings[0])
                soup2 = BeautifulSoup(final_link.text, 'html.parser')

                table_result = soup2.find('table', id="metadata_content_table")

                if table_result:
                    rows = table_result.find_all('tr')
                    fullstring = ""
                    elements = ""

                    for row in rows:

                        if row.find('td', class_="metadata_label"):
                            columns = row.find('td', class_="metadata_label").text
                            # print(columns)
                            fullstring += columns
                            # print(fullstring)
                        if fullstring.find("Subjects") != -1:
                            if columns.find("Subjects") != -1:
                                list = row.find_all('span', itemprop="title")
                                # print(list)
                                for x in list:
                                    sub_element = x.text
                                    # print(sub_element)
                                    elements = elements + sub_element + ">"
                                final_elements_list = elements.rstrip(">")
                                break
                    # print("Education")
                    res1 = "Education"
                else:
                    # print("Education")
                    res1 = "Education"
            else:
                res1 = "Education"

            if final_elements_list != -1:
                # print(res1 + ">" + final_elements_list)
                #res = res1 + ">" + final_elements_list
                if final_elements_list.endswith(">General"):
                    res = final_elements_list[:-(len(">General"))]
                else:
                    res = final_elements_list
                #print(res)
            else:
                res = res1
                #print(res)
            book_info.category = res
            book_info.save()
            return render(request, 'bookadded.html')
    return render(request, 'addbook.html', {'form': form})

def search_view(request):
    issuedbooks = models.IssuedBook.objects.all()
    query = request.GET['query']
    print(query)
    if len(query) == 0:
        r = sr.Recognizer()
        # r.dynamic_energy_threshold = False
        r.energy_threshold = 500
        #print(r.energy_threshold)
        print('speak:')
        with sr.Microphone() as source:
            audio = r.listen(source, phrase_time_limit = 3)
            print('listening...')
            try:
                print('recognizing...')
                query = r.recognize_google(audio, language='eng-in')
                print(query)
            except:
                print('could not recognize')

    booksName = models.Book.objects.filter(book_name__icontains=query)
    booksAuthor = models.Book.objects.filter(book_author__icontains=query)
    booksCategory = models.Book.objects.filter(category__icontains=query)
    books = booksName.union(booksAuthor, booksCategory)
    li = []
    i = 0
    count=0
    #params = {'allBooks': allBooks}
    for b in books:
        for ib in issuedbooks:
            if str(b.isbn) == ib.isbn:
                count+=1
        #leftCopies = books[i].no_of_copies - count
        t = (books[i].book_name, books[i].book_author, books[i].isbn, books[i].category, books[i].no_of_copies, count)
        i = i + 1
        li.append(t)
    if is_admin(request.user):
        return render(request, 'search.html', {'li':li, 'query':query})
    else:
        return render(request, 'studentSearch.html', {'li': li, 'query': query})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books=models.Book.objects.all()
    issuedbooks = models.IssuedBook.objects.all()
    li = []
    i = 0


    for b in books:
        count = 0
        for ib in issuedbooks:
            if str(b.isbn) == ib.isbn:
                count+=1
        #leftCopies = books[i].no_of_copies - count
        t = (books[i].book_name, books[i].book_author, books[i].isbn, books[i].category, books[i].no_of_copies, count)
        i = i + 1
        li.append(t)

    return render(request,'viewbook.html',{'li':li})


def student_viewbook_view(request):
    books = models.Book.objects.all()
    issuedbooks = models.IssuedBook.objects.all()
    li = []
    i = 0
    count = 0

    for b in books:
        for ib in issuedbooks:
            if str(b.isbn) == ib.isbn:
                count += 1
        #leftCopies = books[i].no_of_copies - count
        t = (books[i].book_name, books[i].book_author, books[i].isbn, books[i].category, books[i].no_of_copies, count)
        i = i + 1
        li.append(t)

    return render(request,'studentviewbook.html',{'li':li})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj=models.IssuedBook()
            obj.enrollment=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return render(request,'bookissued.html')
    return render(request,'issuebook.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].book_name,books[i].book_author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request,'viewissuedbook.html',{'li':li})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'viewstudent.html',{'students':students})

@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,student[0].branch,book.book_name,book.book_author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'viewissuedbookbystudent.html',{'li1':li1,'li2':li2})

def destroy(request, id):
    if request.method == 'POST':
        issuedbook = models.IssuedBook.objects.get(id=id)
        issuedbook.delete()
        return HttpResponseRedirect("/")