use itertools::Itertools;

fn transpose(v: &Vec<String>) -> Vec<String> {
    (0..v[0].len())
        .map(|i| v.iter().map(|r| &r[i..i + 1]).collect::<String>())
        .collect_vec()
}

fn mirror(v: &Vec<String>) -> i32 {
    match (1..v.len())
        .map(|i| {
            (
                i,
                v.iter()
                    .take(i)
                    .rev()
                    .zip(v.iter().skip(i))
                    .all(|(a, b)| a == b),
            )
        })
        .find(|(_, b)| *b)
    {
        Some((i, _)) => i as i32,
        None => 0,
    }
}

fn mirror_w_smudge(v: &Vec<String>) -> i32 {
    let x = (1..v.len())
        .map(|i| {
            (
                i,
                v.iter()
                    .take(i)
                    .rev()
                    .zip(v.iter().skip(i))
                    .map(|(a, b)| a.chars().zip(b.chars()).filter(|(a, b)| a != b).count()),
            )
        })
        .find(|(_, b)| b.clone().sum::<usize>() == 1);
    match x {
        Some((i, _)) => i as i32,
        None => 0,
    }
}

fn main() {
    let file: String = std::env::args()
        .collect::<Vec<String>>()
        .get(1)
        .expect("No file given")
        .to_string();
    let input = std::fs::read_to_string(file).expect("Something went wrong reading the file");
    let p1 = input
        .split("\n\n")
        .map(|x| x.split("\n").map(|r| r.to_string()).collect_vec())
        .map(|g| (mirror(&g), mirror(&transpose(&g))))
        .map(|(r, c)| 100 * r + c)
        .sum::<i32>();
    println!("Part 1: {}", p1);

    let p2 = input
        .split("\n\n")
        .map(|x| x.split("\n").map(|r| r.to_string()).collect_vec())
        .map(|g| (mirror_w_smudge(&g), mirror_w_smudge(&transpose(&g))))
        .map(|(r, c)| 100 * r + c)
        .sum::<i32>();
    println!("Part 2: {}", p2);
}
