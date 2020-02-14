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


class BaseUploadSerializer(ModelSerializer):
    class Meta:
        model: Type[models.Model] = None
        lookup_field: str = None

    def __init__(self, instance=None, data=empty, **kwargs):
        many = kwargs.get('many', False)

        if not many:
            self.lookup_field = getattr(self.Meta, 'lookup_field', None)
            if self.lookup_field is None:
                self.lookup_field = self.Meta.model._meta.pk.name

            if isinstance(self.lookup_field, str):
                self.lookup_field = [self.lookup_field]

        super().__init__(instance=instance, data=data, **kwargs)

        for field_obj in self.fields.values():
            for validator in field_obj.validators:
                if isinstance(validator, UniqueValidator):
                    field_obj.validators.remove(validator)
                    break

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
        try:
            instance = self.Meta.model.objects.get(**{field: data[field] for field in self.lookup_field})
            return instance
        except self.Meta.model.DoesNotExist:
            return None


class BaseListSerializer(ListSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instances = []

    def try_set_child_instance(self, child_data):
        return self.child.try_get_instance(child_data)

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
                instance = self.try_set_child_instance(validated)
                self.instances.append(instance)
            except ValidationError as exc:
                errors.append(exc.detail)
            else:
                ret.append(validated)
                errors.append({})

        if any(errors):
            raise ValidationError(errors)

        return ret

    def create(self, validated_data):
        return self.child.create(validated_data)

    def update(self, instance, validated_data):
        return self.child.update(instance, validated_data)

    def save(self, **kwargs):
        validated_data = [dict(list(attrs.items()) + list(kwargs.items())) for attrs in self.validated_data]

        ret = []
        for instance, attrs in zip(self.instances, validated_data):
            if instance is not None:
                ret.append(self.update(instance, attrs))
            else:
                ret.append(self.create(attrs))


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
