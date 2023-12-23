use itertools::Itertools;

fn main() {
    let file: String = std::env::args()
        .collect::<Vec<String>>()
        .get(1)
        .expect("No file given")
        .to_string();
    let input = std::fs::read_to_string(file).expect("Something went wrong reading the file");
    let mut border = 0;
    let path = input
        .split('\n')
        .map(|x| x.split_whitespace().collect_tuple().unwrap())
        .map(|(d, n, _)| (d, n.parse::<i32>().unwrap()))
        .scan((0, 0), |pos, (d, n)| {
            border += n;
            *pos = match d {
                "U" => (pos.0, pos.1 + n),
                "D" => (pos.0, pos.1 - n),
                "L" => (pos.0 - n, pos.1),
                "R" => (pos.0 + n, pos.1),
                _ => panic!("Unknown direction"),
            };
            Some(*pos)
        })
        .collect_vec();

    dbg!(&path);
    let shoelace: i32 = path
        .iter()
        .cycle()
        .tuple_windows()
        .take(path.len())
        .map(|(a, b)| {
            // dbg!((a, b));
            // dbg!(a.0 * b.1 - a.1 * b.0);
            a.0 * b.1 - a.1 * b.0
        })
        .sum::<i32>()
        .abs()
        / 2;
    let p1 = shoelace + border / 2 + 1;
    println!("Part 1: {}", p1);

}
