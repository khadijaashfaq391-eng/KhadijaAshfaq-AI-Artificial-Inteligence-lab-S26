print("Dynamic Calculator")

while True:
    print("Choose operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")

    choice = input("Enter choice (1-5): ")

    if choice == '5':
        print("Calculator closed")
        break

    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if choice == '1':
        result = num1 + num2
        print("Result =", result)

    elif choice == '2':
        result = num1 - num2
        print("Result =", result)

    elif choice == '3':
        result = num1 * num2
        print("Result =", result)

    elif choice == '4':
        if num2 != 0:
            result = num1 / num2
            print("Result =", result)
        else:
            print("Error: Cannot divide by zero")

    else:
        print("Invalid choice")