# SPDX-FileCopyrightText: 2023-present John Muchovej <5000729+jmuchovej@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import uvicorn
from fastapi import FastAPI


api = FastAPI()


def launch_server():
    config = uvicorn.Config(
        api, port=2365, host="0.0.0.0",
        log_level="info",
    )
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    launch_server()
