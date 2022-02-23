from rest_framework import serializers

from terminology.models import Spravochnik, Element


class SpravochnikSerializer(serializers.ModelSerializer):
    """Класс, сериализирующий данные модели справочников"""

    class Meta:
        model = Spravochnik
        fields = '__all__'


class ElementSerializer(serializers.ModelSerializer):
    """Класс, сериализирующий данные модели элементов"""

    class Meta:
        model = Element
        fields = '__all__'
