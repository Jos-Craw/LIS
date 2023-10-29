from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, AdvUser, Comment, Consult,Section, Tvor ,Trud, Volant, Vist, Event, PostType
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ChangeUserInfoForm, RegisterUserForm, CommentForm, Subscribe ,Index,NewConsult,zapis_consult, PostForm,UnSubscribeg,Subscribeg,TvorForm,VistForm,Subscribegv
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.signing import BadSignature
from .utilities import signer
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta, date
from django.core.validators import MaxValueValidator , MinValueValidator
from django.db.models import Q

def index(request):
	weekd=datetime.today().isocalendar()[1] 
	posts = Post.objects.filter(eventdate__week=weekd)
	if request.method == 'POST':
		form = Index(request.POST)
		if form.is_valid():
			nach = form.cleaned_data['Начало']
			con = form.cleaned_data['Конец']
			posts = Post.objects.filter(eventdate__range=(nach,con))
	else:
		form = Index()
	return render(request, 'news/index.html', {'form': form,'posts': posts})

@login_required
def profile(request):
	posttypes = PostType.objects.filter(user=request.user.id)
	posts = Post.objects.filter(zapis=request.user.id)
	vists = Vist.objects.all()
	events = Event.objects.filter(zapisi=request.user.id)
	your_posts = Post.objects.filter(author=request.user.pk)
	a = date.today()
	b = a + timedelta(days=1)
	return render(request, 'news/profile.html', {'vists': vists,'posts': posts,'your_posts':your_posts,'a':a,'b':b,'events':events,'posttypes':posttypes})

@login_required
def create(request):
    if request.method == 'POST' or request.FILES:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
        	post = form.save()
        	post.mesta_now = post.mesta
        	post.mest = post.mesta-post.mesta_now
        	post.save()
        	return redirect('news:index')
    else:
        form = PostForm(initial={'author': request.user.pk})
    context = {'form': form}
    return render(request, 'news/create.html', context)

@login_required
def create_v(request):
	if request.method == 'POST' or request.FILES:
		form = VistForm(request.POST, request.FILES)
		if form.is_valid():
			vist = form.save()
		return redirect('news:index')
	else:
		form = VistForm(initial={'author': request.user.pk})
	context = {'form': form}
	return render(request, 'news/create.html', context)

@login_required
def deletepost(request, pk):
	useremail=[]
	users = AdvUser.objects.all()
	messageSent = False
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		for d in post.zapis.all():
  			print(d.email)
  			useremail.append(d.email)
		subject = 'ОТМЕНЯ МЕРОПРИЯТИЯ' 
		message = 'Отменя ' + post.content + ' ' + str(post.eventdate)+ ' ' +str(post.eventtime)
		send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, useremail)
		messageSent = True
		post.delete()
		return redirect('news:index')
	else:
		context = {'post': post,'messageSent': messageSent}
	return render(request, 'news/deletepost.html', context)

@login_required
def detail(request, pk):
	posttypes = PostType.objects.filter(user=request.user.id)
	your_zapisi = Post.objects.filter(zapis=request.user.id)
	messageSent = False
	post = get_object_or_404(Post, pk=pk)
	comments = Comment.objects.filter(post=pk,moderation=True)
	initial = {'post': post.pk}
	initial['author'] = request.user.first_name + ' ' + request.user.last_name
	a = date.today()
	b = a + timedelta(days=1)
	form_class = CommentForm
	form = form_class(initial=initial)
	if request.method == 'POST' or request.FILES:
		form = CommentForm(request.POST)
		c_form = form_class(request.POST, request.FILES)
		if c_form.is_valid():
			c_form.save()
		else:
			form = c_form
		if form.is_valid():
			cd = form.cleaned_data
			subject = 'НОВЫЙ КОММЕНТАРИЙ'
			message = 'Зайдите на сайт для одобрения комментария: '+cd['content'] + ' от ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['novogencev.pavel@gmail.com']) #hodanovich@gsu.by, osnach@gsu.by
			messageSent = True
	return render(request, 'news/detail.html', {'post': post, 'comments': comments, 'form': form,'messageSent': messageSent,'your_zapisi':your_zapisi,'a':a,'b':b,'posttypes':posttypes})

