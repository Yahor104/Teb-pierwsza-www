import sys

def build_jumps(code):
    stack = []
    jumps = {}
    for i, c in enumerate(code):
        if c == '[':
            stack.append(i)
        elif c == ']':
            start = stack.pop()
            jumps[start] = i
            jumps[i] = start
    return jumps

def run(code):
    tape = [0] * 30000
    ptr = 0
    i = 0
    jumps = build_jumps(code)

    while i < len(code):
        cmd = code[i]

        if cmd == '>':
            ptr += 1
        elif cmd == '<':
            ptr -= 1
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.':
            sys.stdout.write(chr(tape[ptr]))
        elif cmd == ',':
            c = sys.stdin.read(1)
            tape[ptr] = ord(c) if c else 0
        elif cmd == '[' and tape[ptr] == 0:
            i = jumps[i]
        elif cmd == ']' and tape[ptr] != 0:
            i = jumps[i]

        i += 1

if __name__ == "__main__":
    filename = "program.bf"
    try:
        with open(filename, "r") as f:
            code = f.read()
        print(f"=== Запуск {filename} ===\n")
        run(code)
        print("\n=== Программа завершена ===")
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")

    # Ждём, пока пользователь нажмёт Enter, чтобы окно не закрылось
    input("\nНажмите Enter для выхода...")
