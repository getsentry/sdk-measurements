from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.response import Response
from datadog import initialize, statsd

from show.models import Show
from show.serializers import ShowListSerializer, ShowSerializer

options = {
    "statsd_host": "127.0.0.1",
    "statsd_port": 8126,
    "namespace": "django-react-app",
}
initialize(**options)


def index(request):
    bla = 1 / 0
    return HttpResponse("Hello, world. You're at the SHOW index.")


class ShowViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows shows to be viewed or edited.
    """

    serializer_class = ShowListSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ShowListSerializer
        return ShowSerializer

    @statsd.timed("views.get_queryset", sample_rate=1.0)
    def get_queryset(self):
        """
        This view should return a list of all Shows
        containing the search string in title, director, or cast.
        """
        queryset = Show.objects.all()
        q = self.request.query_params.get("q", None)
        if q:
            search_filter = (
                Q(title__icontains=q) | Q(director__icontains=q) | Q(cast__icontains=q)
            )
            queryset = queryset.filter(search_filter)

        return queryset
