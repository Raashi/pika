from rest_framework.fields import CharField
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


class MultipleUniqueValidator:
    message = 'Multiple equal values provided for unique field {}'
    requires_context = True

    def __init__(self, queryset=None, message=None, lookup='exact'):
        self.queryset = queryset
        self.message = message or self.message
        self.lookup = lookup

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


class NotBlankUniqueValidator(UniqueValidator):
    ignore_values = [None, '']

    def __init__(self, unique_validator):
        super().__init__(unique_validator.queryset, unique_validator.message, unique_validator.lookup)

    def __call__(self, value, serializer_field):
        if isinstance(serializer_field, CharField) and value in self.ignore_values:
            return

        super().__call__(value, serializer_field)
