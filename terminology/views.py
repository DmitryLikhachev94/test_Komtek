from datetime import timedelta

from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from terminology.models import Spravochnik
from terminology.serializers import SpravochnikSerializer, ElementSerializer


class SpravochnikList(generics.ListAPIView):
    """получение списка всех справочников"""

    queryset = Spravochnik.objects.all()
    serializer_class = SpravochnikSerializer


class SpravochnikListActual(generics.ListAPIView):
    """получение списка справочников, актуальных на указанную дату"""

    serializer_class = SpravochnikSerializer

    def get_queryset(self):
        # принимаем дату вида dd-mm-yyyy
        date = self.kwargs.get("date")
        # для каждого справочника выбираем актуальную для указанной даты версию
        a = [i['actual'] for i in Spravochnik.objects
            .filter(date_created__lte=date + timedelta(days=1))
            .values('title')
            .annotate(actual=Max('date_created'))]
        return Spravochnik.objects.filter(date_created__in=a)


class ElementsByVersion(generics.ListAPIView):
    """получение элементов заданного справочника указанной/текущей версии"""

    serializer_class = ElementSerializer

    def get_queryset(self):
        # принимаем параметры запросы
        spravochnik_short_title = self.request.query_params.get('short_title', '')
        spravochnik_version = self.request.query_params.get('version', '')
        if spravochnik_short_title:
            if spravochnik_version:
                # возвращаем список элементов справочника указанной версии
                return get_object_or_404(Spravochnik,
                                         short_title=spravochnik_short_title,
                                         version=spravochnik_version).element_set.all()
            # возвращаем список элементов справочника для актуальной версии
            return Spravochnik.objects.filter(
                short_title=spravochnik_short_title
            ).latest('date_created').element_set.all()


class ElementValidation(APIView):
    """валидация нового элемента заданного справочника указанной/текущей версии"""

    def post(self, request):
        # парсим POST запрос
        element = request.data.get("element", {})
        spravochnik = request.data.get("spravochnik", {})
        spravochnik_short_title = spravochnik.get("short_title", "")
        spravochnik_version = spravochnik.get("version", "")
        # находим нужный справочник по данным запроса
        # либо выдаем сообщение об ошибке
        if spravochnik_short_title:
            try:
                if spravochnik_version:
                    spravochnik = Spravochnik.objects.get(
                        short_title=spravochnik_short_title,
                        version=spravochnik_version)
                else:
                    spravochnik = Spravochnik.objects.filter(
                        short_title=spravochnik_short_title
                    ).latest('date_created')
                element['spravochnik'] = spravochnik.pk
            except:
                return Response('Указанный справочник не существует')
        else:
            return Response('Введите данные о справочнике')
        # если данные о справочнике указаны верно
        # пробуем сохранить элемент в базу данных
        serializer = ElementSerializer(data=element)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Создан новый элемент:": serializer.data})
