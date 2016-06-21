from django.shortcuts import render
from django.http import Http404
from django.template.response import TemplateResponse

from rest_framework import serializers, viewsets, routers

from . import models

# Create your views here.
def rsvp_page(request):
    context = {}
    return TemplateResponse(request, 'rsvp/rsvp.html', context)

class RSVPSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)

    rsvp = serializers.NullBooleanField()
    details = serializers.CharField(allow_blank=True)
    email = serializers.CharField(allow_blank=True)
    status = serializers.CharField(required=False)

    class Meta:
        model = models.RSVP
        
        fields = ['uuid', 'rsvp', 'details', 'email', 'status']

class RSVPViewSet(viewsets.ModelViewSet):
    serializer_class = RSVPSerializer
    queryset = models.RSVP.objects.all()

    def get_queryset(self):
        return self.queryset.filter(client_id=self.client_id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        try:
            return super(RSVPViewSet, self).update(request, *args, **kwargs)
        except Http404:
            if partial:
                raise

            # Allow PUT to create
            return super(RSVPViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        save_kwargs = {
            'client_id': self.client_id,
        }

        # Allow PUT to create: if this is a PUT, we'll get the primary key in
        # the URL kwargs.
        #
        # If you're using some other url-kwargs or are indexing models by some
        # other key, then adapt this logic to match.
        if 'pk' in self.kwargs:
            save_kwargs['pk'] = self.kwargs['pk']

        serializer.save(**save_kwargs)

    def initial(self, request, *args, **kwargs):
        super(RSVPViewSet, self).initial(request, *args, **kwargs)

        self.client_id = self.request.META['HTTP_X_HEIDTCO_CLIENT_ID']


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'rsvp', RSVPViewSet, base_name='rsvp')
