# Проект YaCut

## Описание:

Сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Технологии:

* Python 3.10
* Flask 2.0
* SQLAlchemy 1.4

## Установка и запуск:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать БД (через flask shell):

```
>>> from yacut import db
>>> db.create_all()
```

Запустить приложение:

```
flask run
```

## Автор:

### Полшков Михаил