from datetime import datetime, timedelta, time as dt_time
from threading import Event, Thread
import logging


restart_event = Event()
scheduler_stop_event = Event()


def safe_restart(callback):
    if restart_event.is_set():
        logging.info("Restart skipped (already running)")
        return

    restart_event.set()

    logging.info("Calling restart callback...")
    try:
        callback()
    except Exception as e:
        logging.error(f"Error during restart: {e}")
    finally:
        restart_event.clear()


def start_interval_scheduler(interval: float, callback):
    def loop():
        logging.info(f"Interval scheduler started (interval={interval}s)")

        while not scheduler_stop_event.is_set():
            if interval > 0:
                logging.info(f"Waiting {interval} seconds (interval mode)...")

                if scheduler_stop_event.wait(interval):
                    logging.info("Interval scheduler stopped")
                    break

                logging.info("Triggering restart (interval)")
                safe_restart(callback)
            else:
                logging.info("Invalid interval, stopping interval scheduler")
                break

    t = Thread(target=loop, daemon=True)
    t.start()
    return t


def start_time_scheduler(times: list[dt_time], callback):
    def loop():
        logging.info(f"Time scheduler started (times={times})")

        while not scheduler_stop_event.is_set():
            now = datetime.now()
            logging.info(f"Current time: {now}")

            next_runs = []
            for t in times:
                run_dt = datetime.combine(now.date(), t)

                if run_dt <= now:
                    run_dt += timedelta(days=1)

                logging.info(f"Candidate time: {run_dt}")
                next_runs.append(run_dt)

            if not next_runs:
                logging.warning("No scheduled times, stopping time scheduler")
                break

            next_run = min(next_runs)
            wait_seconds = (next_run - now).total_seconds()

            logging.info(f"Next restart at: {next_run}")
            logging.info(f"Waiting {wait_seconds:.2f} seconds (time mode)...")

            if scheduler_stop_event.wait(wait_seconds):
                logging.info("Time scheduler stopped")
                break

            logging.info("Triggering restart (time)")
            safe_restart(callback)

    t = Thread(target=loop, daemon=True)
    t.start()
    return t


def start_restart_schedulers(callback, restart_interval: float = None, restart_time: list[dt_time] = None):
    logging.info("Initializing schedulers...")

    threads = []

    if restart_interval and restart_interval > 0:
        logging.info(f"Enabling interval scheduler: {restart_interval}s")
        threads.append(start_interval_scheduler(restart_interval, callback))
    else:
        logging.info("Interval scheduler disabled")

    if restart_time:
        logging.info(f"Enabling time scheduler: {restart_time}")
        threads.append(start_time_scheduler(restart_time, callback))
    else:
        logging.info("Time scheduler disabled")

    return threads


def stop_restart_schedulers():
    logging.info("Stopping all schedulers...")
    scheduler_stop_event.set()