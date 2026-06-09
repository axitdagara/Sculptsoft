

import logging

logging.basicConfig(level=logging.DEBUG)

from tasks import add, send_email, risky_task

print("=" * 55)
print("  TASKS SUBMIT ")
print("=" * 55)



task_1 = add.delay(10, 25)
print(f"\n[App] Task 1 : add(10, 25)")
print(f"      Task ID: {task_1.id}")
print(f"      Moving forward — NOT WAITING!")


task_2 = send_email.delay("rahul@example.com", "Welcome to our app!")
print(f"\n[App] Task 2 : send_email(...)")
print(f"      Task ID: {task_2.id}")


task_3 = risky_task.delay(42)      
task_4 = risky_task.delay(-5)      
print(f"\n[App] Task 3 sent: risky_task(42)  — this will succeed")
print(f"[App] Task 4 sent: risky_task(-5)  — this will fail!")


print("\n" + "=" * 55)
print("  CHECKING RESULTS...")
print("  (.get() = waiting for the worker)")
print("=" * 55)


result_1 = task_1.get(timeout=15)
print(f"\n[App] Task 1 result: 10 + 25 = {result_1}")


result_2 = task_2.get(timeout=15)
print(f"[App] Task 2 result: {result_2}")

result_3 = task_3.get(timeout=15)
print(f"[App] Task 3 result: {result_3}")


try:
    result_4 = task_4.get(timeout=15)
except Exception as e:
    print(f"[App] Task 4 FAILED (expected): {e}")


print("\n" + "=" * 55)
print("  DONE! All tasks completed.")
print("=" * 55)