@login_required
def detail_v(request, pk):
	messageSent = False
	your_vist = Event.objects.filter(zapisi=request.user.id)
	vist = get_object_or_404(Vist, pk=pk)
	comments = Comment.objects.filter(vist=pk,moderation=True)
	initial = {'vist': vist.pk}
	initial['author'] = request.user.first_name + ' ' + request.user.last_name
	a = date.today()
	b = a + timedelta(days=1)
	form_class = CommentForm
	form = form_class(initial=initial)
	if request.method == 'POST' or request.FILES:
		form = CommentForm(request.POST)
		c_form = form_class(request.POST, request.FILES)
		if c_form.is_valid():
			c_form.save()
		else:
			form = c_form
		if form.is_valid():
			cd = form.cleaned_data
			subject = 'НОВЫЙ КОММЕНТАРИЙ'
			message = 'Зайдите на сайт для одобрения комментария: '+cd['content'] + ' от ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['novogencev.pavel@gmail.com']) #hodanovich@gsu.by, osnach@gsu.by
			messageSent = True
	return render(request, 'news/detail_v.html', {'vist': vist, 'comments': comments, 'form': form,'messageSent': messageSent,'a':a,'b':b,'your_vist':your_vist})



def cult(request):
    weekd=datetime.today().isocalendar()[1] 
    posts = Post.objects.filter(eventdate__week=weekd)
    your_zapisi = Post.objects.filter(zapis=request.user.id)
    tvors = Tvor.objects.filter(otobr=True)
    if request.method == 'POST':
    	form = Index(request.POST)
    	if form.is_valid():
    		nach = form.cleaned_data['Начало']
    		con = form.cleaned_data['Конец']
    		posts = Post.objects.filter(eventdate__range=(nach,con))
    else:
    	form = Index() 
    return render(request, 'news/cult.html', {'posts': posts,'your_zapisi':your_zapisi,'tvors':tvors,'form':form})


def tvor(request,pk):
	naprav = get_object_or_404(Tvor, pk=pk)
	messageSent = False
	if request.method == 'POST':
		form = TvorForm(request.POST)
		if form.is_valid(): 
			cd = form.cleaned_data
			initial = {'naprav': naprav.pk} 
			subject = 'ЗАПИСЬ на творческое направление ' + cd['Роль']
			message = 'ЗАПИСЬ на '+ naprav.name +' '+cd['Роль'] +' ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email+' ' +request.user.group 
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['novogencev.pavel@gmail.com']) #VELIKY@gsu.by
			messageSent = True
	else:
		form = TvorForm
	return render(request, 'news/tvor.html',{'form':form,'messageSent': messageSent,'naprav':naprav})


def sport(request):
	sections = Section.objects.filter(otobr=True)
	weekd=datetime.today().isocalendar()[1] 
	posts = Post.objects.filter(eventdate__week=weekd)
	your_zapisi = Post.objects.filter(zapis=request.user.id)
	if request.method == 'POST':
		form = Index(request.POST)
		if form.is_valid():
			nach = form.cleaned_data['Начало']
			con = form.cleaned_data['Конец']
			posts = Post.objects.filter(eventdate__range=(nach,con))
	else:
		form = Index()
	return render(request, 'news/sport.html', {'posts': posts,'your_zapisi':your_zapisi,'sections':sections,'form':form})


def mass(request):
	weekd=datetime.today().isocalendar()[1] 
	posts = Post.objects.filter(eventdate__week=weekd)
	vists = Vist.objects.filter(start_date__week=weekd,final_date__week=weekd)
	your_zapisi = Post.objects.filter(zapis=request.user.id)
	if request.method == 'POST':
		form = Index(request.POST)
		if form.is_valid():
			nach = form.cleaned_data['Начало']
			con = form.cleaned_data['Конец']
			posts = Post.objects.filter(eventdate__range=(nach,con))
			vists = Vist.objects.filter(
				Q(start_date__range=(nach,con))|
				Q( final_date__range=(nach,con)))
	else:
		form = Index()
	return render(request, 'news/mass.html', {'posts': posts,'your_zapisi':your_zapisi,'vists':vists,'form':form})

def trud(request):
    weekd=datetime.today().isocalendar()[1] 
    posts = Post.objects.filter(eventdate__week=weekd)
    truds = Trud.objects.filter(otobr=True)
    volonts = Volant.objects.filter(otobr=True)
    your_zapisi = Post.objects.filter(zapis=request.user.id)
    if request.method == 'POST':
    	form = Index(request.POST)
    	if form.is_valid():
    		nach = form.cleaned_data['Начало']
    		con = form.cleaned_data['Конец']
    		posts = Post.objects.filter(eventdate__range=(nach,con))
    else:
    	form = Index()
    return render(request, 'news/trud.html', {'posts': posts,'your_zapisi':your_zapisi,'truds':truds,'volonts': volonts,'form':form})

