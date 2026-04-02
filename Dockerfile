# ── Stage 1: Build ──────────────────────────────────────────────────────────
FROM rust:1.87-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y pkg-config libssl-dev && rm -rf /var/lib/apt/lists/*

# Copy workspace manifests first (layer-cache friendly)
COPY rust/Cargo.toml rust/Cargo.lock ./
COPY rust/crates ./crates

# Build only the server binary in release mode
RUN cargo build --release -p claw-server-bin

# ── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM debian:bookworm-slim

WORKDIR /app

# Install minimal runtime deps
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy the compiled binary from builder
COPY --from=builder /app/target/release/claw-server /usr/local/bin/claw-server

EXPOSE 3000

ENV BIND_ADDR=0.0.0.0:3000

CMD ["claw-server"]
