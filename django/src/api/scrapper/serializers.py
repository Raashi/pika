from typing import Type
from collections import Mapping

from django.db import models
from django.db.models import Q

from rest_framework.serializers import ModelSerializer
from rest_framework.fields import empty


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
            self.lookup_field = self.Meta.lookup_field
            if self.lookup_field is None:
                self.lookup_field = self.Meta.model._meta.pk.name

            if instance(self.lookup_field, str):
                self.lookup_field = [self.lookup_field]

            if isinstance(data, Mapping):
                for field in self.lookup_field:
                    assert field in data

                try:
                    instance = self.Meta.model.objects.get(**{field: data[field] for field in self.lookup_field})
                except self.Meta.model.DoesNotExist:
                    pass

        super().__init__(instance, data, **kwargs)

    def updated_related(self, serializers, movie, field='id'):
        objects = []
        for serializer in serializers:
            serializer.validated_data['movie'] = movie
            objects.append(serializer.save())

        if len(objects):
            manager = objects[0].objects
            values = [getattr(obj, field) for obj in objects]
            manager.filter(~Q(**{field + '__in': values})).delete()
