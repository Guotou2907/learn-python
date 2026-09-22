ans = 59
times = 10
print(f"我们来玩一个猜数游戏，范围为1-100，你拥有{times}次机会")
for i in range(times):
    guess = int(input("请输入你猜的数字:"))
    if guess == ans:
        print("猜对啦")
        break
    elif guess > ans:
        print("太大了")
    else:
        print("太小了")

print("游戏结束")
