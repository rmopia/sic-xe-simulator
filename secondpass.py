
import numpy as np

format1 = ["FIX", "FLOAT", "HIO", "NORM", "SIO", "TIO"]
format2 = ["ADDR", "COMPR", "DIVR", "MULR", "RMO", "SHIFTL", "SHIFTR", "SUBR", "SVC", "TIXR"]
assignments = ["RESW", "WORD", "RESB", "BYTE"]
OPTAB = {"ADD": "18", "LDA": "00", "LDS": "6C", "LDX": "04", "STA": "0C", "COMPR": "A0", "JLT": "38", "SUB": "1C",
         "MULR": "98", "FIX": "C4", "FLOAT": "C0", "HIO": "F4", "TIO": "F8", "NORM": "C8", "SIO": "F0"}
registers = {"A": "0", "X": "1", "L": "2", "B": "3", "S": "4", "T": "5"}

sp_dict = {}
sp_list = []


def pass2(loc, new_content, fp_dict, pc_dict):
    # TODO distinguish format, opcode, nixbpe (flags), disp/addr

    obj_code_dict = {}
    print(loc)
    print(new_content)
    print(fp_dict)
    print(pc_dict)

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
            obj_code_dict[item] = OPTAB[item]
        elif bool(set(item).intersection(assignments)):  # we don't want object code for assignments
            pass
        elif "START" in item or "END" in item:  # we also don't want object code for START & END
            pass
        else:
            obj_code = format3(item, base_dict, fp_dict, pc_dict)
            obj_code_dict[' '.join(item)] = obj_code

    print(obj_code_dict)


def format3(item, base_dict, fp_dict, pc_dict):
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

    # print(flag_string)
    s = ' '.join(item)
    # print(s)

    disp = ''

    if flag_string == '110000':
        # disp = TA
        TA = int(fp_dict[item[-1]], 16)
        disp = np.binary_repr(TA, 12)

    elif flag_string == '110010':  # JLT LOOP tests 2's compliment!
        # disp = TA - PC
        # print("TA: " + fp_dict[item[-1]])
        # print("PC: " + pc_dict[s])
        TA = int(fp_dict[item[-1]], 16)
        PC = int(pc_dict[s], 16)
        res = TA - PC
        # print(hex(res))
        # print(np.binary_repr(res, 12))
        disp = np.binary_repr(res, 12)

    elif flag_string == '110100':
        # disp = TA - BASE
        print("op m")
    elif flag_string == '111000':
        # disp = TA - X
        print("op c,x")
    elif flag_string == '111010':
        # disp = TA - PC - X
        print("op m,x")
    elif flag_string == '111100':
        # disp = TA - BASE - X
        print("op m,x")
    elif flag_string == '100000':
        # disp = TA
        addr = str(item[-1]).replace("@", "")
        TA = int(addr, 16)
        # print(np.binary_repr(TA, 12))
        disp = np.binary_repr(TA, 12)
        print("op @c")
    elif flag_string == '100010':
        # disp = TA - PC
        addr = str(item[-1]).replace("@", "")
        TA = int(addr, 16)
        PC = int(pc_dict[s], 16)
        res = TA - PC
        # print(np.binary_repr(res, 12))
        disp = np.binary_repr(res, 12)
        print("op @m")
    elif flag_string == '100100':
        # disp = TA - BASE
        print("op @m")
    elif flag_string == '010000':
        # disp = TA
        val = str(item[-1]).replace("#", "")
        TA = int(val, 16)
        # print(np.binary_repr(TA, 12))
        disp = np.binary_repr(TA, 12)
        print("op #c")
    elif flag_string == '010010':
        # disp = TA - PC
        value = str(item[-1]).replace("#", "")
        TA = int(value, 16)
        PC = int(pc_dict[s], 16)
        # print(TA)
        # print(PC)
        res = TA - PC
        # print(hex(res))
        # print(np.binary_repr(res, 12))
        disp = np.binary_repr(res, 12)
        print("op #m")
    elif flag_string == '010100':
        # disp = TA - BASE
        print("op #m")

    new_op = np.binary_repr(int(op_code, 16), 8)[:-2]
    print(new_op)
    combined_bin = new_op + flag_string + disp
    print(combined_bin)
    print(hex(int(combined_bin, 2)))
    return hex(int(combined_bin, 2))
