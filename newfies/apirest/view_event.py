# -*- coding: utf-8 -*-
#
# Newfies-Dialer License
# http://www.newfies-dialer.org
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2013 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#

from rest_framework import viewsets
from apirest.event_serializers import EventSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from appointment.models.events import Event


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows event to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication = (BasicAuthentication, SessionAuthentication)
    permissions = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the currently authenticated user.
        """
        if self.request.user.is_superuser:
            queryset = Event.objects.all()
        else:
            queryset = Event.objects.filter(creator=self.request.user)
        return queryset

    def pre_save(self, obj):
        obj.creator = self.request.user
