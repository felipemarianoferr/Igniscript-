section .data
    format_in: db "%d", 0
    format_out: db "%d", 10, 0
    cavalos: dd 0
    gasolina: dd 100
    ligado: dd 0
    rpm: dd 0
    marcha: dd 0
    ref_cavalos: dd 120

section .text
    global _start
    extern printf
    extern scanf

_start:
    ; Leitura da cavalaria inicial
    push cavalos
    push format_in
    call scanf
    add esp, 8


    mov eax, 1
    xor ebx, ebx
    int 0x80
