from rest_framework import serializers

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            for field_name in set(self.fields.keys()) - set(fields):
                self.fields.pop(field_name)
