use std::sync::{Arc, Mutex};
use std::thread;

const START_BALANCE: i32 = 100_000; // grosze
const WITHDRAW_AMT: i32 = 70_000;   // grosze

fn withdraw_locked(balance: &Arc<Mutex<i32>>, amount: i32) {
    let mut guard = balance.lock().expect("mutex poisoned");
    if *guard >= amount {
        *guard -= amount;
    }
}

fn main() {
    let balance = Arc::new(Mutex::new(START_BALANCE));

    let b1 = Arc::clone(&balance);
    let t1 = thread::spawn(move || withdraw_locked(&b1, WITHDRAW_AMT));

    let b2 = Arc::clone(&balance);
    let t2 = thread::spawn(move || withdraw_locked(&b2, WITHDRAW_AMT));

    t1.join().expect("thread 1 panicked");
    t2.join().expect("thread 2 panicked");

    let final_balance = *balance.lock().expect("mutex poisoned");
    println!("final balance = {}", final_balance);

    // Invariant: przy dwóch wypłatach po 70_000 z 100_000 nie może być < 0
    // (bo lock zapewnia, że check-then-act jest atomowe jako sekcja krytyczna).
    if final_balance < 0 {
        panic!("Invariant broken: final_balance < 0 (this should never happen with Mutex)");
    }
}
