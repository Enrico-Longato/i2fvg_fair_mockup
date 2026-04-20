"""
Load the processed CSV data into the Django SQLite database.

This wrapper runs Django migrations and then executes the management
command `import_i2fvg_data` from the project located in `../django_project`.
"""

import subprocess
import sys
from pathlib import Path


def main():
    script_dir = Path(__file__).resolve().parent
    django_dir = script_dir.parent / "django_project"
    manage_py = django_dir / "manage.py"

    if not manage_py.exists():
        raise FileNotFoundError(f"manage.py not found: {manage_py}")

    print(f"Using Django project: {django_dir}")
    print("Running: manage.py migrate")
    subprocess.run(
        [sys.executable, str(manage_py), "migrate", "--noinput"],
        cwd=django_dir,
        check=True,
    )

    print("Running: manage.py import_i2fvg_data")
    subprocess.run(
        [sys.executable, str(manage_py), "import_i2fvg_data"],
        cwd=django_dir,
        check=True,
    )


if __name__ == "__main__":
    main()
