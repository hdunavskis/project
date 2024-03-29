# Nordigen Project
The project includes official [**Nordigen Python**](https://github.com/nordigen/nordigen-python) library
as well as [**Nordigen Bank UI**](https://github.com/nordigen/nordigen-bank-ui) library.

## Information and Assumptions
This project is for demonstration purposes only.  
- All errors are handled as 404 for demonstration purposes  
- The gathered data from APIs is cached and not stored in a database. The cache timeout value is set to 900s (5min)  
- Basic user interface is in place to display the data 
- The information displayed back to a user is randomly chosen  
- Datatables is used to show the information, and no additional UI is used  
- Account data is gathered asynchronously using celery  
- The project includes 'Typehints'
- Use localserver to run the project

## Requirements
- Nordigen account to set up *__NORDIGEN_SECRET_ID__*, *__NORDIGEN_SECRET_KEY__* and *__DJANGO_SECRET_KEY__*  
- Access to Nordigen premium products
- Python >=3.8
- Redis-server

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
