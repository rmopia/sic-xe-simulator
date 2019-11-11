
assignments = ["RESW", "WORD", "RESB", "BYTE"]


def pass1(loc, new_content):
    # TODO: ASSIGN REQUIRED VALUES TO VARIABLES
    pass1_dict = {}
    counter = 0
    # print(loc)
    # print(new_content)
    for item in new_content:
        if "START" in item:
            counter -= 1
        elif bool(set(item).intersection(assignments)) or len(item) == 3:
            pass1_dict[item[0]] = loc[counter]
        counter += 1

    return pass1_dict


def find_pc(loc, new_content):
    pc_dict = {}
    counter = 0
    # TODO add limiter to skip final item that isn't an END or assignment line
    for item in new_content:
        if "START" in item or "END" in item or "BASE" in item:
            pass
        elif bool(set(item).intersection(assignments)):
            pass
        else:
            pc_dict[' '.join(item)] = loc[counter]
        counter += 1
    return pc_dict


def find_addr(loc, new_content):
    addr_dict = {}
    counter = 0
    for item in new_content:
        if "START" in item or "END" in item or "BASE" in item:
            pass
        elif bool(set(item).intersection(assignments)):
            pass
        else:
            addr_dict[' '.join(item)] = loc[counter - 1]
        counter += 1
    return addr_dict
