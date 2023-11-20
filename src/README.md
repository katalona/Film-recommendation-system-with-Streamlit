# Подготовка среды 

* Создадим файл .env с переменными среды
~~~
DISTANCE = assets\distance.csv
MOVIES = assets\movie.csv
API_KEY = <тут должен быть ваш API к OMDB>
~~~

* Переходим в  папку проекта
~~~
cd <project name>
~~~

* Создаем виртуальное окружение
~~~
python -m venv venv
~~~
~~~
.\venv\Scripts\activate
~~~

* Устанавливаем в него необходимые библиотеки
~~~
pip install -r req.txt
~~~


## Запуск сервиса

* Переходим в папку src
~~~
cd src
~~~

* Запускаем Streamlilt
~~~
streamlit run app.py
~~~
