from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from authy.models import Profile


def forbidden_users(value):
	forbidden_users = [
		'admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
		'email', 'user', 'join', 'sql', 'static', 'python', 'delete'
	]
	if value.lower() in forbidden_users:
		raise ValidationError('Invalid name for user, this is a reserverd word.')


def invalid_user(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('アカウント名に次の文字は使えません: @ , - , + ')


def unique_email(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('このメールアドレスのユーザーは既に存在します。')


def unique_user(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('このアカウント名は既に存在します。')


class SignupForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True,)
	email = forms.CharField(widget=forms.EmailInput(), max_length=100, required=True,)
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm your password.")

	class Meta:

		model = User
		fields = ('username', 'email', 'password')

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(forbidden_users)
		self.fields['username'].validators.append(invalid_user)
		self.fields['username'].validators.append(unique_user)
		self.fields['email'].validators.append(unique_email)

	def clean(self):
		super(SignupForm, self).clean()
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password != confirm_password:
			self._errors['パスワード :'] = self.error_class(['パスワードが一致していません。'])
		return self.cleaned_data


class ChangePasswordForm(forms.ModelForm):
	id = forms.CharField(widget=forms.HiddenInput())
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Old password", required=True)
	new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="New password", required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Confirm new password", required=True)

	class Meta:
		model = User
		fields = ('id', 'old_password', 'new_password', 'confirm_password')

	def clean(self):
		super(ChangePasswordForm, self).clean()
		id = self.cleaned_data.get('id')
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		user = User.objects.get(pk=id)
		if not user.check_password(old_password):
			self._errors['現在のパスワード :'] = self.error_class(['現在のパスワードが一致しません。'])
		if new_password != confirm_password:
			self._errors['新しいパスワード :'] = self.error_class(['新しいパスワードが一致しません。'])
		return self.cleaned_data


class EditProfileForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
	last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
	location = forms.CharField(widget=forms.TextInput(), max_length=25, required=False)
	url = forms.URLField(widget=forms.TextInput(), max_length=60, required=False)
	profile_info = forms.CharField(widget=forms.TextInput(), max_length=260, required=False)

	class Meta:
		model = Profile
		fields = ('picture', 'first_name', 'last_name', 'location', 'url', 'profile_info')
