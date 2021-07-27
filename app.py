import os
import psutil
import csv
from datetime import datetime
from dotenv import dotenv_values

config = dotenv_values('{path}/.env'.format(path=os.getcwd()))

def getServerStatus():
    disk_usage = psutil.disk_usage('/')
    cpu_total = psutil.cpu_count(True)
    cpu_precent = psutil.cpu_percent(percpu=True, interval=int(config['interval']))
    cpu_times = psutil.cpu_times(percpu=True)
    virtual_memory = psutil.virtual_memory()
    cpu_status = {
        'date': datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
        'cpu_total': cpu_total,
        'disk_total_space':  int(getattr(disk_usage, 'total')) // 1000**3,
        'disk_total_usage': int(getattr(disk_usage, 'used')) // 1000**3,
        'disk_total_free': int(getattr(disk_usage, 'free')) // 1000**3,
        'disk_usage_percent': float(getattr(disk_usage, 'percent')),
        'memory_total': int(getattr(virtual_memory, 'total')) // 1000**3,
        'memory_available': int(getattr(virtual_memory, 'available')) // 1000**3
    }
    for i in range(len(cpu_precent)):
        cpu_status['cpu_usage_core_{index}'.format(index=i)] = cpu_precent[i]
    for i in range(len(cpu_times)):
        cpu_status['cpu_user_active_times_core_{index}'.format(index=i)] = getattr(cpu_times[i], 'user') // 60
        cpu_status['cpu_idle_times_core_{index}'.format(index=i)] = getattr(cpu_times[i], 'idle') // 60
        cpu_status['cpu_system_active_times_core_{index}'.format(index=i)] = getattr(cpu_times[i], 'system') // 60

    if os.path.exists(os.path.abspath('{path}{name}_{date}.csv'.format(name=config['log_name'], path=config['abs_path'], date=datetime.now().strftime('%m-%d-%Y')))):
        with open(os.path.abspath('{path}{name}_{date}.csv'.format(name=config['log_name'], path=config['abs_path'], date=datetime.now().strftime('%m-%d-%Y'))), 'a') as file:
            w = csv.DictWriter(file, cpu_status.keys())
            w.writerow(cpu_status)
    else:
         with open(os.path.abspath('{path}{name}_{date}.csv'.format(name=config['log_name'], path=config['abs_path'], date=datetime.now().strftime('%m-%d-%Y'))), 'w') as file:
            w = csv.DictWriter(file, cpu_status.keys())
            w.writeheader()
            w.writerow(cpu_status)
            

def main():
    count = int(60 / int(config['interval']))
    for i in range(count):
        getServerStatus()

main()