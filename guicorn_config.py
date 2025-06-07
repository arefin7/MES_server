# gunicorn_config.py
def when_ready(server):
    from threading import Thread
    from app import mqtt_thread
    Thread(target=mqtt_thread, daemon=True).start()
