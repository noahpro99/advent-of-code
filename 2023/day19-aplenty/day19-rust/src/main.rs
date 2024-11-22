use std::{collections::HashMap, str::FromStr};

use itertools::Itertools;

#[derive(Debug, Clone)]
enum Comparison {
    LessThan,
    GreaterThan,
}

impl FromStr for Comparison {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "<" => Ok(Comparison::LessThan),
            ">" => Ok(Comparison::GreaterThan),
            _ => Err(format!("Unknown comparison: {}", s)),
        }
    }
}

#[derive(Debug, Clone)]
enum RuleResult {
    Reject,
    Accept,
    Next(String),
}

impl FromStr for RuleResult {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "A" => Ok(RuleResult::Accept),
            "R" => Ok(RuleResult::Reject),
            _ => Ok(RuleResult::Next(s.to_string())),
        }
    }
}

#[derive(Debug, Clone)]
enum Category {
    X,
    M,
    A,
    S,
}

impl FromStr for Category {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "x" => Ok(Category::X),
            "m" => Ok(Category::M),
            "a" => Ok(Category::A),
            "s" => Ok(Category::S),
            _ => Err(format!("Unknown category: {}", s)),
        }
    }
}

impl From<Category> for usize {
    fn from(category: Category) -> Self {
        match category {
            Category::X => 0,
            Category::M => 1,
            Category::A => 2,
            Category::S => 3,
        }
    }
}

#[derive(Debug, Clone)]
struct Rule {
    category: Category,
    comparison: Comparison,
    value: i64,
    result: RuleResult,
}

impl FromStr for Rule {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (value, result) = s[2..].split(":").collect_tuple().unwrap();
        Ok(Rule {
            category: s[0..1].parse::<Category>()?,
            comparison: s[1..2].parse::<Comparison>()?,
            value: value.parse::<i64>().unwrap(),
            result: result.parse::<RuleResult>()?,
        })
    }
}

#[derive(Debug, Clone)]
struct Workflow {
    rules: Vec<Rule>,
    else_result: RuleResult,
}

impl FromStr for Workflow {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let rest = s.strip_suffix("}").unwrap();
        let rules_and_else = rest.split(",").collect_vec();
        let else_result = rules_and_else[rules_and_else.len() - 1].parse::<RuleResult>()?;
        let rules = rules_and_else
            .iter()
            .take(rules_and_else.len() - 1)
            .map(|x| x.parse::<Rule>())
            .collect::<Result<Vec<Rule>, String>>()?;
        Ok(Workflow { rules, else_result })
    }
}

#[derive(Debug, Clone)]
struct Part {
    x: i64,
    m: i64,
    a: i64,
    s: i64,
}
impl Part {
    fn sum(&self) -> i64 {
        self.x + self.m + self.a + self.s
    }

    fn get(&self, category: &Category) -> i64 {
        match category {
            Category::X => self.x,
            Category::M => self.m,
            Category::A => self.a,
            Category::S => self.s,
        }
    }
}

impl FromStr for Part {
    type Err = String;

    fn from_str(str: &str) -> Result<Self, Self::Err> {
        // {x=2127,m=1623,a=2188,s=1013}
        let str = str.strip_prefix("{").unwrap();
        let str = str.strip_suffix("}").unwrap();
        let str = str.split(",").collect_vec();
        let (mut x, mut m, mut a, mut s) = (0, 0, 0, 0);
        for part in str {
            let (category, value) = part.split_once("=").unwrap();
            match category {
                "x" => x = value.parse::<i64>().unwrap(),
                "m" => m = value.parse::<i64>().unwrap(),
                "a" => a = value.parse::<i64>().unwrap(),
                "s" => s = value.parse::<i64>().unwrap(),
                _ => panic!("Unknown category"),
            }
        }
        Ok(Part { x, m, a, s })
    }
}

fn apply_rule(part: &Part, rule: Rule) -> Option<RuleResult> {
    let part_category = match rule.category {
        Category::X => part.x,
        Category::M => part.m,
        Category::A => part.a,
        Category::S => part.s,
    };
    match rule.comparison {
        Comparison::LessThan => {
            if part_category < rule.value {
                Some(rule.result)
            } else {
                None
            }
        }
        Comparison::GreaterThan => {
            if part_category > rule.value {
                Some(rule.result)
            } else {
                None
            }
        }
    }
}

fn apply_workflow(part: &Part, workflow: &Workflow) -> RuleResult {
    let mut result = workflow.else_result.clone();
    for rule in &workflow.rules {
        if let Some(rule_result) = apply_rule(&part, rule.clone()) {
            result = rule_result;
            break;
        }
    }
    result
}

#[derive(Debug, Clone, Copy)]
enum FinalResult {
    Accept,
    Reject,
}

fn accept_or_reject(
    part: &Part,
    workflows: &HashMap<&str, Result<Workflow, String>>,
) -> FinalResult {
    let mut curr = workflows.get("in").unwrap().as_ref().unwrap();
    loop {
        let result = apply_workflow(part, curr);
        match result {
            RuleResult::Accept => return FinalResult::Accept,
            RuleResult::Reject => return FinalResult::Reject,
            RuleResult::Next(next) => {
                curr = workflows.get(next.as_str()).unwrap().as_ref().unwrap();
            }
        }
    }
}

