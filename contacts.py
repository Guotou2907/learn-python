import json
try:
    with open("contacts.json","r",encoding = "utf-8") as f:
        address_book = json.load(f)
except FileNotFoundError:
    address_book = []

def add_contact():
    name = input("请输入联系人的姓名：")
    num = input ("请输入联系人的电话号码：")
    person = {
        "name" : name,
        "num" : num
    }
    address_book.append(person)
    print("添加成功，请进行下一步操作")

def find_contact(target):
    for person in address_book:
        if person["name"] == target:
            return person["name"],person["num"]
    return None,None
def show_contact():
    if not address_book:
        print("通讯录为空")
    else:
        for person in address_book:
            print(f"{person['name']}的电话号码是{person['num']}")

print("欢迎使用通讯录程序，添加联系人请按1，查找联系人请按2，遍历联系人请按3，退出程序请按q")
while True:
    command = input()
    if command == 'q':
        with open("contacts.json","w",encoding = "utf-8") as f:
            json.dump(address_book,f,ensure_ascii = False,indent = 2)
        print("通讯录已关闭")
        break
    elif command == '1':
        add_contact()
    elif command == '2':
        target = input("请输入想要查询的人的名字：")
        found_name,found_number = find_contact(target)
        if found_name:
            print(f"{found_name}的电话号码是{found_number}")
        else:
            print("查无此人")
        print("请进行下一步操作")
    elif command == '3':
        show_contact()
    else:
        print("command not found")
