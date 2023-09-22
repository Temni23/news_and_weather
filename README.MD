#  News and wether

## О проекте
Тестовое задание по заранее сформированному ТЗ

В данном проекте реализована бэкэнд ресурса поддерживающий публикацию новостей, комментарии к новостям, получение информации о примечательных местах, погоду в этих местах и историю погоды.

Посредством git-actions реализовано тестирование, пересборка докер образов на dockerhub.

## Технологии
Python 3.9, Django, Django REST framework, Docker, Celery, Constance, Pandas, Nginx

## Запуск проекта на локальном компьютере c linux

клонировать проект, например так:
git clone git@github.com:Temni23/foodgram-project-react.git
Вместо пути git@github.com:Temni23/foodgram-project-react.git введите свой.
frontend:
cd frontend
npm i
rpm run dev

backend:
cd backend
python -m venv venv

# Linux/macOS:
```
  source env/bin/activate
  ```
# windows:
  ```
  source venv/Scripts/activate
  ```

```
pip install -r requirements.txt
```
```
python manage.py migrate
```
```
python manage.py runserver
```
При успешном старте получим backend приложение на 127.0.0.1:8080

## Альтернативная установка возможна при установленном на локальном компьютере Docker compose

Запустите проект из корня с помощью команды:
```
docker compose up
```
Соберите статику Django с помощью команды:
```
docker compose exec backend python manage.py collectstatic
```
Скопируйте статику командой:
```
docker compose exec backend cp -r /app/collected_static/. /static/static/
```
По адресу http://127.0.0.1:8080/ сайт будет доступен.


### Автор проекта А.В. Климов

