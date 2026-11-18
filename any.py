try:
    duration = int(input("Enter duration: "))
except ValueError:
    print("Please enter a valid integer.")

try:
    duration = int(input("Enter duration: "))
except duration <= 0:
    print("Please enter a valid integer.")
