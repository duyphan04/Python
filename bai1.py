import threading
import sys

# Global variables to store statistical values
average_value = 0
min_value = float('inf')
max_value = float('-inf')

# Lock to synchronize access to global variables
lock = threading.Lock()

# Function to calculate average value
def calculate_average(numbers):
    global average_value
    with lock:
        average_value = sum(numbers) / len(numbers)

# Function to calculate minimum value
def calculate_minimum(numbers):
    global min_value
    with lock:
        min_value = min(numbers)

# Function to calculate maximum value
def calculate_maximum(numbers):
    global max_value
    with lock:
        max_value = max(numbers)

if __name__ == "__main__":
    # Get numbers from command line arguments
    numbers = [int(arg) for arg in sys.argv[1:]]

    # Create worker threads
    average_thread = threading.Thread(target=calculate_average, args=(numbers,))
    minimum_thread = threading.Thread(target=calculate_minimum, args=(numbers,))
    maximum_thread = threading.Thread(target=calculate_maximum, args=(numbers,))

    # Start the threads
    average_thread.start()
    minimum_thread.start()
    maximum_thread.start()

    # Wait for all threads to finish
    average_thread.join()
    minimum_thread.join()
    maximum_thread.join()

    # Output the results
    print("The average value is", average_value)
    print("The minimum value is", min_value)
    print("The maximum value is", max_value)
