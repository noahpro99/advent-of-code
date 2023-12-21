use itertools::Itertools;
use std::collections::{BinaryHeap, HashSet};

#[derive(Hash, Eq, PartialEq, Debug, Clone, Copy, Ord, PartialOrd)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl Direction {
    fn next_coords(&self, pos: (i32, i32)) -> (i32, i32) {
        match self {
            Direction::Up => (pos.0 - 1, pos.1),
            Direction::Down => (pos.0 + 1, pos.1),
            Direction::Left => (pos.0, pos.1 - 1),
            Direction::Right => (pos.0, pos.1 + 1),
        }
    }

    fn udlr() -> Vec<Direction> {
        vec![
            Direction::Up,
            Direction::Down,
            Direction::Left,
            Direction::Right,
        ]
    }

    fn opposite(&self) -> Direction {
        match self {
            Direction::Up => Direction::Down,
            Direction::Down => Direction::Up,
            Direction::Left => Direction::Right,
            Direction::Right => Direction::Left,
        }
    }
}

fn value(parsed: &Vec<Vec<char>>, pos: (i32, i32)) -> i32 {
    parsed[pos.0 as usize][pos.1 as usize]
        .to_string()
        .parse::<i32>()
        .unwrap()
}

fn inside_grid(pos: (i32, i32), parsed: &Vec<Vec<char>>) -> bool {
    pos.0 >= 0 && pos.1 >= 0 && pos.0 < parsed.len() as i32 && pos.1 < parsed[0].len() as i32
}

fn min_heat_loss(parsed: &Vec<Vec<char>>, ultra: bool) -> i32 {
    let mut frontier = BinaryHeap::new();
    let mut visited = HashSet::new();
    let start = (0, 0);
    let end = (parsed.len() as i32 - 1, parsed[0].len() as i32 - 1);

    frontier.push((0, 0, None, start));

    while let Some((score, c, dir, pos)) = frontier.pop() {
        Direction::udlr()
            .iter()
            .filter_map(|&new_dir| {
                let next_pos = new_dir.next_coords(pos);
                let new_c = if dir == Some(new_dir) { c + 1 } else { 1 };
                let next_node = (new_c, Some(new_dir), next_pos);
                if !inside_grid(next_pos, &parsed)
                    || visited.contains(&next_node)
                    || Some(new_dir.opposite()) == dir
                    || !ultra && new_c > 3
                    || ultra
                        && (new_c > 10
                            || (0 < c && c < 4 && dir != Some(new_dir))
                            || new_c < 4 && next_pos == end)
                {
                    return None;
                }
                visited.insert(next_node.clone());
                Some((
                    score - value(parsed, next_pos),
                    new_c,
                    Some(new_dir),
                    next_pos,
                ))
            })
            .for_each(|x| frontier.push(x));
        if pos == end {
            return -score;
        }
    }
    panic!("No path found");
}

fn main() {
    let file: String = std::env::args()
        .collect::<Vec<String>>()
        .get(1)
        .expect("No file given")
        .to_string();
    let input = std::fs::read_to_string(file).expect("Something went wrong reading the file");
    let parsed = input
        .split('\n')
        .map(|x| x.chars().collect_vec())
        .collect_vec();

    let p1 = min_heat_loss(&parsed, false);
    println!("Part 1: {}", p1);

    let p2 = min_heat_loss(&parsed, true);
    println!("Part 2: {}", p2);
}
