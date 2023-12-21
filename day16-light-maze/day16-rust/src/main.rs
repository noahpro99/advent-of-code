use itertools::Itertools;
use std::collections::{HashMap, HashSet};

enum Direction {
    Up,
    Down,
    Left,
    Right,
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
        match (&self, dir) {
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

struct Beam {
    dir: Direction,
    pos: (i32, i32),
}


fn part1(input: Vec<Vec<char>>) -> i32 {
    let mut energized = HashMap::new();
    let mut seen = HashSet::new();
    let mut frontier = Vec::new();
    seen.append(())

}
    

fn main() {
    let file: String = std::env::args()
        .collect::<Vec<String>>()
        .get(1)
        .expect("No file given")
        .to_string();
    let input = std::fs::read_to_string(file).expect("Something went wrong reading the file");

    let p1 = part1(input.split('\n').map(|x| x.chars().collect_vec()).collect_vec());
    // println!("Part 1: {}", p1);

}
