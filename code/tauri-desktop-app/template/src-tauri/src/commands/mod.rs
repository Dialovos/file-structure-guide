// Commands are thin: translate IPC arguments, call plain functions, return results.

pub fn greeting(name: &str) -> String {
    format!("hello, {name}")
}

#[tauri::command]
pub fn greet(name: &str) -> String {
    greeting(name)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greeting_includes_name() {
        assert_eq!(greeting("world"), "hello, world");
    }
}
