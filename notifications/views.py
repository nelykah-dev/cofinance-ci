from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .models import Notification
from .serializers import NotificationSerializer

class MesNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(destinataire=self.request.user)

class MarquerLuView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: NotificationSerializer})
    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, destinataire=request.user)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification introuvable'}, status=404)
        notification.est_lu = True
        notification.save()
        return Response(NotificationSerializer(notification).data)

class MarquerToutesLuesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: dict})
    def patch(self, request):
        Notification.objects.filter(
            destinataire=request.user,
            est_lu=False
        ).update(est_lu=True)
        return Response({'message': 'Toutes les notifications marquées comme lues'})