from rest_framework.exceptions import ValidationError


class MultipleUniqueValidator:
    message = 'Multiple equal (by lookup fields) objects'
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
                    raise ValidationError(self.message)
                field_checks.add(attrs[field_name])
