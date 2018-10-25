from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, document_type, identity_document, birthdate, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            document_type=document_type,
            identity_document=identity_document,
            birthdate=birthdate
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, document_type, identity_document, birthdate, password):
        user = self.model(
            email=email,
            document_type=document_type,
            identity_document=identity_document,
            birthdate=birthdate
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self.db)
        return user

class CustomUser(AbstractUser):
    '''
    '''
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['document_type', 'identity_document', 'birthdate']

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

    document_type = models.CharField(verbose_name='Tipo de documento', max_length=2, choices=DOCUMENT_LIST)
    identity_document = models.CharField(verbose_name='Número de documento', max_length=15)
    birthdate = models.DateField(verbose_name='Fecha de nacimiento')
    email = models.EmailField(_('email address'), blank=True, unique=True)

    objects = CustomUserManager
