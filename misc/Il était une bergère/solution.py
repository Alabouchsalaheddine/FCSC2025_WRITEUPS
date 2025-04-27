#!/usr/bin/env python3
from assembly import assembly

def generate_sqrt_bytecode():
    # Compute x = ⌊√e⌋ via Newton’s method on the VM,
    # with an initial guess x₀ = 1 << ceil(bitlen(e)/2)
    asm = [
        "MOV R1,RB",        # R1 := e
        "MOV R6,#1",        # R6 := 1
        "MOV R5,#1",        # R5 := 1 (for shifts)
        "BTL R4,R1",        # R4 := bitlen(e)
        "ADD R4,R4,R6",     # R4 := bitlen(e) + 1
        "SRL R4,R4,R5",     # R4 := ceil(bitlen/2)
        "SLL R2,R6,R4",     # R2 := 1 << R4  (initial x)

        "loop:",
        "    MOV R4,R1",    #   tmp := e
        "    DIV R4,R4,R2", #   tmp := tmp // x
        "    ADD R4,R2,R4", #   sum := x + tmp
        "    SRL R3,R4,R5", #   new := sum >> 1
        "    CMP R3,R2",    #   compare new vs x
        "    JNCR update",  #   if new < x, update x
        "    MOV R0,R2",    # else result := x
        "    STP",          #      stop

        "update:",
        "    MOV R2,R3",    # x := new
        "    JR loop",      # repeat
    ]
    # assemble and uppercase (for readability)
    return assembly(asm).upper()

if __name__ == "__main__":
    print(generate_sqrt_bytecode())
