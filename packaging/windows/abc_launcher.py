"""Windows launcher for the A+B+C-only WEBSTER executable."""
from WEBSTER_REFERENCE.abc_runtime import ABCApplication

def main():
    app=ABCApplication(); app.start()
    print("="*60); print("WEBSTER • A+B+C BUILD"); print("A: core intelligence | B: Windows desktop | C: local AI"); print("="*60)
    print("Type 'capabilities' for the included scope. Type 'exit' to quit.\n")
    while app.running:
        try: command=input("webster> ")
        except (EOFError,KeyboardInterrupt): app.stop(); break
        try: print(app.command(command))
        except Exception as exc: print(f"Error: {exc}")
if __name__=="__main__": main()
