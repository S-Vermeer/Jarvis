import threading

from plyer import notification
import schedule
import time

directory = r"C:\Users\Public\Documents\Github\Jarvis\PyDa\application"
phillip_image = directory + r"\assets\Phillip_image.ico"

morning_active = False

def morning_message():
    notification.notify(
        title='Morning',
        message='Phillip wishes you a good morning',
        app_icon=phillip_image,
        timeout=10,
    )


def schedule_morning_msg():
    schedule.every().day.at("7:00").do(morning_message)
    run_continuously(1)


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not morning_active:
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


# Start the background thread
stop_run_continuously = run_continuously()


def stop_run_morning():
    global morning_active
    morning_active = True
