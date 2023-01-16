from django import forms
from django.core.exceptions import ValidationError
from django_school.models import Course, Student, NewLot
from django_school.tasks import send_emails_new_course


class StudentCreateForm(forms.ModelForm):
    age = forms.IntegerField(min_value=18, max_value=130)

    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'group': forms.widgets.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(StudentCreateForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.order_by('-name')

    def clean_name(self):
        name = self.cleaned_data['name']
        if " " in name:
            raise forms.ValidationError("Please do not use whitespaces")
        return name

    def clean_surname(self):
        surname = self.cleaned_data['surname']
        if " " in surname:
            raise forms.ValidationError("Please do not use whitespaces")
        return surname


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'group': forms.widgets.CheckboxSelectMultiple(),
            'theses': forms.Textarea(attrs={'cols': 50, 'rows': 4}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 4})
        }

    def send_email(self):
        print(type(self.cleaned_data))
        send_emails_new_course.delay(name=self.cleaned_data['name'], description=self.cleaned_data['description'])


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'group': forms.widgets.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.order_by('-name')
        self.fields['surname'].widget.attrs['readonly'] = True
        self.fields['age'].widget.attrs['readonly'] = True


class CreateLotForm(forms.ModelForm):
    class Meta:
        model = NewLot
        fields = ('name', 'bid')


class UpdateLotForm(forms.ModelForm):
    class Meta:
        model = NewLot
        fields = ('bid',)


class CloseLotForm(forms.ModelForm):
    class Meta:
        model = NewLot
        fields = ('closed',)

