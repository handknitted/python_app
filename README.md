To run

    export FLASK_APP=base/base.py
    python -m flask run -p 8080
    
To run in uwsgi

    . .venv/bin/activate
    pip install uwsgi
    uwsgi --http 127.0.0.1:8080 --master --module base.base --processes 1
    
To build and run in docker

    docker build -t python_app/base:0.1 .
    docker container run --name=base -d -p=8080:8080 python_app/base:0.1



