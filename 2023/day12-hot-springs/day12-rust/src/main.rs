use itertools::Itertools;
use std::collections::HashMap;

fn combos(p: &str, n: &[usize], cache: &mut HashMap<(Box<str>, Box<[usize]>), u64>) -> u64 {
    if p.is_empty() {
        return if n.is_empty() { 1 } else { 0 };
    }
    if n.is_empty() {
        return if !p.contains('#') { 1 } else { 0 };
    }

    let key = (p.into(), n.into());
    if let Some(&c) = cache.get(&key) {
        return c;
    }

    let mut count = 0;
    if p.starts_with(|c| c == '.' || c == '?') {
        count += combos(&p[1..], n, cache);
    }
    if p.starts_with(|c| c == '#' || c == '?') {
        if n[0] <= p.len()
            && !p[..n[0]].contains('.')
            && (n[0] == p.len() || p.chars().nth(n[0]) != Some('#'))
        {
            count += combos(
                if n[0] == p.len() {
                    ""
                } else {
                    &p[(n[0] + 1)..]
                },
                &n[1..],
                cache,
            );
        }
    }
    cache.insert(key, count);
    count
}

fn main() {
    let mut cache = HashMap::new();
    let file: String = std::env::args()
        .collect::<Vec<String>>()
        .get(1)
        .expect("No file given")
        .to_string();
    let input = std::fs::read_to_string(file).expect("Something went wrong reading the file");
    let parsed = input
        .lines()
        .map(|line| {
            line.split_whitespace()
                .collect_tuple::<(&str, &str)>()
                .unwrap()
        })
        .map(|(p, n)| {
            (
                p.to_string(),
                n.split(",")
                    .map(|s| s.parse::<usize>().unwrap())
                    .collect_vec(),
            )
        });

    let p1_combos = parsed.clone().map(|(p, n)| combos(&p, &n, &mut cache));
    let p1 = p1_combos.sum::<u64>();
    println!("Part 1: {}", p1);

    let p2_combos = parsed
        .clone()
        .map(|(p, n)| {
            (
                (p.clone() + "?").repeat(4) + &p,
                n.iter().cycle().take(5 * n.len()).cloned().collect_vec(),
            )
        })
        .map(|(p, n)| combos(&p, &n, &mut cache));

    let p2 = p2_combos.sum::<u64>();
    println!("Part 2: {}", p2);
}
