from django.core import exceptions
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Vote, Profile
from .serializers import VoteSerializer, ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer


class VoteViewSet(viewsets.ModelViewSet):
	queryset = Vote.objects.all()
	serializer_class = VoteSerializer

	@action(methods=['POST'], detail=False)
	def add_vote(self, request, *args, **kwargs):
		print('add_vote')

		try:
			voter = Profile.objects.get(user=request.user)
		except Profile.DoesNotExist:
			return Response({'message': 'voter не найден'})

		try:
			candidate = Profile.objects.get(pk=request.data['candidate'])
		except Profile.DoesNotExist:
			return Response({'message': 'candidate не найден'})

		is_like = request.data['is_like']

		try:
			Vote.objects.get(voter=voter, candidate=candidate)
			return Response({'message': 'Вы отдали голос этому профилю'},
							status=status.HTTP_400_BAD_REQUEST)
		except Vote.DoesNotExist:
			try:
				vote = Vote.objects.create(voter=voter,
										   candidate=candidate,
										   is_like=is_like)
			except exceptions.ValidationError as e:
				return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)

		serializer = VoteSerializer(vote)

		return Response({'message': 'You have successfully voted', 'vote': serializer.data},
						status=status.HTTP_200_OK)


class VoteList(generics.ListAPIView):
	queryset = Vote.objects.all()
	serializer_class = VoteSerializer


class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Vote.objects.all()
	serializer_class = VoteSerializer


class ProfileList(generics.ListAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer


class VoteVotersMeView(generics.RetrieveAPIView):
	pass


class VoteAgainstMeView(generics.RetrieveAPIView):
	pass


class VotesInfoView(generics.RetrieveAPIView):
	queryset = Vote.objects.all()
	serializer_class = VoteSerializer
