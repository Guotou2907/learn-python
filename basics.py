# 1. 变量与基本数据类型
# Python 不需要声明类型，直接赋值即可
name = "蝈头"           # 字符串 (str)，用单引号或双引号都可以
age = 25                # 整数 (int)
height = 1.75           # 浮点数 (float)
is_student = True       # 布尔值 (bool)，注意 True/False 首字母大写

# 2. 打印输出
# f-string 是格式化字符串，前面加 f，变量用 {} 包起来
print(f"我叫{name}，今年{age}岁，身高{height}米。")
print(f"我是学生吗？{is_student}")

# 3. 查看类型
print(type(name))       # <class 'str'>
print(type(age))        # <class 'int'>

# 4. 输入
# input() 会把用户输入的内容当作字符串返回
user_name = input("请输入你的名字：")
print(f"你好，{user_name}！")

# 5. 类型转换
# 如果要算数，必须把字符串转成整数
user_age = input("请输入你的年龄：")
# user_age 目前是字符串，比如 "25"
# int(user_age) 把它转成整数 25
next_year_age = int(user_age) + 1
print(f"明年你就 {next_year_age} 岁了。")

# 6. 注释
# 这是单行注释
"""
这是多行注释
可以写好几行
"""
