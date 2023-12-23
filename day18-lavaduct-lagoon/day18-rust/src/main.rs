use itertools::Itertools;

fn shoelace(path: Vec<(i64, i64)>) -> i64 {
    path.iter()
        .cycle()
        .tuple_windows()
        .take(path.len())
        .map(|(a, b)| a.0 * b.1 - a.1 * b.0)
        .sum::<i64>()
        .abs()
        / 2
}

fn walk(steps: Vec<(i64, i64)>) -> (Vec<(i64, i64)>, i64) {
    let mut boundary_len = 0;
    let path = steps
        .iter()
        .scan((0, 0), |pos, (d, n)| {
            boundary_len += n;
            *pos = match d {
                0 => (pos.0 + n, pos.1),
                1 => (pos.0, pos.1 - n),
                2 => (pos.0 - n, pos.1),
                3 => (pos.0, pos.1 + n),
                _ => panic!("Unknown direction"),
            };
            Some(*pos)
        })
        .collect_vec();
    (path, boundary_len)
}

fn main() {
    let file: String = std::env::args()
        .collect::<Vec<String>>()
        .get(1)
        .expect("No file given")
        .to_string();
    let input = std::fs::read_to_string(file).expect("Something went wrong reading the file");
    let steps = input
        .split('\n')
        .map(|x| x.split_whitespace().collect_tuple().unwrap())
        .map(|(d, n, _)| {
            (
                match d {
                    "R" => 0,
                    "U" => 1,
                    "D" => 2,
                    "L" => 3,
                    _ => panic!("Unknown direction"),
                },
                n.parse::<i64>().unwrap(),
            )
        })
        .collect_vec();

    let (path, border) = walk(steps);
    let p1 = shoelace(path) + border / 2 + 1;
    println!("Part 1: {}", p1);

    let steps2 = input
        .split('\n')
        .map(|x| x.split_whitespace().collect_tuple().unwrap())
        .map(|(_, _, c)| {
            (
                c[c.len() - 2..c.len() - 1].parse::<i64>().unwrap(),
                i64::from_str_radix(&c[2..c.len() - 2], 16).unwrap(),
            )
        })
        .collect_vec();

    let (path2, border2) = walk(steps2);
    let p2 = shoelace(path2) + border2 / 2 + 1;
    println!("Part 2: {}", p2);
}
