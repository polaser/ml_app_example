# ml_app_example
Простой микросервис для развертывания моделей машинного обучения с сохранением отправленных данных и заготовленным логгером действий пользователей

Проект содержит следующие файлы:

- Dockerfile, docker-compose.yml - файлы для развертывания сервиса 
- Creating_model.ipynb - ноутбук с созданной моделью для предсказания стоимости жилья
- model_v2.pk - сериализованная обученая модель
- startservice.sh - shell скрипт, который поднимает данный микросервис
- test_queries.sh - shell скрипт, внутри которого есть пример вызова двух HTTP запросов с помощью утилиты curl
- requirements.txt - файл с описанием необходимых библиотек на python
- *.py - файлы с имплементацией сервиса


Для запуска/тестирования сервиса необходимо:

 1) Установить [docker](https://www.docker.com/get-started "Get started with docker")
 2) Поправить файл startservice.sh: заменить `docker-compose up --no-build` на `docker-compose up --build` *
 3) Запустить скрипт startservice.sh
 4) Запустить скрипт test_queries.sh (если терминал выдаст ошибки со стороны сервера, просьба написать мне на почту: climbest@mail.ru)
 
 Информация о модели: 
  - Модель обучена на датасете [Boston housing prices](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_boston.html#sklearn.datasets.load_boston "Load data") 
  - Модель представляет из себя sklearn реализацию GradientBoostingRegressor со следующими значениями метрик: MSE: 14.9854, MAE: 2.9056, R^2: 0.2079 
  
  Стек: Python3, MongoDB, Flask, Docker, sklearn, jupyter notebook, bash-scripting
  
* При повторном запуске сервиса с помощью этого скрипта необходимо вернуть строку в исходное состояние, чтобы не создавать лишние копии

