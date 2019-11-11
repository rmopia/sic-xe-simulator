
import firstpass as fp

format1 = ["FIX", "FLOAT", "HIO", "NORM", "SIO", "TIO"]
format2 = ["ADDR", "COMPR", "DIVR", "MULR", "RMO", "SHIFTL", "SHIFTR", "SUBR", "SVC", "TIXR"]
assignments = ["RESW", "WORD", "RESB", "BYTE"]


def main():
    f = open("sicxe1", "r")
    content = f.readlines()
    f.close()

    new_content = []
    for item in content:
        new_content.append(item.split())

    # print(new_content)

    start_addr = 0x0  # initial address # can change if specified

    if new_content[0]:  # or new_content contains START
        # print(new_content[0][-1])
        if "#" in new_content[0][-1]:
            start_addr = new_content[0][-1].replace("#", "")
        else:
            start_addr = new_content[0][-1]

    # print("starting address: " + '0x' + str(start_addr))
    # print(len(new_content))  # limiter to find this amount of addresses

    loc = [start_addr]
    # print(loc)

    for line in new_content:
        addr(line, loc)

    for item in range(len(loc)):
        if "0x" in loc[item]:
            loc[item] = loc[item].replace("0x", "")

    # print(loc)

    fp_dict = fp.pass1(loc, new_content)
    print(fp_dict)


def addr(line, address_locations):
    # format 4 check
    if "+" in (line[0], line[1]):
        location = int(str(address_locations[-1]), 16) + int('4', 16)
        address_locations.append(hex(location))
    # format 2 check
    elif bool(set(line).intersection(format2)):
        location = int(str(address_locations[-1]), 16) + int('2', 16)
        address_locations.append(hex(location))
    # format 1 check
    elif bool(set(line).intersection(format1)):
        location = int(str(address_locations[-1]), 16) + int('1', 16)
        address_locations.append(hex(location))
    # assignment check
    elif bool(set(line).intersection(assignments)):
        location = int(str(address_locations[-1]), 16) + int(str(line[-1]), 16) * int(3)
        address_locations.append(hex(location))
    elif "START" in line[0] or "END" in line[0]:
        pass
    # format 3
    else:
        location = int(str(address_locations[-1]), 16) + int('3', 16)
        address_locations.append(hex(location))


main()
