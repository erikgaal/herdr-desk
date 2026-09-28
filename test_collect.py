"""Column rules of collect.place. Run: python3 test_collect.py"""
from collect import place


def card(pr=None, agents=(), **extra):
    return {"repo": "api", "branch": "eng-1-x", "path": "/wt", "pr": pr, "agents": list(agents), **extra}


def pr(**over):
    return {"merged": False, "draft": False, "review": "REVIEW_REQUIRED", "checks": "pass", "conflicts": False,
            "created_days": 0.5, "mergeable": False, **over}


def agent(status, since_days=0.1):
    return {"status": status, "since_days": since_days}


assert place(card(agents=[agent("idle")])) == ("your_move", "waiting for prompt")
assert place(card(agents=[agent("idle", 3)])) == ("your_move", "waiting for prompt, idle 3d")
assert place(card(agents=[agent("idle"), agent("working")]))[0] == "working"
assert place(card(pr(), [agent("idle")])) == ("waiting", None)

assert place(card(pr(review="APPROVED", mergeable=True))) == ("mergeable", None)
assert place(card(pr(review="APPROVED", mergeable=True), [agent("working")]))[0] == "working"
assert place(card(pr(review="APPROVED", mergeable=True), [agent("blocked")])) == ("your_move", "agent needs you")
assert place(card(pr(review="APPROVED", checks="fail"))) == ("your_move", "checks failing")
assert place(card(pr(review="APPROVED"))) == ("waiting", None)

assert place(card(pr(conflicts=True))) == ("your_move", "merge conflicts")
assert place(card(pr(draft=True, created_days=3))) == ("your_move", "draft > 1d")
assert place(card(pr(draft=True, created_days=3, conflicts=True, checks="fail"))) == ("your_move", "draft > 1d · conflicts · CI red")
assert place(card(pr(draft=True, conflicts=True))) == ("waiting", None)
assert place(card(pr(draft=True, conflicts=True, created_days=3), [agent("blocked")])) == ("your_move", "agent needs you")

assert place(card(pr(merged=True))) == ("landed", None)
assert place(card(pr(merged=True), path=None)) == (None, None)
assert place(card()) == (None, None)
assert place(card(todo=True)) == ("todo", None)
print("ok")
