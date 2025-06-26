#!/usr/bin/env python3
"""Sample Python file for testing compression."""

def hello_world():
    """Print hello world message."""
    print("Hello, World!")
    return "Hello, World!"

def fibonacci(n):
    """Calculate fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    """Main function."""
    hello_world()
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")

if __name__ == "__main__":
    main()
