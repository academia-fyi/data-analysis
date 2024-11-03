# syntax=docker/dockerfile:1
#region Build Stage:: Base #############################################################
FROM ghcr.io/jmuchovej/devcontainers/research@sha256:f56cf22ffa720a4fc6c86309f96d5e1e6cb8820b37e0026f58245f2a5544dd5b AS base

SHELL [ "/bin/bash", "-o", "pipefail", "-c" ]

ENV CONTAINER=1
ENV CONDA_ALWAYS_YES=true
ENV PROJECT=/workspaces/data-analysis

USER root

RUN <<EOF
apt-get update
apt-get install -y --no-install-recommends \
    mdbtools \
    libpq-dev

apt-get clean
rm -rf /var/lib/apt/lists/*
EOF

USER ${NB_UID}

ADD --chown=${NB_UID}:${NB_GID} . ${PROJECT}
WORKDIR ${PROJECT}
#endregion #############################################################################

#region Build Stage:: Configuration ####################################################
FROM base AS config

USER root

# Config & Setup Conda #################################################################
# Fix File/Directory Permissions #######################################################
RUN <<EOF
fix-permissions "${CONDA_DIR}"
fix-permissions "${PROJECT}"
fix-permissions "/home/${NB_USER}"
EOF
#endregion #############################################################################

#region Build Stage: Output ############################################################
FROM base AS output

USER ${NB_UID}

COPY --from=config ${CONDA_DIR} ${CONDA_DIR}
COPY --from=config ${PROJECT} ${PROJECT}
COPY --from=config "/home/${NB_USER}" "/home/${NB_USER}"
#endregion #############################################################################
