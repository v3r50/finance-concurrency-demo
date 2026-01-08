from multiprocessing import Process, Value

START_BALANCE = 100_000  # grosze
WITHDRAW_AMT = 70_000    # grosze

def withdraw_naive(balance: Value, amount: int) -> None:
    # check-then-act bez synchronizacji
    if balance.value >= amount:
        balance.value -= amount

def run_once() -> int:
    # lock=False -> celowo brak ochrony
    balance = Value("i", START_BALANCE, lock=False)

    p1 = Process(target=withdraw_naive, args=(balance, WITHDRAW_AMT))
    p2 = Process(target=withdraw_naive, args=(balance, WITHDRAW_AMT))
    p1.start(); p2.start()
    p1.join(); p2.join()

    return balance.value