fn main() {
    let file: String = std::env::args()
        .collect::<Vec<String>>()
        .get(1)
        .expect("No file given")
        .to_string();
    // let file = "ex1.txt";
    let input = std::fs::read_to_string(file).expect("Something went wrong reading the file");

    let (workflows, parts) = input
        .split("\n\n")
        .map(|x| x.split("\n").collect_vec())
        .collect_tuple()
        .unwrap();

    // parse the workflows into hashmap of id -> workflow
    let workflows = workflows
        .iter()
        .map(|x| {
            let (first, second) = x.split_once("{").unwrap();
            (first, second.parse::<Workflow>())
        })
        .collect::<HashMap<&str, Result<Workflow, String>>>();

    // parse the parts
    let parts = parts
        .iter()
        .map(|x| x.parse::<Part>())
        .collect::<Result<Vec<Part>, String>>()
        .unwrap();

    // apply the workflows to the parts
    let p1 = parts
        .iter()
        .map(|x| (x, accept_or_reject(x, &workflows)))
        .filter(|(_, result)| matches!(result, FinalResult::Accept))
        .map(|(part, _)| part.sum())
        .sum::<i64>();
    println!("Part 1: {}", p1);

    // create the first part range
    let part_range = PartRange {
        x: (1, 4001),
        m: (1, 4001),
        a: (1, 4001),
        s: (1, 4001),
    };

    let p2 = product_accepted(
        &part_range,
        Box::new(&RuleResult::Next("in".to_string())),
        &workflows,
    );
    println!("Part 2: {}", p2);
}

fn product_accepted(
    parts: &PartRange,
    curr: Box<&RuleResult>,
    workflows: &HashMap<&str, Result<Workflow, String>>,
) -> i64 {
    match curr.as_ref() {
        RuleResult::Accept => parts.product(),
        RuleResult::Reject => 0,
        RuleResult::Next(next) => {
            let mut sum = 0;
            let workflow = workflows.get(next.as_str()).unwrap().as_ref().unwrap();
            let mut parts = parts.clone();
            for rule in &workflow.rules {
                let (outside, inside) = split_part_range(&parts, rule);
                if let Some(inside) = inside {
                    sum += product_accepted(&inside, Box::new(&rule.result), &workflows);
                }
                if let Some(outside) = outside {
                    parts = outside;
                } else {
                    return sum;
                }
            }
            sum += product_accepted(&parts, Box::new(&workflow.else_result), &workflows);
            sum
        }
    }
}

/// Splits the part range into two part ranges, one that falls outside the rule and one that falls under the rule
///
/// (outside, inside)
fn split_part_range(parts: &PartRange, rule: &Rule) -> (Option<PartRange>, Option<PartRange>) {
    let mut outside: Option<PartRange> = None;
    let mut inside: Option<PartRange> = None;
    let category = &rule.category;
    let part_category = parts.get(&category);
    let value = rule.value;
    let mut outside_part = parts.clone();
    let mut inside_part = parts.clone();
    match rule.comparison {
        Comparison::LessThan => {
            if part_category.0 < value && value + 1 <= part_category.1 {
                outside_part.get_mut(&category).0 = value;
                inside_part.get_mut(&category).1 = value;
                outside = Some(outside_part);
                inside = Some(inside_part);
            } else if part_category.1 <= value + 1 {
                inside = Some(parts.clone());
            } else if part_category.0 > value {
                outside = Some(parts.clone());
            }
        }
        Comparison::GreaterThan => {
            if part_category.0 <= value && value + 1 < part_category.1 {
                outside_part.get_mut(&category).1 = value + 1;
                inside_part.get_mut(&category).0 = value + 1;
                outside = Some(outside_part);
                inside = Some(inside_part);
            } else if part_category.1 <= value + 1 {
                outside = Some(parts.clone());
            } else if part_category.0 > value {
                inside = Some(parts.clone());
            }
        }
    }
    (outside, inside)
}

#[derive(Debug, Clone, Copy)]
struct PartRange {
    x: (i64, i64),
    m: (i64, i64),
    a: (i64, i64),
    s: (i64, i64),
}

impl PartRange {
    fn get(&self, category: &Category) -> (i64, i64) {
        match category {
            Category::X => self.x,
            Category::M => self.m,
            Category::A => self.a,
            Category::S => self.s,
        }
    }

    fn get_mut(&mut self, category: &Category) -> &mut (i64, i64) {
        match category {
            Category::X => &mut self.x,
            Category::M => &mut self.m,
            Category::A => &mut self.a,
            Category::S => &mut self.s,
        }
    }

    fn product(&self) -> i64 {
        (self.x.1 - self.x.0)
            * (self.m.1 - self.m.0)
            * (self.a.1 - self.a.0)
            * (self.s.1 - self.s.0)
    }
}

impl Into<Part> for &PartRange {
    fn into(self) -> Part {
        Part {
            x: self.x.0,
            m: self.m.0,
            a: self.a.0,
            s: self.s.0,
        }
    }
}
