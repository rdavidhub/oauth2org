from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from .utils import get_id_token_payload

# Copyright Videntity Systems Inc.

__author__ = "Alan Viars"


SEX_CHOICES = (('male', 'Male'), ('female', 'Female'), ('', 'Unspecified'))


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='userprofile', on_delete=models.CASCADE,
                                db_index=True, null=False)
    subject = models.CharField(max_length=64, default='', blank=True,
                               help_text='Subject for identity token',
                               db_index=True)
    nickname = models.CharField(
        max_length=255,
        default='',
        blank=True,
        help_text='Nickname, alias, or other names used.')
    middle_name = models.CharField(max_length=255, default='', blank=True)
    email_verified = models.BooleanField(default=False, blank=True)
    phone_verified = models.BooleanField(default=False, blank=True)
    picture_url = models.CharField(blank=True, default="", max_length=1024,
                                   help_text=_('A public URL to a profile picture'))
    mobile_phone_number = models.CharField(max_length=25, blank=True, default="",
                                           help_text=_('US numbers only.'),)
    mobile_phone_number_verified = models.BooleanField(
        blank=True, default=False)

    four_digit_suffix = models.CharField(
        max_length=4, blank=True, default="",
        help_text=_('If populated, this field must contain exactly four numbers.'),)

    gender = models.CharField(choices=SEX_CHOICES,
                              max_length=32, default="",
                              help_text=_('Birth Sex Gender'),
                              )
    gender_identity = models.CharField(max_length=64, default="",
                                       help_text=_('Gender Identity'),
                                       )

    identity_assurance_level = models.CharField(choices=(('1', '1'), ('2', '2'), ('3', '3')),
                                                max_length=1, default="1",
                                                help_text=_(
                                                    'Identity Assurance Level'),
                                                )

    birth_date = models.DateField(blank=True, null=True)
    most_recent_id_token_payload = models.TextField(
        blank=True, default="", max_length=4096)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        display = '%s %s (%s)' % (self.user.first_name,
                                  self.user.last_name,
                                  self.user.username)
        return display

    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)
        self._id_token_payload = get_id_token_payload(self.user)

    @property
    def id_token_payload(self):
        """Return the token Payload as a"""
        return self._id_token_payload

    @property
    def ssn(self):
        num = ""
        for doc in self.doc:
            if doc['type'] == "SSN":
                num = doc['num']
        return num

    @property
    def doc(self):
        doc = self.id_token_payload.get('document')
        if not doc:
            doc = []
        return doc

    @property
    def fhir_patient_id(self):
        doc = self.id_token_payload.get('document')
        for d in doc:
            if d["type"] == "PATIENT_ID_FHIR":
                return d["num"]
        return None

    @property
    def fhir_user(self):
        return "%s%s" % (self.user.fhir_patient_id)

    @property
    def given_name(self):
        return self.user.first_name

    @property
    def family_name(self):
        return self.user.last_name

    @property
    def phone_number(self):
        return str(self.mobile_phone_number)

    def get_verified_phone_number(self):
        return self.phone_number if self.phone_verified else None

    @property
    def preferred_username(self):
        return self.user.username

    @property
    def preferred_gender(self):
        return self.sex

    @property
    def preferred_birthdate(self):
        return str(self.birth_date)

    @property
    def sub(self):
        return self.subject

    @property
    def sex(self):
        return self.gender

    @property
    def gender_intersystems(self):
        if self.gender == 'male':
            return 'M'
        if self.gender == 'female':
            return 'F'

    @property
    def birthdate(self):
        return self.birth_date

    @property
    def birthdate_intersystems(self):
        return str(self.birth_date).replace('-', '')

    @property
    def name(self):
        name = '%s %s' % (self.user.first_name, self.user.last_name)
        return name

    @property
    def ial(self):
        return ""

    @property
    def profile_url(self):
        return ""

    @property
    def website(self):
        return ""

    @property
    def picture(self):
        return ""

    @property
    def address(self):
        return ""
