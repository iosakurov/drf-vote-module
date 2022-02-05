from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'votes', views.VoteViewSet)
router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [
	path('', include(router.urls))
	# path('votes/', views.VoteList.as_view()),
	# path('votes/<int:pk>', views.VoteDetail.as_view()),

	# path('votes/<int:profile_id>/votesScore', views.VoteDetail.as_view()),
	# path('votes/voteFor', views.VoteDetail.as_view()),
	# path('votes/voteAgainst', views.VoteDetail.as_view()),
	# path('votes/<int:pk>/votersMeScore', views.VoteDetail.as_view()),
	# path('votes/<int:pk>/againstMeScore', views.VoteDetail.as_view()),
	# path('votes/<int:pk>/againstMeScore', views.VoteDetail.as_view()),
	# path('votes/mostPopular', views.ProfileDetail.as_view()),

	# path('profiles/', views.ProfileList.as_view()),
	# path('profiles/<int:pk>', views.ProfileDetail.as_view()),

	# path('profiles/getVotesInfo', views.ProfileDetail.as_view()),
	# path('profiles/getVotersMe', views.ProfileDetail.as_view()),
	# path('profiles/getAgainstMe', views.ProfileDetail.as_view()),
	# path('profiles/<int:pk>/votes/addVote', views.ProfileDetail.as_view()),
	# path('profiles/<int:pk>/votes/deleteVote', views.ProfileDetail.as_view()),
]
