import numpy as np

with open("aoc2024/data/day5.txt", encoding="utf-8") as f:
    text = f.read()

rules_txt, updates_txt = text.split("\n\n")
rules = np.array([line.split("|") for line in rules_txt.splitlines()])
updates = [np.array(line.split(",")) for line in updates_txt.splitlines()]


# Part 1
def _follows_rule(rule: np.ndarray, update: np.ndarray) -> bool:
    """Check that the first number in the rule shows up before the second number in the rule in the update."""
    if any(rule_item not in update for rule_item in rule):
        return True
    first_idx, second_idx = [np.where(update == rule_item)[0] for rule_item in rule]
    return first_idx < second_idx


def _follows_all_rules(update: np.ndarray, rules: np.ndarray = rules) -> bool:
    """Check that the update follows all the rules."""
    return all(_follows_rule(rule, update) for rule in rules)


def _middle_item(update: np.ndarray) -> str:
    return update[(update.size - 1) // 2]


sum(int(_middle_item(update)) for update in updates if _follows_all_rules(update))


def fix_update(update: np.ndarray) -> np.ndarray:
    """Fix the update by swapping the first and last elements."""
    while not _follows_all_rules(update):
        for rule in rules:
            if not _follows_rule(rule, update):
                first_idx, second_idx = [
                    np.where(update == rule_item)[0] for rule_item in rule
                ]
                update[first_idx], update[second_idx] = (
                    update[second_idx],
                    update[first_idx],
                )
    return update


# Part 2
sum(
    int(_middle_item(fix_update(update)))
    for update in updates
    if not _follows_all_rules(update)
)
