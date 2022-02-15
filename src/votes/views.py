from django.core import exceptions
from rest_framework import status, filters, viewsets
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import action
import django_filters

from .models import Vote, Profile
from .serializers import VoteSerializer, ProfileSerializer
from .filters import VoteFilter


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_class = VoteFilter
    filter_backends = [filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    ordering = ['-id']
    ordering_fields = ['id']

    @action(methods=['post'], detail=False, url_path='addVote')
    def add_vote(self, request, *args, **kwargs):
        # TODO:
        # Выяснить, если смысл в этом методе, а то похоже на
        # Vote.objects.create(), но с доп проверкой и в отдельном методе

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
            vote = Vote.objects.get(voter=voter, candidate=candidate)

            return Response({'message': 'Голос обновлен!',
                             'url': reverse('vote-detail', args=[vote.pk], request=request)},
                            status=status.HTTP_200_OK)
        except Vote.DoesNotExist:
            try:
                vote = Vote.objects.create(voter=voter,
                                           candidate=candidate,
                                           is_like=is_like)
            except exceptions.ValidationError as e:
                return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VoteSerializer(vote)

        return Response({'message': 'Вы успешно проголосовали', 'result': serializer.data},
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='getInfoVotes')
    def info(self, request, *args, **kwargs):
        votes_count = Vote.objects.all().count()
        votes_for = Vote.objects.filter(is_like=True).count()
        votes_against = Vote.objects.filter(is_like=False).count()

        return Response({
            'votes': {
                'count': votes_count,
                'for': votes_for,
                'against': votes_against
            }
        }, status=status.HTTP_200_OK)
