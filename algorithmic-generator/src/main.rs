use nalgebra_glm as glm;
use rand::Rng;
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::Write;

#[derive(serde::Serialize, Deserialize, Debug)]
struct Tree {
    node: TreeNode,
    children: Vec<Tree>,
}
impl Tree {
    fn new(node: TreeNode, children: Vec<Tree>) -> Tree {
        Tree {
            node: node,
            children: children,
        }
    }
}

#[derive(Serialize, Deserialize, Debug)]
struct TreeNode {
    girth: f32,
    position: glm::Vec3,
}
impl TreeNode {
    fn new(girth: f32, position: glm::Vec3) -> TreeNode {
        TreeNode {
            girth: girth,
            position: position,
        }
    }
}

fn find_perpendicular_unit_vec(vec: &glm::Vec3) -> glm::Vec3 {
    let rand_vector = glm::vec3(1.0, 2.0, 3.0);

    return glm::normalize(&glm::cross(vec, &rand_vector));
}

const MAX_BRANCH_LENGTH: f32 = 0.25;
const MIN_GIRTH_THRESHOLD: f32 = 1.0;

fn generate_children(node: &TreeNode, direction: glm::Vec3) -> Vec<Tree> {
    let mut rng = rand::thread_rng();

    let girth = node.girth;
    let position = node.position;

    let mut child_girth_total = 0.0;
    let mut children_nodes = vec![];
    loop {
        if child_girth_total >= girth {
            break;
        }

        let perp_unit_vector1 = find_perpendicular_unit_vec(&direction);
        let perp_unit_vector2 = glm::normalize(&glm::cross(&direction, &perp_unit_vector1));

        let new_direction_component1: glm::Vec3 = perp_unit_vector1 * (rng.gen::<f32>() - 0.5);
        let new_direction_component2: glm::Vec3 = perp_unit_vector2 * (rng.gen::<f32>() - 0.5);

        let new_direction = glm::normalize(
            &(new_direction_component1 + new_direction_component2 + glm::vec3(0.0, 0.0, 2.0)),
        );

        let new_branch_length = rng.gen::<f32>() * MAX_BRANCH_LENGTH;

        let new_position: glm::Vec3 = position + (new_direction * new_branch_length);

        let new_girth: f32 = rng.gen::<f32>() * girth;

        child_girth_total += new_girth;

        children_nodes.push(TreeNode::new(new_girth, new_position));
    }

    let mut children_trees = vec![];

    for child in children_nodes {
        if child.girth <= MIN_GIRTH_THRESHOLD {
            children_trees.push(Tree::new(child, vec![]));
        } else {
            let direction = &child.position - position;
            let children = generate_children(&child, direction);
            children_trees.push(Tree::new(child, children));
        }
    }

    return children_trees;
}

fn main() {
    let initial_tree = Tree::new(TreeNode::new(3.0, glm::vec3(0.0, 0.0, 0.5)), vec![]);

    let children = generate_children(&initial_tree.node, glm::vec3(0.0, 0.0, 1.0));

    let tree = Tree::new(initial_tree.node, children);
    let tree = Tree::new(TreeNode::new(3.0, glm::vec3(0.0, 0.0, 0.0)), vec![tree]);

    let serialized = serde_json::to_string(&tree).unwrap();

    let path = "tree.json";

    let mut output = File::create(path).unwrap();

    write!(output, "{}", serialized).unwrap();
}
