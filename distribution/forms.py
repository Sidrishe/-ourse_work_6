from django import forms
from users.forms import StyleFormMixin
from .models import Distribution, Message, DistributionClient


class DistributionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Distribution
        fields = ('start_time', 'end_time', 'frequency', 'status', 'distribution_client', 'message')


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'body')


class DistributionClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = DistributionClient
        fields = ('first_name', 'last_name', 'email', 'comment')
