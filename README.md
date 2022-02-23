Тестовое задания для Komtek, суть задания лежит в файле task.md

Реализация:

1. Классическая панель администратора с возможностью просмотра и добавления справочников и элементов.
доступна по url роуту "admin/"

2. Реализация REST API.

1) Получение списка справочников
роут "api/v1/spravochniks/"

Выводит все экзмепляры справочников

2) Получение списка справочников, актуальных на указанную дату
роут "api/v1/spravochniks-actual/<my_date:date>"

Включает в себя динамический параметр <date> вида dd-mm-yyyy, с кастомным конвертером даты.

Выводит все экзмепляры справочников, актуальных на указанную дату
  
3) Получение элементов заданного справочника указанной/текущей версии
роут "api/v1/elements-by-version/"
  
Требует передачи параметров GET запроса вида "?short_title=<short_title>&version=<version>"

Выводит список элементов справочника с указанным <short_title> 
Если <version> указана, то выбирается справочник указанной версии
В противном случае, выбирается справочник актуальной версии
  
4) Валидация нового элемента заданного справочника указанной/текущей версии
роут "api/v1/elements-validation/"
  
Требует передачи POST запроса с json body вида:
  
{
    "spravochnik": {
        "short_title":"<short_title>",
        "version":"<version>"
    },
    "element": {
        "code":"<code>",
        "elem_value":"<elem_value>"
    }
}
  
Проверяет новый элемент на валидность, после чего сохраняет в базу данных.
Если версия <version> не указана, сохраняет элемент для актуальной версии справочника