

from celery import Celery

app = Celery("celery_demo",                        
    broker="redis://localhost:6379/0",    
    backend="redis://localhost:6379/0",  
    include=['tasks']
)

app.conf.result_expires = 600
