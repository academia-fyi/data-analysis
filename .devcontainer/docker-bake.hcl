variable "GIT_SHORT_SHA" {
    type = string
}

group "default" {
    targets = [ "base" ]
}

target "base" {
    // Since buildx should be executed with `-f .devcontainer/docker-bake.hcl`
    //   the `context` is relative to __where `docker buildx bake` is run__.
    context = "./"
    dockerfile = ".devcontainer/Dockerfile"
    platforms = [ "linux/amd64", "linux/arm64", ]

    tags = [
        "ghcr.io/academia-fyi/data-analysis:edge",
        "ghcr.io/academia-fyi/data-analysis:${GIT_SHORT_SHA}",
    ]
}