def trud_naprav(request,pk):
	trud = get_object_or_404(Trud, pk=pk)
	messageSent = False
	if request.method == 'POST':
		form = zapis_consult(request.POST)
		if form.is_valid(): 
			initial = {'trud': trud.pk}
			subject = 'ЗАПИСЬ на трудовое направление '  
			message = 'ЗАПИСЬ на '+ trud.name +' ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email+' ' +request.user.group 
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['novogencev.pavel@gmail.com']) #FEDORENKO@gsu.by
			messageSent = True
	else:
		form = zapis_consult
	return render(request, 'news/tvor.html',{'messageSent': messageSent})


def volon_naprav(request,pk):
	volont = get_object_or_404(Volant, pk=pk) 
	messageSent = False
	if request.method == 'POST':
		form = zapis_consult(request.POST)
		if form.is_valid():
			if volont.name == 'Профсоюз':
				email = 'novogencev.pavel@gmail.com' #AZYAVCHIKOV@gsu.by
			else:
				email = 'novogencev.pavel@gmail.com' #FEDORENKO@gsu.by
			initial = {'volont': volont.pk}
			subject = 'ЗАПИСЬ на волонтерское направление '  
			message = 'ЗАПИСЬ на '+ volont.name +' ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email+' ' +request.user.group 
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
			messageSent = True
	else:
		form = zapis_consult
	return render(request, 'news/tvor.html',{'messageSent': messageSent})	



def otz(request):
	comments = Comment.objects.filter(moderation=True)
	return render(request, 'news/otz.html', {'comments': comments})

def sec(request,pk):
	section = get_object_or_404(Section, pk=pk)
	messageSent = False
	if request.method == 'POST':
		form = zapis_consult(request.POST)
		if form.is_valid(): 
			initial = {'section': section.pk}
			subject = 'ЗАПИСЬ на секцию '  
			message = 'ЗАПИСЬ на '+ section.name +' ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email+' ' +request.user.group 
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['novogencev.pavel@gmail.com']) #KULESHOV@gsu.by
			messageSent = True
	else:
		form = zapis_consult
	return render(request, 'news/sec.html',{'messageSent': messageSent})


def consult(request):
	consults = Consult.objects.filter(zan=False)
	form_class = NewConsult
	form = form_class
	if request.method == 'POST':
		c_form = form_class(request.POST, request.FILES)
		if c_form.is_valid():
			c_form.save()
		else:
			form = c_form
	return render(request, 'news/consult.html', {'consults': consults, 'form': form})

def zap_consult(request, pk):
	consult = get_object_or_404(Consult, pk=pk)
	messageSent = False
	if request.method == 'POST':
		form = zapis_consult(request.POST)
		if form.is_valid(): 
			initial = {'consult': consult.pk}
			subject = 'ЗАПИСЬ на консультацию '  
			message = 'ЗАПИСЬ на '+ str(consult.eventdate) +' '+ consult.eventtime + ' : ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email+ ' ' +request.user.group
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['novogencev.pavel@gmail.com']) #TROSHEVA@gsu.by
			messageSent = True
			consult.zan = True
			consult.save()
	else:
		form = zapis_consult
	return render(request,'news/zapis_consult.html',{'consult':consult,'form': form,'messageSent': messageSent})



class POSTLoginView(LoginView):
    template_name = 'news/login.html'


class POSTLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'news/logout.html'


class POSTChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'news/password_change.html'
    success_url = reverse_lazy('news:profile')
    success_message = 'Password changed'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'news/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('news:profile')
    success_message = 'Info changed'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'news/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('news:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'news/register_done.html'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'news/delete_user.html'
    success_url = reverse_lazy('news:index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User deleted')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'news/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'news/user_is_activated.html'
    else:
        template = 'news/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

