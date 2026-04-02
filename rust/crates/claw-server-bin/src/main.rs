use claw_server::{app, AppState};

#[tokio::main]
async fn main() {
    let addr = std::env::var("BIND_ADDR").unwrap_or_else(|_| "0.0.0.0:3000".to_string());
    let listener = tokio::net::TcpListener::bind(&addr)
        .await
        .expect("failed to bind address");
    println!("claw-server listening on {addr}");
    axum::serve(listener, app(AppState::new()))
        .await
        .expect("server error");
}
