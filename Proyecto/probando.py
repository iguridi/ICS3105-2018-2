def rec(assigns, total, i=0):
    if i >= len(assigns):
        # print(assigns)
        # return
        yield assigns
        return
    for j in range(0, total+1):
        # print('hoola')
        yield from rec(assigns[:i] + [j] + assigns[i+1:], total-j, i+1)

gen = rec([0,0,0,0], 7)
print(gen)
for i in gen:
    print(i)