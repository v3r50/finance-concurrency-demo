use std::thread;

const START_BALANCE: i32 = 100_000; // grosze
const WITHDRAW_AMT: i32 = 70_000;   // grosze

fn main() {
    let mut balance: i32 = START_BALANCE;

    // Dwa wątki próbują zrobić check-then-act na współdzielonym stanie.
    // To jest dokładny odpowiednik idei z python/naive.py, ale Rust to zatrzyma na etapie kompilacji.
    let t1 = thread::spawn(|| {
        if balance >= WITHDRAW_AMT {
            balance -= WITHDRAW_AMT;
        }
    });

    let t2 = thread::spawn(|| {
        if balance >= WITHDRAW_AMT {
            balance -= WITHDRAW_AMT;
        }
    });

    let _ = t1.join();
    let _ = t2.join();

    println!("final balance = {}", balance);
}