from django.db import models
from django.db.models import Q


class Department(models.Model):
    name = models.CharField(verbose_name="Navn", max_length=500)

    class Meta:
        ordering = ['name']

    @staticmethod
    def search(qs, pattern):
        return qs.filter(Q(name__icontains=pattern)).distinct()


class Person(models.Model):
    given_name = models.CharField(verbose_name="Fornavn", max_length=500)
    family_name = models.CharField(verbose_name="Etternavn", max_length=500)
    email = models.EmailField(verbose_name="email", max_length=500)
    mobile_phone = models.CharField(verbose_name="Mobilnummer", max_length=12, null=True, blank=True)
    work_phone = models.CharField(verbose_name="Jobbtelefon", max_length=12, null=True, blank=True)

    class Meta:
        ordering = ['family_name', 'given_name']

    @staticmethod
    def search(qs, pattern):
        return qs.filter(
            Q(given_name__icontains=pattern)
            | Q(family_name__icontains=pattern)
            | Q(positions__department__name__icontains=pattern)
        ).distinct()


class Position(models.Model):
    type = models.CharField(verbose_name="Type", max_length=500)
    info = models.CharField(verbose_name="Informasjon", max_length=500)
    person = models.ForeignKey(Person, verbose_name="Person", related_name="positions")
    department = models.ForeignKey(Department, verbose_name="Avdeling", related_name="positions")

    @staticmethod
    def search(qs, pattern):
        return qs.filter(
            Q(person__given_name__icontains=pattern)
            | Q(person__family_name__icontains=pattern)
        ).distinct()
