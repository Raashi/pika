from typing import Type

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from rest_framework.serializers import ModelSerializer, ListSerializer, HiddenField
from rest_framework.fields import empty
from rest_framework.validators import UniqueValidator

from .validators import MultipleUniqueValidator

UserModel = get_user_model()


TMDB_image_fields = ['path', 'aspect_ratio', 'width', 'height', 'vote_average', 'vote_count']
TMDB_video_fields = ['tmdb_id', 'language', 'country', 'key', 'name', 'size', 'type']
TMDB_review_fields = ['tmdb_id', 'author', 'content', 'url', 'language']


class BaseUploadSerializer(ModelSerializer):
    """
    all lookup fields must be required and not_null
    """

    class Meta:
        model: Type[models.Model] = None
        lookup_fields: str or list = None

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)

        self.lookup_fields = self._init_lookup_fields()
        self._init_unique_validators()

    def _init_lookup_fields(self):
        lookup_fields = getattr(self.Meta, 'lookup_fields', None)
        if lookup_fields is None:
            lookup_fields = self.Meta.model._meta.pk.name

        if isinstance(lookup_fields, str):
            lookup_fields = [lookup_fields]

        return lookup_fields

    def _init_unique_validators(self):
        for field_obj in self.fields.values():
            for validator in field_obj.validators:
                if isinstance(validator, UniqueValidator):
                    field_obj.validators.remove(validator)
                    # remember validator
                    field_obj.unique_validator = validator
                    break

    def try_get_instance(self, validated_data):
        """raise Exception if there are multiples in db (by lookup_fields)"""
        attrs = {}
        for field in self.lookup_fields:
            # all lookup_fields are required
            attrs[field] = validated_data[field]

        try:
            return self.Meta.model.objects.get(**attrs)
        except self.Meta.model.DoesNotExist:
            pass

    # helper shortcuts
    def save_arr_of_related(self, validated_data, field_name, related_field_name, related_obj):
        for item in validated_data:
            item[related_field_name] = related_obj
        return self.fields[field_name].save(validated_data=validated_data)

    def save_arr_of_m2m(self, validated_data, field_name):
        return self.fields[field_name].save(validated_data=validated_data)


class BaseListSerializer(ListSerializer):
    def __init__(self, *args, **kwargs):
        if 'child' in kwargs:
            assert isinstance(kwargs['child'], BaseUploadSerializer)

        super().__init__(*args, **kwargs)

        self.instances = []
        self.validators.append(MultipleUniqueValidator())
        self.lookup_fields = self.child.lookup_fields

    def to_internal_value(self, data):
        # copied from rest framework sources
        if not isinstance(data, list):
            message = self.error_messages['not_a_list'].format(input_type=type(data).__name__)
            raise ValidationError({api_settings.NON_FIELD_ERRORS_KEY: [message]}, code='not_a_list')

        # copied from rest framework sources
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

    def save_child(self, instance, validated_data):
        setattr(self.child, '_errors', [])
        setattr(self.child, '_validated_data', validated_data)
        setattr(self.child, 'instance', instance)
        return self.child.save()

    def save(self, **kwargs):
        """pass validated data in kwargs if this list serializer is child of some other serializer"""
        children = []

        if self.root != self:
            validated_data = kwargs['validated_data']
        else:
            validated_data = self.validated_data

        for item, instance in zip(validated_data, self.instances):
            children.append(self.save_child(instance, item))

        return children


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
