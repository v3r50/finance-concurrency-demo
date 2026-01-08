from multiprocessing import Process, Value, Lock

START_BALANCE = 100_000
WITHDRAW_AMT = 70_000

def withdraw_locked(balance: Value, amount: int, lock: Lock) -> None:
    with lock:
        if balance.value >= amount:
            balance.value -= amount

def run_once() -> int:
    balance = Value("i", START_BALANCE)  # może mieć własny lock, ale używamy jawnego
    lock = Lock()

    p1 = Process(target=withdraw_locked, args=(balance, WITHDRAW_AMT, lock))
    p2 = Process(target=withdraw_locked, args=(balance, WITHDRAW_AMT, lock))
    p1.start(); p2.start()
    p1.join(); p2.join()

    return balance.value