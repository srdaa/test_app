Ручки:

GET /docs/ - Документация Swagger

POST /items/ - Создание предмета. Возвращает ID предмета

GET /items/<id> - Возвращает страницу с предметом и кнопкой buy

POST /orders/ - Создание заказа. Возвращает ID заказа

GET /orders/<id> - Возвращает страницу с заказом и кнопкой buy 

GET /buy/orders/<id> - Возвращает session id для оплаты

GET /buy/items/<id> - Возвращает session id для оплаты

В админке 3 модели.

Для запуска понадобится docker и docker compose. 

make dev - запуск контейнеров

make dev - down удаление контейнеров

make dev-logs - логи контейнера
