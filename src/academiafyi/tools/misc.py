from pathlib import Path
import logging

import click

from omegaconf import DictConfig, OmegaConf
from hydra import compose, initialize_config_dir
from hydra.core.global_hydra import GlobalHydra
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    Progress,
    TextColumn,
    MofNCompleteColumn,
    SpinnerColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
)

console = Console(stderr=True, record=True)


# https://github.com/Textualize/rich/issues/2416#issuecomment-1193773381
def _log_formatter(record: dict) -> str:
    """Log message formatter"""
    color_map = {
        "TRACE": "dim blue",
        "DEBUG": "cyan",
        "INFO": "bold",
        "SUCCESS": "bold green",
        "WARNING": "yellow",
        "ERROR": "bold red",
        "CRITICAL": "bold white on red",
    }
    lvl_color = color_map.get(record["level"].name, "cyan")
    return (
        "[not bold green]{time:YYYY/MM/DD HH:mm:ss}[/not bold green] | {level.icon}"
        + f"  - [{lvl_color}]{{message}}[/{lvl_color}]"
    )


logger = logging.getLogger("academia-fyi")
handler = RichHandler(
    console=console,
    rich_tracebacks=True,
    tracebacks_show_locals=True,
    tracebacks_suppress=[click],
    level=logging.DEBUG,
)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

pbar = Progress(
    TextColumn("[progress.description]{task.description}"),
    SpinnerColumn(),
    MofNCompleteColumn(),
    TextColumn("Elapsed: "),
    TimeElapsedColumn(),
    TextColumn("Remaining: "),
    TimeRemainingColumn(),
)


def setup_hydra(overrides: list[str]) -> DictConfig:
    """Given a list of overrides (paired with `<key>=<value>`), assemble the
    Hydra config so that it can be used to drive the majority of functions in a
    reliable, reproducible, way.

    Args:
        overrides : A list of Hydra-CLI compatible args to control execution params.
    """
    OmegaConf.clear_resolvers()

    GlobalHydra.instance().clear()
    config_dir = Path(__file__).parent.resolve() / "../configs"
    initialize_config_dir(str(config_dir), version_base="1.3")
    # Allow non-list-like values to be correct interpreted as string literals
    overrides = {var: override for (var, override) in [o.split("=") for o in overrides]}
    overrides = {
        var: (override if "," not in override or "[" in override else f'"{override}"')
        for (var, override) in overrides.items()
    }
    overrides = [f"{var}={override}" for (var, override) in overrides.items()]
    cfg = compose("config", overrides, return_hydra_config=True)

    return cfg
