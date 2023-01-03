from django import forms
from django_school.models import Teacher, Group, Course, Student


def check_surname(surname):
    if Student.objects.filter(surname=surname):
        raise forms.ValidationError("Surname must be unique")
    return surname


class CourseCreateForm(forms.Form):
    name = forms.CharField(required=True)
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())
    description = forms.CharField(widget=forms.widgets.Textarea(attrs={'cols': 50, 'rows': 3}))
    theses = forms.CharField(widget=forms.widgets.Textarea(attrs={'cols': 50, 'rows': 3}))
    image = forms.ImageField()
    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.widgets.CheckboxSelectMultiple
    )

    def clean_name(self):
        if Course.objects.filter(name=self.cleaned_data['name']):
            raise forms.ValidationError("Course with this name already exists. Enter another name")
        return name

    def create_course(self):
        course = Course.objects.create(
            name=self.cleaned_data['name'],
            teacher=self.cleaned_data['teacher'],
            description=self.cleaned_data['description'],
            theses=self.cleaned_data['theses'],
            image=self.cleaned_data['image'],
        )

        course.group.add(*self.cleaned_data['group'])
        return course


class StudentCreateForm(forms.Form):
    name = forms.CharField(strip=True)
    surname = forms.CharField(required=True, strip=True, validators=[check_surname])
    age = forms.IntegerField(min_value=18, max_value=130)
    email = forms.EmailField()
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.widgets.CheckboxSelectMultiple
    )

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

    def create_student(self):
        student = Student.objects.create(
            name=self.cleaned_data['name'],
            surname=self.cleaned_data['surname'],
            age=self.cleaned_data['age'],
            email=self.cleaned_data['email'],
            course=self.cleaned_data['course'],
        )

        student.group.add(*self.cleaned_data['group'])
        return student

