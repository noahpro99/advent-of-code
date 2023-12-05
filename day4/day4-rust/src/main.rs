use std::{collections::{HashMap, HashSet}, fmt::Debug};

fn main() {
    let input = std::fs::read_to_string("d4.txt").unwrap();
    let p1: u32 = input
        .lines()
        .map(|x| {
            x.split(": ").collect::<Vec<&str>>()[1]
                .split(" | ")
                .collect::<Vec<&str>>()
                .iter()
                .map(|x| HashSet::from_iter(x.split_whitespace()))
                .collect::<Vec<HashSet<&str>>>()
                .into_iter()
                .reduce(|acc, x| acc.intersection(&x).cloned().collect::<HashSet<&str>>())
                .unwrap()
                .len()
        })
        .map(|x| if x == 0 { 0 } else { 2u32.pow(x as u32 - 1) })
        .sum();
    dbg!(p1);

    // let p2 = input.lines().enumerate().fold(
    //     HashMap::new(),
    //     |mut acc: HashMap<&str, HashSet<&str>>, (i, x)| {
    //         let count = x.split(": ").collect::<Vec<&str>>()[1]
    //             .split(" | ")
    //             .collect::<Vec<&str>>()
    //             .iter()
    //             .map(|x| HashSet::from_iter(x.split_whitespace()))
    //             .collect::<Vec<HashSet<&str>>>()
    //             .into_iter()
    //             .reduce(|acc, x| acc.intersection(&x).cloned().collect::<HashSet<&str>>())
    //             .unwrap()
    //             .len();
    //         (0..count).for_each(|_| {
    //             acc.entry(_).
    //         });
    //         acc.insert(i, count);
    //             acc
    //     },
    // );

}
