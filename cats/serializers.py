from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db import transaction

import datetime as dt

from .models import CHOICES, Achievement, Cat, User


class UserSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'cats')
        ref_name = 'ReadOnlyUsers'


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True, required=False)
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    color = serializers.ChoiceField(choices=CHOICES)
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'achievements', 'owner',
                  'age')
        read_only_fields = ('owner',)

        validators = [
            UniqueTogetherValidator(
                queryset=Cat.objects.all(),
                fields=('name', 'owner'),
                message='У вас уже есть кот с таким именем!'
            )
        ]

    def validate_birth_year(self, value):
        year = dt.date.today().year
        if not (year - 40 < value <= year):
            raise serializers.ValidationError('Проверьте год рождения!')
        return value
    
    def validate(self, data):
        if data.get('color', getattr(self.instance, 'color', None)) == data.get('name', getattr(self.instance, 'name', None)):
            raise serializers.ValidationError(
                'Имя не может совпадать с цветом!')
        return data 

    def get_age(self, obj):
        return dt.date.today().year - obj.birth_year

    def _save_achievements(self, cat, achievements):
        names = [item['name'] for item in achievements]
        if len(names) != len(set(names)):
            raise serializers.ValidationError({'achievements': 'Достижения не должны повторяться.'})
        cat.achievements.set(
            Achievement.objects.get_or_create(name=name)[0] for name in names
        )

    @transaction.atomic
    def create(self, validated_data):
        achievements = validated_data.pop('achievements', [])
        cat = Cat.objects.create(**validated_data)
        self._save_achievements(cat, achievements)
        return cat

    @transaction.atomic
    def update(self, instance, validated_data):
        achievements = validated_data.pop('achievements', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        if achievements is not None:
            self._save_achievements(instance, achievements)
        return instance
