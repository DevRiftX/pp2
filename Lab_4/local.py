n = int(input())
massive = list(map(int, input().split()))

count_d = 0
for i in range(3):
    if massive[i] % 2 == 0:
        count_d += 1

count_n = count_d >= 2

for i in range(n):
    if (massive[i] % 2 == 0) != count_n:
        print(i + 1)
        break