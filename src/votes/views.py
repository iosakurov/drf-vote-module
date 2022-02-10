from django.core import exceptions
import django_filters
from rest_framework import generics, status, filters
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Vote, Profile
from .serializers import VoteSerializer, ProfileSerializer


class VoteFilter(django_filters.FilterSet):
    voter = django_filters.CharFilter(field_name='voter__user__username', lookup_expr='iexact')
    candidate = django_filters.CharFilter(field_name='candidate__user__username', lookup_expr='iexact')

    class Meta:
        model = Vote
        fields = ['id', 'candidate', 'voter', 'is_like']


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    # permission_classes = [permissions.IsAuthenticated]

    ordering_fields = ['id']
    ordering = ['-id']
    filter_backends = [filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    filter_class = VoteFilter

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
