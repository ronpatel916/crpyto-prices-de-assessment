import subprocess
import logging

logging.basicConfig(level=logging.INFO)


def run_task(script_name):
    try:
        logging.info(f"Running {script_name}")
        subprocess.run(["python", script_name],check=True)
    except Exception as e:
        logging.error(f"Error executing {script_name}: {e}")
        raise

def main():
    scripts = [
        'task1_fetch_coin_universe.py',
        'task2_process_pricing_data.py',
        'task3_performance_analysis.py',
        'task4_average_performance.py'
    ]

    for script in scripts:
        run_task(f"scripts/{script}")


if __name__ == '__main__':
    main()