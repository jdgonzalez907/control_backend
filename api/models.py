from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    '''
    '''
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Debe ingresar un email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    '''
    '''
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = []

    DOCUMENT_CC = 'CC'
    DOCUMENT_TI = 'TI'
    DOCUMENT_CE = 'CE'
    DOCUMENT_PP = 'PP'
    DOCUMENT_LIST = (
        (DOCUMENT_CC, 'Cédula de ciudadanía'),
        (DOCUMENT_TI, 'Tarjeta de identidad'),
        (DOCUMENT_CE, 'Cédula de extranjería'),
        (DOCUMENT_PP, 'Pasaporte')
    )

    username = None
    document_type = models.CharField(verbose_name='Tipo de documento', max_length=2, null=True, blank=False)
    identity_document = models.CharField(verbose_name='Número de documento', max_length=15, null=True, blank=False)
    birthdate = models.DateField(verbose_name='Fecha de nacimiento', null=True, blank=False)
    email = models.EmailField('Email', unique=True)

    # objects = CustomUserManager()
