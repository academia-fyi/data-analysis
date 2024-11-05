from pathlib import Path
from typer import Typer


cli = Typer()


@cli.command()
def refresh_datasources(
    datapath: Path,
) -> None:
    """Refreshes all data-sources.

    Args
        datapath: Where should we put this data?
    """
    from academiafyi.sources import us_ipeds

    us_ipeds.download(datapath)
