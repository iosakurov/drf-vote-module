from rest_framework import serializers
from .models import Profile, Vote
import time


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'name']

    def get_name(self, obj):
        return obj.user.username


class VoteSerializer(serializers.ModelSerializer):
    voter = ProfileSerializer()
    candidate = ProfileSerializer()

    class Meta:
        model = Vote
        fields = ['id', 'is_like', 'voter', 'candidate', 'date_first', 'date_modify']
        read_only_fields = ['voter', 'candidate', 'date_first', 'date_modify']
