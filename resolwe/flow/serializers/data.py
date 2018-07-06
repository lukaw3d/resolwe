"""Resolwe data serializer."""
from rest_framework import serializers

from resolwe.flow.models import Data, DescriptorSchema
from resolwe.rest.fields import ProjectableJSONField

from .base import ResolweBaseSerializer
from .descriptor import DescriptorSchemaSerializer


class DataSerializer(ResolweBaseSerializer):
    """Serializer for Data objects."""

    input = ProjectableJSONField(required=False)
    output = ProjectableJSONField(required=False)
    descriptor = ProjectableJSONField(required=False)
    process_slug = serializers.CharField(source='process.slug', read_only=True)
    process_name = serializers.CharField(source='process.name', read_only=True)
    process_type = serializers.CharField(source='process.type', read_only=True)
    process_input_schema = ProjectableJSONField(source='process.input_schema', read_only=True)
    process_output_schema = ProjectableJSONField(source='process.output_schema', read_only=True)

    class Meta:
        """DataSerializer Meta options."""

        model = Data
        read_only_fields = (
            'checksum',
            'created',
            'descriptor_dirty',
            'finished',
            'id',
            'modified',
            'process_cores',
            'process_error',
            'process_info',
            'process_input_schema',
            'process_memory',
            'process_name',
            'process_output_schema',
            'process_progress',
            'process_rc',
            'process_slug',
            'process_type',
            'process_warning',
            'output',
            'size',
            'started',
            'status',
        )
        update_protected_fields = (
            'contributor',
            'input',
            'process',
        )
        fields = read_only_fields + update_protected_fields + (
            'descriptor',
            'descriptor_schema',
            'name',
            'slug',
            'tags',
        )

    def get_fields(self):
        """Dynamically adapt fields based on the current request."""
        fields = super(DataSerializer, self).get_fields()

        if self.request.method == "GET":
            fields['descriptor_schema'] = DescriptorSchemaSerializer(required=False)
        else:
            fields['descriptor_schema'] = serializers.PrimaryKeyRelatedField(
                queryset=DescriptorSchema.objects.all(), required=False
            )

        return fields
