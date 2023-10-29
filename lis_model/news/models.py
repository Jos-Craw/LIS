from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from .utilities import send_activation_notification
import os
from django.core.validators import MaxValueValidator , MinValueValidator


class AdvUser(AbstractUser):
    fac = (
        ('bio','Биологический факультет'),
        ('geo','Геолого-географический факультет'),
        ('ist','Факультет истории и межкультурных коммуникаций'),
        ('in','Факультет иностранных языков'),
        ('mat','Факультет математитики и ТП'),
        ('psi','Факультет психологии и педагогики'),
        ('fiz','Факультет физики и ИТ'),
        ('ffk','Факультет физической культуры'),
        ('fil','Филологический факультет'),
        ('eko','Экономический факультет'),
        ('yr','Юридичесий факультет'),
        )
        

    is_activated = models.BooleanField(default=True, db_index=True,verbose_name='Прошел активацию')
    avatar = models.ImageField(null=True, blank=True, upload_to="image/profile/",verbose_name='Аватарка')
    phone_num = models.CharField(unique = True, null = True, blank = False, max_length=13,verbose_name='Номер телефона')
    faculty = models.CharField(null = True, blank =False,choices=fac,max_length=50,verbose_name='Факультет')
    group = models.CharField(null = True, blank = False,max_length=10,verbose_name='Группа')



    class Meta(AbstractUser.Meta):
        pass

class Consult(models.Model):
    date = (
         ('9:00','9:00'),
         ('10:00','10:00'),
         ('11:00','11:00'),
         ('12:00','12:00'),
         ('13:00','13:00'),
         ('14:00','14:00'),
         ('15:00','15:00'),
        )
    eventdate = models.DateField(db_index=True,null=True,blank=False,verbose_name='Дата')
    eventtime = models.CharField(choices=date,blank=False,max_length=10,verbose_name='Время')
    zan = models.BooleanField(default=False, db_index=True,verbose_name='Занятость')

    class Meta:
        verbose_name_plural = 'Консультации'
        verbose_name = 'Консультация'
        ordering = ['eventdate']

