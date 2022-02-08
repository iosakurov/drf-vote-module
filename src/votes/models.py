from django.contrib.auth.models import User
from django.core import exceptions
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Vote(models.Model):
	is_like = models.BooleanField()
	date_first = models.DateTimeField(auto_now_add=True)
	date_modify = models.DateTimeField(auto_now=True)

	voter = models.ForeignKey(
		'Profile',
		on_delete=models.CASCADE,
		related_name='my_votes')
	candidate = models.ForeignKey(
		'Profile',
		on_delete=models.CASCADE,
		related_name='votes_me'
	)

	class Meta:
		unique_together = ('voter', 'candidate')

	def __str__(self):
		return f'{self.voter} to {self.candidate} Like:{self.is_like}'

	def vote_like(self):
		self.is_like = True
		print(self.is_like)
		self.save()

	def vote_dislike(self):
		self.is_like = False
		self.save()

	def clean(self):
		print('Clean')
		if self.voter.pk == self.candidate.pk:
			raise exceptions.ValidationError(
				'Самому себе лайки нельзя ставить',
				code='you_cant_vote_by_yourself',
				params={'author_like': self.voter, 'who_liked': self.candidate}
			)
		super(Vote, self).clean()

	def save(self, *args, **kwargs):
		if self.voter.pk == self.candidate.pk:
			raise exceptions.ValidationError(
				f'Самому себе лайки нельзя ставить',
				code='you_cant_vote_by_yourself',
				params={'author_like': self.voter, 'who_liked': self.candidate}
			)

		super(Vote, self).save(*args, **kwargs)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def vote_for_candidate(self, profile, is_like=True):
		if not isinstance(profile, Profile):
			raise TypeError(
				f"'{profile}' должен быть Profile, а получен {type(profile)}"
			)

		try:
			like = Vote.objects.get(voter=self, candidate=profile)
			print('Голос найден')
			like.is_like = is_like
			like.save()
		except Vote.DoesNotExist:
			print('Такого голоса нет, создаем')
			Vote.objects.create(voter=self, candidate=profile, is_like=is_like)
			print('Голос успешно создан')

	def __str__(self):
		return f'{self.user.username}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
	try:
		Profile.objects.get(user=instance)
	except Profile.DoesNotExist:
		print('Create profile for ', instance)
		profile = Profile.objects.create(user=instance)
		profile.save()
