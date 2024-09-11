/*import sys

def average(new_number, current, count, max_count=None):
    if max_count is not None and count > max_count:
        count = max_count
    return current + (new_number - current) / count

def main():
    count = 0
    current = 0.0

    while True:
        count += 1
        new_number = float(count)  # some function to get next new_number here
        current = average(new_number, current, count)

if __name__ == "__main__":
    main()