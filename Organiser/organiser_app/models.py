# coding=utf-8
from datetime import datetime
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager
from django.core.urlresolvers import reverse_lazy
from django.db import models
from djangotoolbox.fields import EmbeddedModelField, RawField


class User(AbstractUser):
    # objects = UserManager()
    def __unicode__(self):
        return self.get_full_name() + " [" + self.email + "]"


class Note(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    edit_date = models.DateTimeField(verbose_name="Data edycji", null=True, blank=True, auto_now=True)
    title = models.CharField(verbose_name="Tytuł", max_length=100)
    content = models.TextField(verbose_name="Treść", default=None)
    author = models.ForeignKey(User)

    def get_absolute_url(self):
        return reverse_lazy('note', args=(self.id,))

    def __str__(self):
        return self.author.get_full_name() + " - " + self.title


class Contact(models.Model):
    first_name = models.CharField(verbose_name="Imię", max_length=100)
    last_name = models.CharField(verbose_name="Nazwisko", max_length=100)
    birthdate = models.DateField(verbose_name="Data urodzenia", null=True, blank=True)
    phone_number = models.CharField(max_length=12, verbose_name="Numer telefonu", null=True, blank=True)
    location = models.CharField(max_length=300, verbose_name="Miejsce zamieszkania", null=True, blank=True)
    additional_info = models.TextField(max_length=500, verbose_name="Dodatkowe informacje", null=True, blank=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def first_letter(self):
        return self.last_name and self.last_name[0] or ''

    def get_absolute_url(self):
        return reverse_lazy('contact', args=(self.id,))


class CalendarEvent(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tytuł")
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name="Opis")
    start_date = models.DateTimeField(verbose_name="Data rozpoczęcia")
    end_date = models.DateTimeField(default=None, null=True, blank=True, verbose_name="Data zakończenia")
    location = models.CharField(max_length=300, verbose_name="Miejsce wydarzenia", default=None, null=True, blank=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.author.get_full_name() + " - " + self.title + " [" + str(self.start_date)+ "]"

    def isActive(self):
        if self.end_date:
            return self.start_date.date() <= datetime.today().date() <= self.end_date
        else:
            if self.start_date.date() == datetime.today().date():
                return True
            else:
                return False

    def get_absolute_url(self):
        return reverse_lazy('event', args=(self.id,))
