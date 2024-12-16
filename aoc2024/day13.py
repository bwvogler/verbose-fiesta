"""Button A: X+11, Y+73
Button B: X+65, Y+17
Prize: X=18133, Y=4639
"""

a = (11, 73)
b = (65, 17)
p = (18133, 4639)
[
    3 * a_count + b_count
    for a_count in range((p // b).min())
    for b_count in range((p // a).min())
    if a_count * a + b_count * b == p
]