from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import serializers, status
from rest_framework.throttling import AnonRateThrottle

from .parser import TerminalCommandDispatcher
from apps.telemetry.models import InteractionMetric


class TerminalThrottle(AnonRateThrottle):
    scope = 'terminal'


class CommandRequestSerializer(serializers.Serializer):
    command = serializers.CharField(max_length=512, allow_blank=False)


class TerminalExecuteView(APIView):
    """
    Simulated hacker/developer terminal API.
    Receives CLI string, runs it through TerminalCommandDispatcher,
    and returns output and status code for terminal UI widgets.
    """
    permission_classes = [AllowAny]
    throttle_classes = [TerminalThrottle]

    def post(self, request):
        serializer = CommandRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        command_str = serializer.validated_data['command']

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        client_ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')

        # Log telemetry interaction
        try:
            InteractionMetric.objects.create(
                interaction_type='TERMINAL_COMMAND',
                target_identifier=command_str[:255]
            )
        except Exception:
            pass

        result = TerminalCommandDispatcher.execute(command_str, client_ip=client_ip)
        return Response(result, status=status.HTTP_200_OK)
