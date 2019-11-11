
assignments = ["RESW", "WORD", "RESB", "BYTE"]


def pass1(loc, new_content):
    # TODO: ASSIGN REQUIRED VALUES TO VARIABLES
    pass1_dict = {}
    counter = 0
    print(loc)
    print(new_content)
    for item in new_content:
        if "START" in item:
            counter -= 1
        elif bool(set(item).intersection(assignments)) or len(item) == 3:
            pass1_dict[item[0]] = loc[counter]
        counter += 1

    return pass1_dict
