from rest_framework import serializers


class BulkUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    name = serializers.CharField(required=True)

    class Meta:
        model = None
        fields = (
            'name',
            'file',
        )
