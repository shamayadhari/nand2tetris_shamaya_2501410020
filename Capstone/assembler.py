import sys
import os

# Hack Assembly instruction tables

DEST = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

JUMP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101"
}

print("Hack Assembler started!")

# Predefined Hack symbols
def create_symbol_table():
    symbols = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576
    }

    # Add R0 to R15
    for i in range(16):
        symbols[f"R{i}"] = i

    return symbols

def first_pass(lines):
    symbols = create_symbol_table()
    rom_address = 0
    defined_labels = set()

    for line in lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]

            if label in defined_labels:
                print(f"Warning: Duplicate label '{label}' detected!")
            else:
                defined_labels.add(label)

                if label in symbols:
                    print(f"Warning: Label '{label}' conflicts with an existing symbol!")
                else:
                    symbols[label] = rom_address

        else:
            rom_address += 1

    return symbols

def clean_lines(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    cleaned = []

    for line in lines:
        line = line.split("//")[0]
        line = line.strip()

        if line:
            cleaned.append(line)

    return cleaned

def to_binary(value):
    return format(int(value), "016b")


def second_pass(lines, symbols):
    machine_code = []
    next_variable = 16

    for line in lines:

        if line.startswith("("):
            continue

        if line.startswith("@"):
            symbol = line[1:]

            if symbol.isdigit():
                address = int(symbol)

            elif symbol in symbols:
                address = symbols[symbol]

            else:
                symbols[symbol] = next_variable
                address = next_variable
                next_variable += 1

            machine_code.append(to_binary(address))

        else:
            machine_code.append(convert_c_instruction(line))

    return machine_code
     
def convert_c_instruction(line):

    dest = ""
    jump = ""

    if "=" in line:
        dest, line = line.split("=")

    dest = "".join(c for c in "AMD" if c in dest)

    if ";" in line:
        comp, jump = line.split(";")
    else:
        comp = line

    # Handle equivalent comp expressions
    comp = comp.replace("A+D", "D+A")
    comp = comp.replace("M+D", "D+M")
    comp = comp.replace("A&D", "D&A")
    comp = comp.replace("M&D", "D&M")
    comp = comp.replace("A|D", "D|A")
    comp = comp.replace("M|D", "D|M")

    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]

def assemble(filename):
    lines = clean_lines(filename)

    # Pass 1: Build symbol table
    symbols = first_pass(lines)

    # Pass 2: Generate machine code
    machine_code = second_pass(lines, symbols)

    # Create output filename
    output_file = os.path.splitext(filename)[0] + ".hack"

    with open(output_file, "w") as file:
        for instruction in machine_code:
            file.write(instruction + "\n")

    print(f"Successfully assembled: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py filename.asm")
    else:
        assemble(sys.argv[1])