import time
from pair_scanner import run_scanner


while True:

    print("\nUpdating scanner...\n")


    result = run_scanner()


    print(
        result.to_string(index=False)
    )


    print("\nNext update in 5 minutes")


    time.sleep(300)
