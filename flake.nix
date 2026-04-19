{
  description = "Dropspot development flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url  = "github:numtide/flake-utils";
    rust-overlay = {
      url = "github:oxalica/rust-overlay";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ self, nixpkgs, flake-utils, rust-overlay }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [ (import rust-overlay) ];
        pkgs = import nixpkgs {
          inherit system overlays;
          config = {
            allowUnfree = true;
            permittedInsecurePackages = [];
          };
        };

        python = with pkgs; (python314.withPackages (ps: with ps; [
          pip
          pyright
          ruff
          uv
        ]));

        rust = with pkgs; (rust-bin.fromRustupToolchainFile ./rust-toolchain.toml);
        rustDeps = with pkgs; [
          rust
          bacon # File watching
        ];

        editorDeps = with pkgs; [
          neovim
          rustfmt
        ];

        deps = with pkgs; [
          direnv
          python
        ] ++ rustDeps ++ editorDeps;
      in
      {
        devShells.default = with pkgs; mkShell {
          buildInputs = deps;
          # TODO(alec): How to get RUST_SRC_PATH from the `rust` package we use from rust-overlay
          RUST_SRC_PATH = "${pkgs.rust.packages.stable.rustPlatform.rustLibSrc}";
        };
      }
    );
}
