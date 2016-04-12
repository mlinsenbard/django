from django.db import models

# Create your models here.

class Tag(models.Model):
	subject = models.CharField(max_length=64)

	def __unicode__(self):
		return self.subject

class BlogEntry(models.Model):
	title = models.CharField(max_length=64)
	subtitle = models.CharField(max_length=64)
	content = models.TextField()
	# the <path-to-static>/img/ filename
	picture = models.CharField(max_length=128, blank=True)
	tags = models.ManyToManyField(Tag)
	date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

class Project(models.Model):
	title = models.CharField(max_length=64)
	description = models.CharField(max_length=512)
	# same as Blog pciture
	picture = models.CharField(max_length=128, blank=True)
	links = models.TextField()

	def __unicode__(self):
		return self.title

class Fight(models.Model):
	instigator = models.CharField(max_length=32)
	target = models.CharField(max_length=32)
	i_hp = models.FloatField(default=100)
	t_hp = models.FloatField(default=100)
	turn = models.BooleanField(default=True)