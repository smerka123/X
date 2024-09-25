from rest_framework import serializers, viewsets
from .models import Tweet, Like, Follow

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['id', 'user', 'content', 'created_at']

# Tweet Viewset
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-created_at')
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def feed(self, request):
        user = request.user
        following_users = user.following.values_list('following_id', flat=True)
        tweets = Tweet.objects.filter(user__id__in=following_users)
        serializer = self.get_serializer(tweets, many=True)
        return Response(serializer.data)
