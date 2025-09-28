import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # if file_contents:
    #     raise NotImplementedError("Scanner not implemented")
    # else:
    #     print("EOF  null") # Placeholder, replace this line when implementing the scanner

    for char in file_contents:
        if char == "(":
            print("LEFT_PAREN ( null")
        elif char == ")":
            print("RIGHT_PAREN ) null")

    print("EOF  null")

if __name__ == "__main__":
    main()
