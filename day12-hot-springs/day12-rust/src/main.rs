use itertools::Itertools;
use regex::Regex;
use std::collections::{HashMap, VecDeque};

fn valid(p: &String, n: Vec<i32>) -> bool {
    let re = Regex::new(r"\#+").unwrap();
    let lengths = re
        .find_iter(p)
        .map(|m| (m.end() - m.start()) as i32)
        .collect_vec();
    n == lengths
}


fn variants(s: &String) -> Vec<String> {
    // if last char is a ? replace it with either a # or a .
    let mut v = Vec::new();
    let mut s = s.clone();
    if s.ends_with("?") {
        s.pop();
        v.push(s.clone() + "#");
        v.push(s + ".");
    } else {
        v.push(s);
    }
    v
}

fn start_is_less_than2(s: &String, n: Vec<i32>, map: &mut HashMap<String, Vec<i32>>) -> bool {
    // get up to the last char of s from the map to get the lengths
    // add the last char of s to the lengths by looking at the last two chars of s ## adds one to last length and .# adds one to last length and adds a new length
    // if all but last lengths are equal to corresponding from n and the last length is less than or equal to the last matching value from n
    if s.len() == 0 {
        return true;
    }
    if s.len() == 1 {
        let lengths = match s.as_str() {
            "#" => vec![1],
            "." => vec![],
            _ => panic!("Invalid string"),
        };
        map.insert(s.clone(), lengths.clone());
        return lengths.len() == 0 || lengths[0] <= n[0];
    }
    let mut lengths = map.get(&s[0..s.len() - 1].to_string()).unwrap().clone();
    let l = lengths.len();
    let last_char = &s[s.len() - 1..s.len()];
    let second_last_char = &s[s.len() - 2..s.len() - 1];
    // dbg!(s, &lengths, &second_last_char, &last_char);
    match (second_last_char, last_char) {
        ("#", "#") => lengths[l - 1] += 1,
        (".", "#") => lengths.push(1),
        (_, ".") => (),
        _ => panic!("Invalid string"),
    };
    map.insert(s.clone(), lengths.clone());

    if lengths.len() == 0 {
        return true;
    } else if lengths.len() == 1 {
        return lengths[0] <= n[0];
    } else if lengths.len() > n.len() {
        return false;
    }
    lengths
        .iter()
        .take(lengths.len() - 1)
        .zip(n.iter())
        .all(|(l, n)| l == n)
        && lengths.last().unwrap() <= &n[lengths.len() - 1]
}

fn combos(p: &String, n: Vec<i32>) -> i32 {
    // take every possible combination of
    let mut map = HashMap::<String, Vec<i32>>::new();
    let mut stack = VecDeque::<String>::new();
    variants(&p[0..1].to_string())
        .iter()
        .for_each(|v| stack.push_back(v.clone()));

    let mut combos = 0;
    while let Some(s) = stack.pop_front() {
        if s.len() == p.len() {
            if valid(&s, n.clone()) {
                combos += 1;
            }
            continue;
        } else if start_is_less_than2(&s, n.clone(), &mut map) {
            // create variants of s with an additional char from p and push them to stack
            let s_plus_one = s.clone() + &p[s.len()..s.len() + 1];
            variants(&s_plus_one)
                .iter()
                .for_each(|v| stack.push_back(v.clone()));
        }
    }
    combos
}

fn main() {
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
                    .map(|s| s.parse::<i32>().unwrap())
                    .collect_vec(),
            )
        });

    // let p1_combos = parsed.clone().enumerate().map(|(i, (p, n))| {
    //     dbg!(i);
    //     combos(&p, n)
    // });
    // let p1 = p1_combos.sum::<i32>();
    // println!("Part 1: {}", p1);

    let p2_combos = parsed
        .clone()
        .map(|(p, n)| {
            // make p itself copied 5 times
            // also do the same for n
            // put a ? between each of the 5 copies of p
            (
                (p.clone() + "?").repeat(4) + &p,
                n.iter().cycle().take(5 * n.len()).cloned().collect_vec(),
            )
        })
        .enumerate()
        .map(|(i, (p, n))| {
            dbg!(i);
            combos(&p, n)
        });

    let p2 = p2_combos.sum::<i32>();
    println!("Part 2: {}", p2);
}
