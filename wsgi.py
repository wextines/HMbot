from multiprocessing import Process
import time

def background_task():
    while True:
        print("Фоновая задача выполняется...")
        time.sleep(10)

# Запускаем фоновый процесс
p = Process(target=background_task)
p.start()

def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"Worker is running"]

