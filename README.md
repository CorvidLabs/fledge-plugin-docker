# fledge-plugin-docker

Docker `build` / `push` and `compose up`/`down`/`logs` helpers, wired to your fledge project. The image name defaults to your project name; the version defaults to `latest`.

Reference plugin demonstrating the [fledge-v1 plugin protocol](https://corvidlabs.github.io/fledge/plugin-protocol.html) with the `exec` capability.

## Install

```bash
fledge plugins install CorvidLabs/fledge-plugin-docker
```

You'll be prompted to grant the `exec` capability — every action shells out to docker.

## Usage

```bash
fledge docker build                         # docker build -t <project>:latest .
fledge docker build --version v1.2.3        # docker build -t <project>:v1.2.3 .
fledge docker build --tag custom-name       # docker build -t custom-name:latest .
fledge docker build --file Dockerfile.prod  # use a different Dockerfile

fledge docker push --registry ghcr.io/myorg # docker push ghcr.io/myorg/<project>:latest
fledge docker push --registry ghcr.io/myorg --version v1.2.3

fledge docker up                            # docker compose up -d
fledge docker up --foreground               # docker compose up (attached)
fledge docker down                          # docker compose down
fledge docker logs                          # docker compose logs --tail=200 --follow

fledge docker --json                        # machine-readable
```

## Use in lanes

```toml
[lanes.deploy-staging]
description = "Build, push, deploy to staging"
fail_fast = true
steps = [
  "test",
  { run = "fledge docker build --version $(git rev-parse --short HEAD)" },
  { run = "fledge docker push --registry ghcr.io/myorg --version $(git rev-parse --short HEAD)" },
  { run = "scripts/deploy.sh staging" },
]

[lanes.local-stack]
description = "Spin up the dev stack"
steps = [
  { run = "fledge docker up" }
]
```

## JSON output

```json
{
  "schema_version": 1,
  "action": "docker_build",
  "command": "docker build -t 'myapp:latest' -f 'Dockerfile' .",
  "image": "myapp:latest",
  "exit_code": 0,
  "ok": true
}
```

## What this is and isn't

This plugin **wraps** docker. It doesn't reimplement docker. The win is that the image name is wired to your project automatically, the lane integration is consistent, and the JSON envelope means agents can drive deploy pipelines without scraping docker output.

For multi-stage builds, BuildKit features, multi-arch buildx, registry auth, etc. — use docker directly inside an inline lane step. This plugin is the 90% case.

## License

MIT
