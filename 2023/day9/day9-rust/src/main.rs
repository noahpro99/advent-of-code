use itertools::Itertools;

fn part1(input: &String) -> u32 {
    let x = input
        .split("\n")
        .map(|x| {
            x.split_whitespace()
                .map(|x| x.parse::<u32>().unwrap())
                .collect_vec()
        })
        .map(|x| x)
        .collect_vec();
    dbg!(x);
    1
}

fn part2(input: &String) -> u32 {
    1
}

pub fn main() {
    let input = std::fs::read_to_string("d9.txt").unwrap();
    let p1 = part1(&input);
    let p2 = part2(&input);

    println!("Part 1: {}", p1);
    println!("Part 2: {}", p2);

    // assert_eq!(p1, 1992273652);
    // assert_eq!(p2, 1012);
}
