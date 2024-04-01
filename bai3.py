import threading

# Function to check if a number is prime
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Function for each thread to find primes in its range
def find_primes(start, end, primes):
    for num in range(start, end):
        if is_prime(num):
            primes.append(num)

# Main function
def main():
    N = int(input("Enter the number N to find primes less than or equal to N: "))
    T = int(input("Enter the number of threads T: "))
    thread_list = []
    primes = []

    # Lock for thread-safe appending to primes list
    lock = threading.Lock()

    # Creating threads
    for i in range(T):
        start = i * (N // T) + 1
        # Ensure the last thread covers the remaining range
        end = N + 1 if i == T - 1 else (i + 1) * (N // T) + 1
        thread = threading.Thread(target=find_primes, args=(start, end, primes))
        thread_list.append(thread)
        thread.start()

    # Waiting for all threads to complete
    for thread in thread_list:
        thread.join()

    # Output the primes found by all threads
    with lock:
        primes.sort()  # Sorting the final list of primes
        print("Primes less than or equal to N:")
        for prime in primes:
            print(prime, end=' ')

if __name__ == "__main__":
    main()
