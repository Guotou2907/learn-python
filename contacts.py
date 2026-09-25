address_book = []
print("欢迎使用通讯录程序，添加联系人请按1，查找联系人请按2，遍历联系人请按3，退出程序请按q")
while True:
    command = input()
    if command == "q":
        print("通讯录已关闭")
        break
    elif command == "1":
        name = input("请输入联系人的名字：")
        number = input("请输入联系人的号码：")
        person = {
            "name":name,
            "number":number
        }
        address_book.append(person)
        print("添加成功，请进行下一步操作")
    elif command == "2":
        target = input("请输入你想要找到的人的名字：")
        found = False
        for person in address_book:
            if person['name'] == target:
                print(f"你想找的人的电话号码是：{person['number']}")
                found = True
                break
        if not found:
            print("查无此人")
        print("请进行下一步操作")
    elif command == "3":
        for person in address_book:
            print(f"{person['name']}的电话号码是{person['number']}")
        print("请进行下一步操作")
