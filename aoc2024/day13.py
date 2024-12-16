"""Button A: X+11, Y+73
Button B: X+65, Y+17
Prize: X=18133, Y=4639
"""

import numpy as np

a = np.array((11, 73))
b = np.array((65, 17))
p = np.array((18133, 4639))
hunderd = np.array([(100)])
[
    3 * a_count + b_count
    # tuple(a_count * a + b_count * b)
    for a_count in range(np.hstack([(p // b), hunderd]).min())
    for b_count in range((p // a).min())
    if tuple(a_count * a + b_count * b) == tuple(p)
]
