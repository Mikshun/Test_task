# Описание проекта
Данный скрипт реализовает запрос вопросов викторины с публичного Api jservice.io и сохраняет их в базу данных.
В случае если в бд уже имеются вопросы, запрашивается дополнительный get запрос к апи до тех пор пока не будет найден уникальный вопрос.
## Инструкция Запуска
+ Скачать репизотрий моно с помощью  команды:
  ```bash
     git clone https://github.com/Mikshun/Test_task
     ```
+ Перейти в корневую папку проект pythonProject2
+ Через терминал запустить команду: docker-compose up
+ После сборки и запуска контейнера перейти по второму ip адресу.
