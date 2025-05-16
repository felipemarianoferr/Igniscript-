import os

class Code:
    instructions = []

    def append(instruction):
        Code.instructions.append(instruction)

    def header():
        Code.instructions.append("section .data")
        Code.instructions.append('    format_in: db "%d", 0')
        Code.instructions.append('    format_out: db "%d", 10, 0')
        Code.instructions.append('    cavalos: dd 0')
        Code.instructions.append('    gasolina: dd 100')
        Code.instructions.append('    ligado: dd 0')
        Code.instructions.append('    rpm: dd 0')
        Code.instructions.append('    marcha: dd 0')
        Code.instructions.append('    ref_cavalos: dd 120\n')
        Code.instructions.append("section .text")
        Code.instructions.append("    global _start")
        Code.instructions.append("    extern printf")
        Code.instructions.append("    extern scanf\n")
        Code.instructions.append("_start:")
        Code.instructions.append("    ; Leitura da cavalaria inicial")
        Code.instructions.append("    push cavalos")
        Code.instructions.append("    push format_in")
        Code.instructions.append("    call scanf")
        Code.instructions.append("    add esp, 8\n")

    def footer():
        Code.instructions.append("")
        Code.instructions.append("    mov eax, 1")
        Code.instructions.append("    xor ebx, ebx")
        Code.instructions.append("    int 0x80")

    def dump(filename):
        base_name = os.path.splitext(filename)[0]
        asm_filename = base_name + ".asm"

        with open(asm_filename, 'w') as f:
            for instr in Code.instructions:
                f.write(instr + '\n')
