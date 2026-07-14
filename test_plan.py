from workflow.nodes import _build_plan_by_rules

# Test: needs browser + match
msg = "帮我找深圳AI Agent岗位并匹配"
plan = _build_plan_by_rules(msg)
for t in plan:
    print(f"  id={t['id']} name={t['name']} agent={t['agent']} depends={t['depends']}")

# Validate depends
all_ids = {t["id"] for t in plan}
for t in plan:
    for d in t["depends"]:
        assert d in all_ids, f"BAD DEPENDENCY: {t['id']} depends on {d} which doesn't exist!"
print("All deps valid!")
