# Nordigen Project
The project includes official [**Nordigen Python**](https://github.com/nordigen/nordigen-python) library
as well as [**Nordigen Bank UI**](https://github.com/nordigen/nordigen-bank-ui) library.

## Requirements
- Nordigen account to set up *__secret_id__* and *__secret_key__*
- Python >=3.8
- Reds-server

## Set up
1. Create and set up an account with Nordigen and create *__secret id__* and *__secret key__*
2. Install and activate redis-server (default port 6379). For Linux Debian:  
```sudo apt install redis-server```  
3. Start the redis-service  
```sudo systemctl enable redis-server```  
```sudo systemctl start redis-server```  
4. Create and activate venv  
``` python3 -m venv venv_name venv_path```  
``` source venv/venv_name/bin/activate``` 
5. Change directory to the project root directory (where manage.py files is located)
6. Install required pip packages  
``` pip install -r requirements.txt ```  
7. Update .env file. Add *__secret id__* and *__secret key__* from Nordigen website  
8. Start celery  
``` celery -A website worker```  
9. Start local server (default port 8000)  
``` python manage.py runserver --insecure```  
10. Open webbrowser 127.0.0.1:8000
