#!/usr/bin/env python3
import sys
print("Python script started", flush=True)
print(f"Python version: {sys.version}", flush=True)
print(f"Executable: {sys.executable}", flush=True)

# Try to import telegram
try:
    import telegram
    print(f"Telegram imported successfully: {telegram.__version__}", flush=True)
except Exception as e:
    print(f"Failed to import telegram: {e}", flush=True)
    sys.exit(1)

print("Test completed successfully", flush=True)
