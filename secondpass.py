
import numpy as np

format1 = ["FIX", "FLOAT", "HIO", "NORM", "SIO", "TIO"]
format2 = ["ADDR", "COMPR", "DIVR", "MULR", "RMO", "SHIFTL", "SHIFTR", "SUBR", "SVC", "TIXR"]
assignments = ["RESW", "WORD", "RESB", "BYTE"]
OPTAB = {"ADD": "18", "LDA": "00", "LDX": "04", "STA": "0C", "COMPR": "A0", "JLT": "38"}

sp_dict = {}
sp_list = []


def pass2(loc, new_content, fp_dict, pc_dict, addr_dict):
    # TODO distinguish format, opcode, nixbpe (flags), disp/addr

    print(loc)
    print(new_content)
    print(fp_dict)
    print(pc_dict)
    print(addr_dict)

    base_dict = {"BASE": None}

    for item in new_content:
        if "BASE" in item:
            base_dict["BASE"] = item[-1]

    for item in new_content:
        print(item)
        # TODO find format 1-4, START, ENDS, ASSIGNMENTS & BASE
        if "+" in item[0]:
            print("format 4")
        elif bool(set(item).intersection(format2)):
            print("format 2")
        elif bool(set(item).intersection(format1)):
            print("format 1")
        elif bool(set(item).intersection(assignments)):  # we don't want object code for assignments
            pass
        elif "START" in item or "END" in item:  # we also don't want object code for START & END
            pass
        else:
            format3(item, base_dict, fp_dict, pc_dict, addr_dict)


def format3(item, base_dict, fp_dict, pc_dict, addr_dict):
    if len(item) == 3:
        op_code = OPTAB[item[1]]
    else:  # len(item) = 2
        op_code = OPTAB[item[0]]
    print(op_code)

    flags = {"n": 0, "i": 0, "x": 0, "b": 0, "p": 0, "e": 0}
    if "#" in item[-1]:
        flags["n"], flags["i"] = 0, 1
    elif "@" in item[-1]:
        flags["n"], flags["i"] = 1, 0
    else:
        flags["n"], flags["i"] = 1, 1  # we're ruling out that we don't want sic instances (ni = 00)

    if ",x" in item[-1] or ",X" in item[-1]:  # not sure if capitalization matters - yet
        flags["x"] = 1

    flags["b"], flags["p"], flags["e"] = 0, 1, 0

    if bool(base_dict["BASE"]):  # if not empty # TODO fix this so if the 12+ bits in disp, base is applied
        flags["b"], flags["p"], flags["e"] = 1, 0, 0

    # since this is format 3, can never have e = 1
    # TODO make a base flag and/or base dictionary to remember what variable is a base: thus if their is a
    #  base and if our disp/addr doesn't fit in 12 bits then use base
    flags["b"], flags["p"], flags["e"] = 0, 1, 0

    st = [str(i) for i in list(flags.values())]
    flag_string = ''.join(st)

    print(flag_string)
    s = ' '.join(item)
    # print(s)

    disp = 0

    if flag_string == '110000':
        # disp = TA
        print("op c")
    elif flag_string == '110010':  # JLT LOOP tests 2's compliment!
        # disp = TA - PC
        print("TA: " + fp_dict[item[-1]])
        print("PC: " + pc_dict[s])
        TA = int(fp_dict[item[-1]], 16)
        PC = int(pc_dict[s], 16)
        res = TA - PC
        print(hex(res))
        print(np.binary_repr(res, 12))
        disp = np.binary_repr(res, 12)

        print("op m")
    elif flag_string == '110100':
        print("op m")
    elif flag_string == '111000':
        print("op c,x")
    elif flag_string == '111010':
        print("op m,x")
    elif flag_string == '111100':
        print("op m,x")
    elif flag_string == '100000':
        print("op @c")
    elif flag_string == '100010':
        print("op @m")
    elif flag_string == '100100':
        print("op @m")
    elif flag_string == '010000':
        print("op #c")
    elif flag_string == '010010':
        print("op #m")
    elif flag_string == '010100':
        print("op #m")
