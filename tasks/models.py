from django.db import models
from django.conf import settings


class Company(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return f'{self.user.username} - {self.name}'


class Project(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	name = models.CharField(max_length=255)
	company = models.ForeignKey(Company, on_delete=models.PROTECT)
	started_at = models.DateField()
	ended_at = models.DateField(blank=True, null=True)

	def __str__(self):
		return f'{self.user.username} - {self.company.name} - {self.name}'


class Task(models.Model):

	class TaskLevel(models.TextChoices):
		easy = 'easy', 'Easy'
		normal = 'normal', 'Normal'
		hard = 'hard', 'Hard'

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	title = models.CharField(max_length=255)
	description = models.TextField()
	project = models.ForeignKey(Project, on_delete=models.PROTECT)
	level = models.CharField(
		max_length=64, choices=TaskLevel.choices, default=TaskLevel.easy
	)
	company = models.ForeignKey(Company, on_delete=models.PROTECT)
	working_minutes = models.PositiveIntegerField()
	total_minutes = models.PositiveIntegerField()
	started_at = models.DateTimeField()
	ended_at = models.DateTimeField()
	is_shallow_work = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.title} - {self.project} - {self.company}'