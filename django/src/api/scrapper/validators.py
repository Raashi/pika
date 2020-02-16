from rest_framework.fields import CharField
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


class MultipleUniqueValidator:
    message = 'Multiple equal values provided for unique field {}'
    requires_context = True

    def __call__(self, arr, serializer):
        checks = {}

        for field_name, field_obj in serializer.child.fields.items():
            if hasattr(field_obj, 'unique_validator'):
                checks[field_name] = set()

        for attrs in arr:
            for field_name, field_checks in checks.items():
                if field_name not in attrs or attrs[field_name] is None:
                    continue
                if attrs[field_name] in field_checks:
                    raise ValidationError(self.message.format(field_name))
                field_checks.add(attrs[field_name])


class VeryMultipleUniqueValidator:
    message = 'Multiple equal values provided for unique field {} in different parent objects {}'
    ignore_values = [None, '']
    requires_context = True

    def __call__(self, arr, serializer):
        checks = {}

        child_fields = getattr(serializer.child.Meta, 'child_fields', [])
        if not child_fields:
            return

        for field in serializer.child.Meta.child_fields:
            for child_field, child_field_obj in serializer.child.fields[field].child.fields.items():
                if hasattr(child_field_obj, 'unique_validator'):
                    if field not in checks:
                        checks[field] = {}
                    checks[field][child_field] = set()

        for item in arr:
            for field in serializer.child.Meta.child_fields:
                for sub_item in item[field]:
                    for sub_field in checks[field]:
                        value = sub_item.get(sub_field, None)
                        if value in self.ignore_values:
                            continue
                        if value in checks[field][sub_field]:
                            raise ValidationError(self.message.format(sub_field, field))
                        checks[field][sub_field].add(value)


class NotBlankUniqueValidator(UniqueValidator):
    ignore_values = [None, '']

    def __init__(self, unique_validator):
        super().__init__(unique_validator.queryset, unique_validator.message, unique_validator.lookup)

    def __call__(self, value, serializer_field):
        if isinstance(serializer_field, CharField) and value in self.ignore_values:
            return

        super().__call__(value, serializer_field)
