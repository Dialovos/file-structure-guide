//! Criterion bench harness. Run with: `cargo bench --bench core_bench`.
//!
//! Benchmarks live in `benches/`; this file is registered in `Cargo.toml`
//! under `[[bench]] name = "core_bench" harness = false` so criterion can
//! drive its own runner instead of libtest.

use criterion::{black_box, criterion_group, criterion_main, Criterion};
use mylib::greet;

fn bench_greet(c: &mut Criterion) {
    c.bench_function("greet world", |b| {
        b.iter(|| greet(black_box("world")))
    });
}

criterion_group!(benches, bench_greet);
criterion_main!(benches);