class Post(models.Model):
    tag = (
        ('cult','Культурно-досуговая деятельность'),
        ('sport','Спортивная деятельность'),
        ('mass','Массовые мероприятия и выставки'),
        ('trud','Трудовая и волонтерская деятельность'),
        )

    name = models.CharField(null=True, blank=False,max_length=100,verbose_name='Заголовок')
    content = models.TextField(null=True, blank=False,verbose_name='Контент')
    image = models.ImageField(upload_to='image/%Y/%m/%d/', blank=True, null=True,verbose_name='Изображение')
    file = models.FileField(upload_to='files/%Y/%m/%d/', blank=True, null=True,verbose_name='Приклепленные файлы')
    video = models.FileField(upload_to='video/%Y/%m/%d/', blank=True, null=True,verbose_name='Видео')
    audio = models.FileField(upload_to='audio/%Y/%m/%d/', blank=True, null=True,verbose_name='Аудио')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, null=True,verbose_name='Автор')
    pubdate = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')
    eventtime = models.TimeField(db_index=True,null=True,blank=False,verbose_name='Время')
    eventdate = models.DateField(db_index=True,null=True,blank=False,verbose_name='Дата')
    stoim = models.CharField(null = True, blank = False, max_length=10,verbose_name='Стоимость')
    mesta = models.IntegerField(null = True, blank = False,default=2,validators=[MinValueValidator(0)],verbose_name='Количество мест всего') 
    mesta_now = models.IntegerField(null = True, blank = False,verbose_name='Количество мест сейчас')
    mest = models.IntegerField(null = True) 
    tags = models.CharField( blank = False,choices=tag, max_length=50,verbose_name='Тэг',null=True)
    zapis = models.ManyToManyField(AdvUser, related_name='Записаные',blank=True, verbose_name='Записаные', through='PostType', through_fields=('post','user'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'События'
        verbose_name = 'Событие'
        ordering = ['eventdate']

    def filename(self):
        return os.path.basename(self.file.name)

class PostType(models.Model):
    user = models.ForeignKey(AdvUser,on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True)
    zap_type = models.BooleanField(default=False, db_index=True,verbose_name='Групповая запись')
    colvo= models.IntegerField(null = True,verbose_name='Количество занятых мест')

    class Meta:
        verbose_name_plural = 'Записи мероприятий'
        verbose_name = 'Запись мероприяти'

class Event(models.Model):
    eventtime = models.TimeField(db_index=True,null=True,blank=False,verbose_name='Время')
    eventdate = models.DateField(db_index=True,null=True,blank=False,verbose_name='Дата')
    zan = models.BooleanField(default=False, db_index=True,verbose_name='Занято')
    zapisi = models.ManyToManyField(AdvUser, related_name='Записи',blank=True,verbose_name='Записаные')
    group = models.BooleanField(default=False, db_index=True,verbose_name='Групповая')

    def __str__(self):
        return f'{self.eventtime} {self.eventdate}'

    class Meta:
        verbose_name_plural = 'Время и дата выставки'
        verbose_name = 'Время и дата выставки'



class Vist(models.Model):
    name = models.CharField(null=True, blank=False,max_length=100,verbose_name='Название')
    content = models.TextField(null=True, blank=False,verbose_name='Контент')
    image = models.ImageField(upload_to='image/%Y/%m/%d/', blank=True, null=True,verbose_name='Изображение')
    file = models.FileField(upload_to='files/%Y/%m/%d/', blank=True, null=True,verbose_name='Приклепленные файлы')
    video = models.FileField(upload_to='video/%Y/%m/%d/', blank=True, null=True,verbose_name='Видео')
    audio = models.FileField(upload_to='audio/%Y/%m/%d/', blank=True, null=True,verbose_name='Аудио')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, null=True,verbose_name='Автор')
    pubdate = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')
    stoim = models.CharField(null = True, blank = False, max_length=10,verbose_name='Стоимость')
    event = models.ManyToManyField(Event,related_name='Даты',blank=True,verbose_name='Время и дата')
    final_date = models.DateField(db_index=True,null=True,blank=False,verbose_name='Конец выставки')
    start_date = models.DateField(db_index=True,null=True,blank=False,verbose_name='Начало выставки')

    class Meta:
        verbose_name_plural = 'Выставки'
        verbose_name = 'Выставка'
        ordering = ['pubdate']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True ,null=True,verbose_name='Мероприятие')
    vist = models.ForeignKey(Vist, on_delete=models.CASCADE, blank=True , null=True,verbose_name='Выставка')
    content = models.TextField(null=True, blank=False,verbose_name='Контент')
    author = models.CharField(max_length=30,verbose_name='Автор')
    pubdate = models.DateTimeField(auto_now_add=True, db_index=True,verbose_name='Дата публикации')
    moderation = models.BooleanField(default=False,verbose_name='Модерация')

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        ordering = ['-pubdate']


class Section(models.Model):
    name = models.CharField(max_length=30,verbose_name='Название')
    otobr = models.BooleanField(default=False, db_index=True,verbose_name='Отображение')

    class Meta:
        verbose_name_plural = 'Секции'
        verbose_name = 'Секция'

class Tvor(models.Model):
    name = models.CharField(max_length=30,verbose_name='Название')
    otobr = models.BooleanField(default=False, db_index=True,verbose_name='Отображение')

    class Meta:
        verbose_name_plural = 'Творческие направления'
        verbose_name = 'Творческое направление'

class Trud(models.Model):
    name = models.CharField(max_length=30,verbose_name='Название')
    otobr = models.BooleanField(default=False, db_index=True,verbose_name='Отображение')

    class Meta:
        verbose_name_plural = 'Трудовые направления'
        verbose_name = 'Трудовое направление'

class Volant(models.Model):
    name = models.CharField(max_length=30,verbose_name='Название')
    otobr = models.BooleanField(default=False, db_index=True,verbose_name='Отображение')

    class Meta:
        verbose_name_plural = 'Волонтерские направления'
        verbose_name = 'Волонтерское направление'

user_registrated = Signal(['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)
