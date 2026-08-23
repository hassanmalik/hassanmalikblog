from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
checks = sorted((ROOT / "tests").glob("check_*.py"))
failed = []

for check in checks:
    print(f"\n== {check.name} ==")
    result = subprocess.run([sys.executable, str(check)], cwd=ROOT, check=False)
    if result.returncode:
        failed.append(check.name)

if failed:
    print(f"\nFAIL: {len(failed)} check(s): {', '.join(failed)}")
    sys.exit(1)
print(f"\nPASS: {len(checks)} publication checks")
