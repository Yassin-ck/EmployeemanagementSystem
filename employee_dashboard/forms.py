from django import forms
from .models import (
    Notice_board,
    Department_notice,
    LeaveApply,
    TodayTasks,
    Paycheque,
    UserProfile,
)
from PIL import Image
import re


class DateInput(forms.DateInput):
    input_type = "date"


class TodayTaskForm(forms.ModelForm):
    class Meta:
        model = TodayTasks
        fields = ('comment',)


class NoticeboardForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    # def clean_image(self):
    #     image = self.cleaned_data.get('image')
    #     if image:
    #         img = Image.open(image)
    #         max_width =1000
    #         max_height =1000
    #         if img.width > max_width or img.height >max:
    #             raise forms.ValidationError('The image size exceeds the allowed limit')
    #     return image
    class Meta:
        model = Notice_board
        fields = ("title", "subject", "content", "image")

        def __init__(self, *args, **kwargs):
            super().save(*args, **kwargs)
            self.fields["image"].required = False


class DepartmentnoticeForm(forms.ModelForm):
    title = forms.CharField(required=False)
    subject = forms.CharField(required=False)

    class Meta:
        model = Department_notice
        fields = ("title", "subject", "content", "image")


# Dateinput


class LeaveForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    reason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = LeaveApply
        fields = ("start_date", "end_date", "reason")



class PaychequeForm(forms.ModelForm):
    

    class Meta:
        model = Paycheque
        fields = (
            "user",
            "base_salary",
            "allowances",
            "overtime_hours",
            "overtime_pay_rate",
            "bonus",
            "deductions",
        )

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['user'].required = False


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput)
    income = forms.FloatField()

    class Meta:
        model = UserProfile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].required = False

    def clean_alternative_number(self):
        alternative_number = self.cleaned_data["alternative_number"]
        if not re.match(r"^\+[0-9]+$", alternative_number):
            raise forms.ValidationError(
                'Alternative number should start with "+" and contain only digits.'
            )
        return alternative_number

    def clean_city(self):
        city = self.cleaned_data["city"]
        if not re.match(r"^[a-zA-Z]+$", city):
            raise forms.ValidationError(
                "City should only contain alphabetic characters."
            )
        return city

    def clean_state(self):
        state = self.cleaned_data["state"]
        if not re.match(r"^[a-zA-Z]+$", state):
            raise forms.ValidationError(
                "State should only contain alphabetic characters."
            )
        return state

    def clean_country(self):
        country = self.cleaned_data["country"]
        if not re.match(r"^[a-zA-Z]+$", country):
            raise forms.ValidationError(
                "Country should only contain alphabetic characters."
            )
        return country

