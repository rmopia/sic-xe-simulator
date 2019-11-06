
def main():
    f = open("sicxe1", "r")
    content = f.readlines()
    f.close()

    new_content = []
    for item in content:
        new_content.append(item.split())

    print(new_content)

    start_addr = 0  # initial address # can change if specified

    if new_content[0]:  # or new_content contains START
        print(new_content[0][-1])
        if "#" in new_content[0][-1]:
            start_addr = new_content[0][-1].replace("#", "")
        else:
            start_addr = new_content[0][-1]

    print(start_addr)
    print(len(new_content))  # limiter to find this amount of addresses

    for line in new_content:
        if len(line) == 2:
            print("2 items")
        elif len(line) == 3:
            print("3 items")

        for element in line:
            if element == "RESW":
                print("pass1")
            else:
                print()


main()