def zapis(request, pk):
	post = get_object_or_404(Post, pk=pk)
	messageSent = False
	if request.method == 'POST':
		form = Subscribe(request.POST)
		if form.is_valid():
			if post.tags == 'cult':
				email = 'novogencev.pavel@gmail.com' #VELIKY@gsu.by
			elif post.tags == 'sport':
				email = 'novogencev.pavel@gmail.com' #KULESHOV@gsu.by
			elif post.tags == 'mass':
				email = 'novogencev.pavel@gmail.com' #osnach@gsu.by,bardashevich@gsu.by
			elif post.tags == 'trud':
				email = 'novogencev.pavel@gmail.com' #FEDORENKO@gsu.by
			cd = form.cleaned_data
			initial = {'post': post.pk}
			subject = post.name + ' ЗАПИСЬ ' 
			message = 'ЛИЧНАЯ ЗАПИСЬ: от ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email+' ' +request.user.group
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
			messageSent = True
			post.zapis.add(request.user.id)
			post.mesta_now = post.mesta_now -1
			post.save()
	else:
		form = Subscribe()
	return render(request, 'news/zapis.html', {'form': form,'messageSent': messageSent,'post':post})

def zapisg(request, pk):
	post = get_object_or_404(Post, pk=pk)
	messageSent = False
	if request.method == 'POST':
		form = Subscribeg(request.POST)
		if form.is_valid(): 
			if post.tags == 'cult':
				email = 'novogencev.pavel@gmail.com' #VELIKY@gsu.by
			elif post.tags == 'sport':
				email = 'novogencev.pavel@gmail.com' #KULESHOV@gsu.by
			elif post.tags == 'mass':
				email = 'novogencev.pavel@gmail.com' #osnach@gsu.by,bardashevich@gsu.by
			elif post.tags == 'trud':
				email = 'novogencev.pavel@gmail.com' #FEDORENKO@gsu.by
			cd = form.cleaned_data
			initial = {'post': post.pk}
			subject = post.name + ' ЗАПИСЬ ' 
			message = 'ГРУППОВАЯ ЗАПИСЬ: '+cd['message'] + ' от ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
			messageSent = True
			post.zapis.add(request.user.id)
			posttypes = PostType.objects.filter(user=request.user, post=post)
			posttype = get_object_or_404(PostType,pk=posttypes[0].id)
			posttype.zap_type = True
			posttype.colvo = cd['colvo']
			post.mesta_now = post.mesta_now - cd['colvo']
			post.save()
			posttype.save()
	else:
		form = Subscribeg()
	return render(request, 'news/zapisg.html', {'form': form,'messageSent': messageSent,'post':post})

def otpis(request, pk):
	post = get_object_or_404(Post, pk=pk)
	messageSent = False
	if request.method == 'POST':
		form = Subscribe(request.POST)
		if form.is_valid():
			if post.tags == 'cult':
				email = 'novogencev.pavel@gmail.com' #VELIKY@gsu.by
			elif post.tags == 'sport':
				email = 'novogencev.pavel@gmail.com' #KULESHOV@gsu.by
			elif post.tags == 'mass':
				email = 'novogencev.pavel@gmail.com' #osnach@gsu.by,bardashevich@gsu.by
			elif post.tags == 'trud':
				email = 'novogencev.pavel@gmail.com' #FEDORENKO@gsu.by
			cd = form.cleaned_data
			initial = {'post': post.pk}
			subject = post.name + ' ОТПИСЬ ' 
			message = 'ЛИЧНАЯ ОТПИСЬ: от ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num + ' ' + request.user.email+ ' ' +request.user.group
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
			messageSent = True
			post.zapis.remove(request.user.id)
			post.mesta_now = post.mesta_now +1
			post.save()
	else:
		form = Subscribe()
	return render(request, 'news/otpis.html', {'form': form,'messageSent': messageSent,'post':post})

def otpisg(request, pk):
	post = get_object_or_404(Post, pk=pk)
	messageSent = False
	post.mest = post.mesta-post.mesta_now
	post.save()
	posttypes = PostType.objects.filter(user=request.user, post=post)
	posttype = get_object_or_404(PostType,pk=posttypes[0].id)
	if request.method == 'POST':
		form = UnSubscribeg(request.POST)
		if form.is_valid():
			if post.tags == 'cult':
				email = 'novogencev.pavel@gmail.com' #VELIKY@gsu.by
			elif post.tags == 'sport':
				email = 'novogencev.pavel@gmail.com' #KULESHOV@gsu.by
			elif post.tags == 'mass':
				email = 'novogencev.pavel@gmail.com' #osnach@gsu.by,bardashevich@gsu.by
			elif post.tags == 'trud':
				email = 'novogencev.pavel@gmail.com' #FEDORENKO@gsu.by
			cd = form.cleaned_data
			initial = {'post': post.pk}
			subject = post.name + ' ОТПИСЬ ' 
			message = 'ГРУППОВАЯ ОТПИСЬ: '+cd['message'] + ' от ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
			messageSent = True
			if cd['colvo'] == posttype.colvo: 
				post.zapis.remove(request.user.id)
			elif cd['colvo'] < posttype.colvo :
				posttype.colvo = posttype.colvo - cd['colvo']
				posttype.save()
			post.mesta_now = post.mesta_now + cd['colvo']
			post.save()
	else:
		form = Subscribeg()
	return render(request, 'news/otpisg.html', {'form': form,'messageSent': messageSent,'post':post,'posttype':posttype})


