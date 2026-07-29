import json, sys
sys.stdout.reconfigure(encoding='utf-8')

run_file = "runs/v5_B_group_openrouter_20260729T163707109109.json"

from pathlib import Path
files = sorted(Path("runs").glob("v5_B_group*.json"), reverse=True)
print("Found:", [f.name for f in files])
if files:
    data = json.load(open(files[0], encoding='utf-8'))
    for c in data['results']:
        if not c['result']['passed']:
            print(c['id'])
            print("  ACTUAL:", json.dumps(c['result']['actual_tool_calls'], ensure_ascii=False))
            print("  EXPECT:", json.dumps(c.get('expect'), ensure_ascii=False))
