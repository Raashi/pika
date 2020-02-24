from rest_framework.fields import CharField
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


class MultipleUniqueValidator:
    message = 'Multiple equal values provided for unique field {} with value {}'
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
                    msg = self.message.format(field_name, attrs[field_name])
                    raise ValidationError(msg)
                field_checks.add(attrs[field_name])


class MultipleUniqueByLookupValidator:
    message = 'Multiple equal by lookup fields values provided with value {}'
    missing_message = 'Lookup fields must be required'
    requires_context = True

    def __call__(self, arr, serializer):
        checks = set()
        for item in arr:
            self.enforce_required_fields(item, serializer.child)
            value = tuple(item[field] for field in serializer.lookup_fields)
            if value in checks:
                raise ValidationError(self.message.format(value))
            checks.add(value)

    def enforce_required_fields(self, attrs, serializer):
        """
        The `UniqueTogetherValidator` always forces an implied 'required'
        state on the fields it applies to.
        """
        if serializer.instance is not None:
            return

        missing_items = {
            field_name: self.missing_message
            for field_name in serializer.lookup_fields
            if serializer.fields[field_name].source not in attrs
        }
        if missing_items:
            raise ValidationError(missing_items, code='required')


class NotBlankUniqueValidator(UniqueValidator):
    ignore_values = [None, '']

    def __init__(self, unique_validator):
        super().__init__(unique_validator.queryset, unique_validator.message, unique_validator.lookup)

    def __call__(self, value, serializer_field):
        if isinstance(serializer_field, CharField) and value in self.ignore_values:
            return

        super().__call__(value, serializer_field)
