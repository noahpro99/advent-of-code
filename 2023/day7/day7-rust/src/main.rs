use std::collections::HashMap;

use itertools::Itertools;

pub fn p1(input: &String) -> usize {
    let values: HashMap<&str, usize> = HashMap::from_iter(vec![
        ("A", 13),
        ("K", 12),
        ("Q", 11),
        ("J", 10),
        ("T", 9),
        ("9", 8),
        ("8", 7),
        ("7", 6),
        ("6", 5),
        ("5", 4),
        ("4", 3),
        ("3", 2),
        ("2", 1),
    ]);

    fn hand_value(hand_counts: Vec<usize>) -> usize {
        match hand_counts.as_slice() {
            _ if hand_counts.contains(&5) => 14usize.pow(11),
            _ if hand_counts.contains(&4) => 14usize.pow(10),
            _ if hand_counts.contains(&3) && hand_counts.contains(&2) => 14usize.pow(9),
            _ if hand_counts.contains(&3) => 14usize.pow(8),
            _ if hand_counts.contains(&2) && hand_counts.len() == 3 => 14usize.pow(7),
            _ if hand_counts.contains(&2) => 14usize.pow(6),
            _ => 0,
        }
    }

    input
        .split("\n")
        .into_iter()
        .map(|line| line.split_whitespace().collect_tuple().unwrap())
        .map(|(h, b)| (h.chars(), b.parse::<u32>().unwrap()))
        .map(|(h, b)| {
            (
                h.clone()
                    .rev()
                    .enumerate()
                    .map(|(i, c)| values.get(&c.to_string()[..]).unwrap() * 14usize.pow(i as u32)),
                h.clone()
                    .sorted()
                    .dedup()
                    .map(|c| h.clone().filter(|c2| c2 == &c).count())
                    .collect_vec(),
                b,
            )
        })
        .map(|(ct, ht, b)| (hand_value(ht) + ct.sum::<usize>(), b))
        .sorted_by(|(h, _), (h2, _)| Ord::cmp(&h, &h2))
        .enumerate()
        .map(|(i, (_, b))| (i + 1) * b as usize)
        .sum()
}

pub fn main() {
    let input = std::fs::read_to_string("d7.txt").unwrap();
    let p1 = p1(&input);
    // assert_eq!(p1, 1);
    println!("Day 4 Part 1: {}", p1);
}
