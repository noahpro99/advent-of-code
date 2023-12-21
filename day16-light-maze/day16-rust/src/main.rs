use itertools::Itertools;
use std::collections::HashSet;

#[derive(Hash, Eq, PartialEq, Debug, Clone)]
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
}

enum Tile {
    Empty,
    ForwardSlash,
    BackSlash,
    VerticalSplitter,
    HorizontalSplitter,
}

impl Tile {
    fn from_char(c: char) -> Tile {
        match c {
            '.' => Tile::Empty,
            '/' => Tile::ForwardSlash,
            '\\' => Tile::BackSlash,
            '|' => Tile::VerticalSplitter,
            '-' => Tile::HorizontalSplitter,
            _ => panic!("Invalid tile"),
        }
    }

    fn next_beams(&self, dir: Direction) -> Vec<Direction> {
        match (&self, &dir) {
            (Tile::Empty, _) => vec![dir],
            (Tile::ForwardSlash, Direction::Up) => vec![Direction::Right],
            (Tile::ForwardSlash, Direction::Down) => vec![Direction::Left],
            (Tile::ForwardSlash, Direction::Left) => vec![Direction::Down],
            (Tile::ForwardSlash, Direction::Right) => vec![Direction::Up],
            (Tile::BackSlash, Direction::Up) => vec![Direction::Left],
            (Tile::BackSlash, Direction::Down) => vec![Direction::Right],
            (Tile::BackSlash, Direction::Left) => vec![Direction::Up],
            (Tile::BackSlash, Direction::Right) => vec![Direction::Down],
            (Tile::VerticalSplitter, Direction::Up) => vec![Direction::Up],
            (Tile::VerticalSplitter, Direction::Down) => vec![Direction::Down],
            (Tile::VerticalSplitter, Direction::Left) => vec![Direction::Up, Direction::Down],
            (Tile::VerticalSplitter, Direction::Right) => vec![Direction::Up, Direction::Down],
            (Tile::HorizontalSplitter, Direction::Up) => vec![Direction::Left, Direction::Right],
            (Tile::HorizontalSplitter, Direction::Down) => vec![Direction::Left, Direction::Right],
            (Tile::HorizontalSplitter, Direction::Left) => vec![Direction::Left],
            (Tile::HorizontalSplitter, Direction::Right) => vec![Direction::Right],
        }
    }
}

#[derive(Hash, Eq, PartialEq, Debug, Clone)]
struct Beam {
    dir: Direction,
    pos: (i32, i32),
}

impl Beam {
    fn next_coords(&self) -> (i32, i32) {
        self.dir.next_coords(self.pos)
    }
}

fn inside_grid(pos: (i32, i32), grid: &Vec<Vec<char>>) -> bool {
    pos.0 >= 0 && pos.0 < grid.len() as i32 && pos.1 >= 0 && pos.1 < grid[0].len() as i32
}

fn energized(input: Vec<Vec<char>>, start: Beam) -> i32 {
    let mut energized = HashSet::new();
    let mut seen = HashSet::new();
    let mut frontier = Vec::new();

    frontier.push(start.clone());

    while let Some(beam) = frontier.pop() {
        let next_pos = beam.next_coords();
        if !inside_grid(next_pos, &input) {
            continue;
        }
        Tile::from_char(input[next_pos.0 as usize][next_pos.1 as usize])
            .next_beams(beam.dir)
            .iter()
            .for_each(|next_beam| {
                let next = Beam {
                    dir: next_beam.clone(),
                    pos: next_pos,
                };
                if !seen.contains(&next) {
                    frontier.push(next.clone());
                    seen.insert(next.clone());
                    energized.insert(next.pos.clone());
                }
            });
    }
    energized.len() as i32
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
    let p1 = energized(
        parsed.clone(),
        Beam {
            dir: Direction::Right,
            pos: (0, -1),
        },
    );
    println!("Part 1: {}", p1);

    // let p2 be max when you start anywhere on the outside
    let starts = (0..parsed.len() as i32)
        .map(|x| Beam {
            dir: Direction::Right,
            pos: (x, -1),
        })
        .chain((0..parsed.len() as i32).map(|x| Beam {
            dir: Direction::Left,
            pos: (x, parsed[0].len() as i32),
        }))
        .chain((0..parsed[0].len() as i32).map(|x| Beam {
            dir: Direction::Down,
            pos: (-1, x),
        }))
        .chain((0..parsed[0].len() as i32).map(|x| Beam {
            dir: Direction::Up,
            pos: (parsed.len() as i32, x),
        }))
        .collect_vec();

    let p2 = starts
        .iter()
        .map(|x| energized(parsed.clone(), x.clone()))
        .max()
        .unwrap();
    println!("Part 2: {}", p2);
}