def zapisv(request, pk1,pk2):
	vist = get_object_or_404(Vist, pk=pk1)
	event = get_object_or_404(Event, pk=pk2)
	messageSent = False
	if request.method == 'POST':
		form = Subscribe(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			initial = {'vist': vist.pk}
			initial = {'event': event.pk}
			subject = vist.name +' '+str(event.eventdate)+' '+str(event.eventtime) + ' ЗАПИСЬ ' 
			message = 'ЛИЧНАЯ ЗАПИСЬ: от ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email+' ' +request.user.group
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['novogencev.pavel@gmail.com']) #LVDUBROVSKAYA@gsu.by
			messageSent = True
			event.zan = True
			event.zapisi.add(request.user.id)
			event.group = False
			event.save()
			vist.save()
	else:
		form = Subscribe()
	return render(request, 'news/zapis.html', {'form': form,'messageSent': messageSent,'vist':vist,'event':event})


def zapisgv(request, pk1, pk2):
	vist = get_object_or_404(Vist, pk=pk1)
	event = get_object_or_404(Event, pk=pk2)
	messageSent = False
	if request.method == 'POST':
		form = Subscribegv(request.POST)
		if form.is_valid(): 
			cd = form.cleaned_data
			initial = {'vist': vist.pk}
			initial = {'event': event.pk}
			subject = vist.name +' '+str(event.eventdate)+' '+str(event.eventtime) + ' ЗАПИСЬ ' 
			message = 'ГРУППОВАЯ ЗАПИСЬ: '+cd['message'] + ' от ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['novogencev.pavel@gmail.com']) #LVDUBROVSKAYA@gsu.by
			messageSent = True
			event.zan = True
			event.zapisi.add(request.user.id)
			event.group = True
			event.save()
			vist.save()
	else:
		form = Subscribegv()
	return render(request, 'news/zapis.html', {'form': form,'messageSent': messageSent,'vist':vist,'event':event})

def otpisv(request, pk1,pk2):
	vist = get_object_or_404(Vist, pk=pk1)
	event = get_object_or_404(Event, pk=pk2)
	messageSent = False
	if request.method == 'POST':
		form = Subscribe(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			initial = {'vist': vist.pk}
			initial = {'event': event.pk}
			subject = vist.name +' '+str(event.eventdate)+' '+str(event.eventtime) + ' ОТПИСЬ ' 
			message = 'ЛИЧНАЯ ОТПИСЬ: от ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num + ' ' + request.user.email+ ' ' +request.user.group
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['novogencev.pavel@gmail.com']) #LVDUBROVSKAYA@gsu.by
			messageSent = True
			event.zan = False
			event.group = False
			event.zapisi.remove(request.user.id)
			event.save()
			vist.save()
	else:
		form = Subscribe()
	return render(request, 'news/otpis.html', {'form': form,'messageSent': messageSent,'vist':vist,'event':event})

def otpisgv(request, pk1,pk2):
	vist = get_object_or_404(Vist, pk=pk1)
	event = get_object_or_404(Event, pk=pk2)
	messageSent = False
	if request.method == 'POST':
		form = Subscribegv(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			initial = {'vist': vist.pk}
			initial = {'event': event.pk}
			subject = vist.name +' '+str(event.eventdate)+' '+str(event.eventtime) + ' ОТПИСЬ '  
			message = 'ГРУППОВАЯ ОТПИСЬ: '+cd['message'] + ' от ' + request.user.first_name + ' ' +request.user.last_name + ' ' +request.user.phone_num+ ' ' + request.user.email
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['novogencev.pavel@gmail.com']) #LVDUBROVSKAYA@gsu.by
			messageSent = True
			event.zan = False
			event.group = False
			event.zapisi.remove(request.user.id)
			event.save()
			vist.save()
	else:
		form = Subscribegv()
	return render(request, 'news/otpis.html', {'form': form,'messageSent': messageSent,'vist':vist,'event':event})