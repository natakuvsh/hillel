from django import forms
from django_school.models import Course, Student


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
