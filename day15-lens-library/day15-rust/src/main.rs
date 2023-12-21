use std::collections::HashMap;

fn hash(l: &str) -> i32 {
    l.chars().fold(0, |acc, x| 17 * (acc + x as i32) % 256)
}

fn main() {
    let file: String = std::env::args()
        .collect::<Vec<String>>()
        .get(1)
        .expect("No file given")
        .to_string();
    let input = std::fs::read_to_string(file).expect("Something went wrong reading the file");

    let p1 = input.split(',').map(|x| hash(x)).sum::<i32>();
    println!("Part 1: {}", p1);

    let p2 = input
        .split(',')
        .map(|x| {
            (
                hash(x.split(&['-', '='][..]).next().unwrap()),
                x.split(&['-', '='][..]).next().unwrap(),
                x.contains("="),
                x.split(&['-', '='][..]).last(),
            )
        })
        .fold(
            HashMap::<i32, Vec<(&str, i32)>>::new(),
            |mut hm, (h, st, s, n)| {
                let binding = vec![];
                let b = hm.entry(h).or_insert(binding.clone());
                match s {
                    true => match b.iter().enumerate().find(|(_, x)| x.0 == st) {
                        Some((i, _)) => {
                            b[i] = (st, n.unwrap().parse::<i32>().unwrap());
                        }
                        None => {
                            b.push((st, n.unwrap().parse::<i32>().unwrap()));
                        }
                    },
                    false => {
                        b.retain(|x| x.0 != st);
                    }
                }
                hm
            },
        )
        .iter()
        .map(|(k, v)| {
            v.iter()
                .enumerate()
                .map(|(i, x)| (k + 1) * (i + 1) as i32 * x.1)
                .sum::<i32>()
        })
        .sum::<i32>();
    println!("Part 2: {}", p2);
}
