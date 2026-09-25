def logic_function(x1, x2, x3):

    truth_table = "00100100"
    index = (x1 << 2) | (x2 << 1) | x3
    return int(truth_table[index])

print("x1 x2 x3 => result")
for x1 in [0, 1]:
    for x2 in [0, 1]:
        for x3 in [0, 1]:
            result = logic_function(x1, x2, x3)
            print(f" {x1}  {x2}  {x3}  =>   {result}")