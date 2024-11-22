use itertools::Itertools;

fn get_distance(
    a: (i32, i32),
    b: (i32, i32),
    n: i64,
    blank_cols: impl Iterator<Item = usize>,
    blank_rows: impl Iterator<Item = usize>,
) -> i64 {
    let base_distance = (a.0 - b.0).abs() + (a.1 - b.1).abs();
    let additional_from_rows = blank_rows
        .filter(|r| a.0.min(b.0) < *r as i32 && a.0.max(b.0) > *r as i32)
        .count() as i32;
    let additional_from_cols = blank_cols
        .filter(|c| a.1.min(b.1) < *c as i32 && a.1.max(b.1) > *c as i32)
        .count() as i32;
    // print row of smaller one
    println!("{}", a.0.min(b.0));
    base_distance as i64 + (n - 1) * (additional_from_rows + additional_from_cols) as i64
}

pub fn main() {
    let file: String = std::env::args()
        .collect::<Vec<String>>()
        .get(1)
        .expect("No file given")
        .to_string();
    let input = std::fs::read_to_string(file).expect("Something went wrong reading the file");

    let galaxies = input
        .lines()
        .enumerate()
        .map(|(r, line)| {
            line.chars()
                .enumerate()
                .filter_map(move |(c, ch)| match ch {
                    '#' => Some((r as i32, c as i32)),
                    _ => None,
                })
        })
        .flatten()
        .collect_vec();

    let blank_rows = input.lines().enumerate().filter_map(|(r, line)| {
        if line.chars().all(|ch| ch == '.') {
            Some(r)
        } else {
            None
        }
    });

    let n_cols = input.lines().next().unwrap().len();
    let blank_cols = (0..n_cols).filter(|c| {
        input
            .lines()
            .all(|line| line.chars().nth(*c).unwrap() == '.')
    });

    let p1 = galaxies
        .iter()
        .tuple_combinations::<(_, _)>()
        .map(|(a, b)| get_distance(*a, *b, 2, blank_cols.clone(), blank_rows.clone()))
        .sum::<i64>();
    println!("Part 1: {}", p1);

    let p2: i64 = galaxies
        .iter()
        .tuple_combinations()
        .map(|(a, b)| get_distance(*a, *b, 1e6 as i64, blank_cols.clone(), blank_rows.clone()))
        .sum();
    println!("Part 2: {}", p2);
}
