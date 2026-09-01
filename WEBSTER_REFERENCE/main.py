"""WEBSTER executable entry point.

Sprint 1 provides a dependency-free CLI so the real system has a verified
launch path before higher-level AI, memory, agent, tool, and UI layers are added.
"""

from __future__ import annotations

from core.application import WebsterApplication


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
    main()
