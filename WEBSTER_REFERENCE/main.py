"""WEBSTER executable entry point.

The entry point is package-aware so frozen builds and normal source execution
share the same import path.
"""

from __future__ import annotations

from .core.application import WebsterApplication


def main() -> None:
    app = WebsterApplication()
    app.start()

    print("=" * 60)
    print("                         WEBSTER")
    print("             Artificial Intelligence Platform")
    print("=" * 60)
    print(f"\nWEBSTER {app.VERSION} started successfully.")
    print("Type 'help' for commands. Type 'exit' to quit.\n")

    while app.status()["running"]:
        try:
            command = input("webster> ")
        except (EOFError, KeyboardInterrupt):
            print("\nShutting down...")
            app.stop()
            break

        response = app.command(command)
        print(response)


if __name__ == "__main__":
    # Direct execution is intentionally unsupported; use `python -m WEBSTER_REFERENCE.main`
    # so package-relative imports remain valid.
    raise SystemExit("Run WEBSTER with: python -m WEBSTER_REFERENCE.main")
