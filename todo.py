todo = []
while True:
    item = input("请输入你想要购买的物品，输入完毕后请输入done：")
    if item == "done":
        break
    else:
        todo.append(item)

for item in todo:
    print(f"我需要买{item}")
