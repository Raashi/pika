from typing import Type

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from rest_framework.serializers import ModelSerializer, ListSerializer, HiddenField
from rest_framework.fields import empty
from rest_framework.validators import UniqueValidator

UserModel = get_user_model()


TMDB_image_fields = ['path', 'aspect_ratio', 'width', 'height', 'vote_average', 'vote_count']
TMDB_video_fields = ['tmdb_id', 'language', 'country', 'key', 'name', 'size', 'type']
TMDB_review_fields = ['tmdb_id', 'author', 'content', 'url', 'language']


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


class BaseUploadSerializer(ModelSerializer):
    class Meta:
        model: Type[models.Model] = None
        lookup_field: str = None

    def __init__(self, instance=None, data=empty, **kwargs):
        self.lookup_field = self.get_lookup_field()
        super().__init__(instance=instance, data=data, **kwargs)

        for field_obj in self.fields.values():
            for validator in field_obj.validators:
                if isinstance(validator, UniqueValidator):
                    field_obj.validators.remove(validator)
                    # remember validator
                    field_obj.unique_validator = validator
                    break

    def get_lookup_field(self):
        lookup_field = getattr(self.Meta, 'lookup_field', None)
        if lookup_field is None:
            lookup_field = self.Meta.model._meta.pk.name

        if isinstance(lookup_field, str):
            lookup_field = [lookup_field]

        return lookup_field

    def updated_related(self, serializers, movie, field='id'):
        objects = []
        for serializer in serializers:
            serializer.validated_data['movie'] = movie
            objects.append(serializer.save())

        if len(objects):
            manager = objects[0].objects
            values = [getattr(obj, field) for obj in objects]
            manager.filter(~Q(**{field + '__in': values})).delete()

    def try_get_instance(self, data):
        attrs = {}
        for field in self.lookup_field:
            # all lookup_fields are required
            attrs[field] = data[field]

        try:
            return self.Meta.model.objects.get(**attrs)
        except self.Meta.model.DoesNotExist:
            pass
        # return status-code=500 if there are multiples in db

    def hard_save(self, validated_data, instance):
        self.instance = instance
        self._errors = {}
        self._validated_data = validated_data
        return self.save()


class BaseListSerializer(ListSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instances = []
        self.validators.append(MultipleUniqueValidator())
        self.lookup_field = self.child.lookup_field

    def to_internal_value(self, data):
        if not isinstance(data, list):
            message = self.error_messages['not_a_list'].format(input_type=type(data).__name__)
            raise ValidationError({api_settings.NON_FIELD_ERRORS_KEY: [message]}, code='not_a_list')

        if not self.allow_empty and len(data) == 0:
            message = self.error_messages['empty']
            raise ValidationError({api_settings.NON_FIELD_ERRORS_KEY: [message]}, code='empty')

        ret = []
        errors = []

        for item in data:
            try:
                validated = self.child.run_validation(item)
                instance = self.child.try_get_instance(item)

                if instance is None:
                    for field, field_obj in self.child.fields.items():
                        if hasattr(field_obj, 'unique_validator'):
                            field_obj.unique_validator(validated[field], field_obj)

                self.instances.append(instance)
            except ValidationError as exc:
                errors.append(exc.detail)
            else:
                ret.append(validated)
                errors.append({})

        if any(errors):
            raise ValidationError(errors)

        return ret

    def _hard_save(self, validated_data):
        ret = []

        for instance, attrs in zip(self.instances, validated_data):
            self.child._errors = {}
            self.child._validated_data = attrs
            self.child.instance = instance
            ret.append(self.child.hard_save(attrs, instance))

        return ret

    def hard_save(self, validated_data):
        return self._hard_save(validated_data)

    def save(self, **kwargs):
        validated_data = [dict(list(attrs.items()) + list(kwargs.items())) for attrs in self.validated_data]
        return self._hard_save(validated_data)


class LoginSerializer(ModelSerializer):
    is_admin = HiddenField(default=True)
    is_active = HiddenField(default=True)

    class Meta:
        model = UserModel
        fields = ['is_admin', 'is_active', 'password', UserModel.USERNAME_FIELD]

        # suppress checking username uniqueness
        extra_kwargs = {UserModel.USERNAME_FIELD: {'validators': []}}

    def validate(self, attrs):
        password = attrs.pop('password')
        try:
            user = UserModel.objects.get(**attrs)
        except UserModel.DoesNotExist:
            raise ValidationError('Incorrect credentials')

        if not user.check_password(password):
            raise ValidationError('Incorrect credentials')

        attrs['user'] = user

        return attrs

    def save(self, **kwargs):
        # TODO: change class
        # serializers is read_only
        raise Exception
