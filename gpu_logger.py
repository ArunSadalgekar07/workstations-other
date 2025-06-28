import time
import sys
import os
import logging
from datetime import datetime
from utils.shell_ops import get_gpu_stats, get_user_gpu_usage
from utils.db import insert_gpu_log, insert_user_gpu_log

# Setup logging
def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'gpu_logger.log')),
            logging.StreamHandler(sys.stdout)
        ]
    )

def log_gpu_stats():
    """Get current GPU stats and log them to the database."""
    success, gpu_data = get_gpu_stats()
    if success and isinstance(gpu_data, list):
        for gpu in gpu_data:
            try:
                # Extract correct values from GPU data
                gpu_index = gpu.get('index')
                gpu_name = gpu.get('name')
                utilization = gpu.get('gpu_util', 0)  # Changed from 'utilization' to 'gpu_util'
                memory_used = gpu.get('mem_used', 0)  # Changed from 'memory_used' to 'mem_used'
                
                # Log the values
                insert_gpu_log(
                    gpu_index=gpu_index,
                    gpu_name=gpu_name,
                    utilization=utilization,
                    memory_used=memory_used
                )
                logging.info(f"Logged stats for GPU {gpu_index}: Utilization={utilization}%, Memory={memory_used}MiB")
            except Exception as e:
                logging.error(f"Error logging GPU stats: {str(e)}")
                logging.error(f"GPU data received: {gpu}")  # Added to debug data structure
    else:
        logging.error(f"Failed to get GPU stats: {gpu_data}")

def log_user_gpu_usage():
    """Get current user GPU usage and log it to the database."""
    success, user_data = get_user_gpu_usage()
    if success and isinstance(user_data, list):
        for user in user_data:
            try:
                username = user.get('username')
                gpu_memory_mib = user.get('gpu_memory_mib', 0)
                gpu_memory_percentage = user.get('gpu_memory_percentage', 0)
                
                # Log the values
                insert_user_gpu_log(
                    username=username,
                    gpu_memory_mib=gpu_memory_mib,
                    gpu_memory_percentage=gpu_memory_percentage
                )
                logging.info(f"Logged user GPU usage for {username}: Memory={gpu_memory_mib}MiB ({gpu_memory_percentage}%)")
            except Exception as e:
                logging.error(f"Error logging user GPU usage: {str(e)}")
                logging.error(f"User data received: {user}")  # Added to debug data structure
    else:
        logging.error(f"Failed to get user GPU usage: {user_data}")

def log_all_stats():
    """Log both GPU stats and user GPU usage."""
    log_gpu_stats()
    log_user_gpu_usage()

def main():
    """Main loop to periodically log GPU stats and user GPU usage."""
    setup_logging()
    interval = 300  # 5 minutes in seconds
    
    logging.info("Starting GPU logger...")
    logging.info(f"Logging interval: {interval} seconds")
    logging.info("Logger will run indefinitely until stopped manually")
    
    while True:
        try:
            log_all_stats()
            time.sleep(interval)
        except KeyboardInterrupt:
            logging.info("GPU logger stopped by user.")
            break
        except Exception as e:
            logging.error(f"Error in main loop: {str(e)}")
            time.sleep(interval)

if __name__ == "__main__":
    main() 