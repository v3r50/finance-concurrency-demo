use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, Instant};

use indicatif::{ProgressBar, ProgressStyle};

// ================= Stałe (grosze) =================
const START_BALANCE: i64 = 100_000;
const WITHDRAW_AMT: i64 = 70_000;

// Domyślne parametry eksperymentu
const DEFAULT_TRIALS: usize = 20_000;
const DEFAULT_THREADS: usize = 2;
const DEFAULT_OPS_PER_THREAD: usize = 1;

// ================= CLI parsing (bez deps) =================
fn arg_usize(name: &str, default: usize) -> usize {
    let mut it = std::env::args().skip(1);
    while let Some(a) = it.next() {
        if a == name {
            return it
                .next()
                .unwrap_or_default()
                .parse::<usize>()
                .unwrap_or(default);
        }
    }
    default
}

// ================= Core =================
fn withdraw_locked(balance: Arc<Mutex<i64>>, ops_per_thread: usize) {
    for _ in 0..ops_per_thread {
        let mut guard = balance.lock().expect("mutex poisoned");
        if *guard >= WITHDRAW_AMT {
            *guard -= WITHDRAW_AMT;
        }
        // guard drop -> unlock
    }
}

fn run_trial(threads: usize, ops_per_thread: usize) -> i64 {
    let balance = Arc::new(Mutex::new(START_BALANCE));
    let mut handles = Vec::with_capacity(threads);

    for _ in 0..threads {
        let b = Arc::clone(&balance);
        handles.push(thread::spawn(move || withdraw_locked(b, ops_per_thread)));
    }

    for h in handles {
        h.join().expect("thread panicked");
    }

    let final_balance = {
        let guard = balance.lock().expect("mutex poisoned");
        *guard
    };
    final_balance
}

// ================= Stats =================
fn main() {
    let trials = arg_usize("--trials", DEFAULT_TRIALS);
    let threads = arg_usize("--threads", DEFAULT_THREADS);
    let ops = arg_usize("--ops", DEFAULT_OPS_PER_THREAD);

    println!("=== MUTEX STATS (Rust) ===");
    println!(
        "start={} ({} PLN), withdraw={} ({} PLN)",
        START_BALANCE,
        START_BALANCE as f64 / 100.0,
        WITHDRAW_AMT,
        WITHDRAW_AMT as f64 / 100.0
    );
    println!("trials={}, threads={}, ops/thread={}", trials, threads, ops);
    println!();

    // Progress bar
    let pb = ProgressBar::new(trials as u64);
    pb.set_style(
        ProgressStyle::with_template(
            "{spinner:.green} [{elapsed_precise}] {bar:40.cyan/blue} {pos}/{len} ETA {eta_precise} {msg}",
        )
        .unwrap(),
    );
    pb.set_message("running trials");
    pb.enable_steady_tick(Duration::from_millis(120));

    let t0 = Instant::now();

    let mut broken = 0usize;
    let mut outcomes: HashMap<i64, usize> = HashMap::new();

    for _ in 0..trials {
        let final_balance = run_trial(threads, ops);

        *outcomes.entry(final_balance).or_insert(0) += 1;
        if final_balance < 0 {
            broken += 1;
        }

        pb.inc(1);
    }

    pb.finish_with_message("done");

    println!("\nTime: {:.3?}", t0.elapsed());
    println!("Invariant broken (final < 0): {}", broken);
    println!(
        "Broken rate: {:.6}%",
        (broken as f64 / trials as f64) * 100.0
    );

    println!("\nTop outcomes:");
    let mut sorted: Vec<_> = outcomes.into_iter().collect();
    sorted.sort_by_key(|(_, cnt)| std::cmp::Reverse(*cnt));
    for (val, cnt) in sorted.into_iter().take(10) {
        println!("  {:>10} ({:>8.2} PLN): {}", val, val as f64 / 100.0, cnt);
    }

    println!("\nRun examples:");
    println!("  cargo run --bin mutex_stats -- --trials 50000 --threads 4 --ops 10");
    println!("  cargo run --bin mutex_stats -- --trials 20000 --threads 2 --ops 1");
}
