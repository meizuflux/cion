FROM gitpod/workspace-python-3.10

USER gitpod

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    cargo install just
