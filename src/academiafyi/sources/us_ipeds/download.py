from copy import deepcopy
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import polars as pl
from academiafyi.tools.misc import pbar


def _scrape_and_build_database_table() -> pl.DataFrame:
    """Build the database table from the website."""
    ACCESS_DBS_URL = "https://nces.ed.gov/ipeds/use-the-data/download-access-database"
    URL = urlparse(ACCESS_DBS_URL)

    response = requests.get(ACCESS_DBS_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.body.select("table.ipeds-table")[0]
    header = table.select("thead th")
    header = [th.string for th in header]

    rows = table.select("tbody tr")

    data = []

    for row in rows:
        rowdata = {}
        for key, element in zip(header, row.select("td")):
            col = element.find_all("a")
            if len(col) > 0:
                href = col[0].get("href")
                col = urlunparse(deepcopy(URL)._replace(path=href))
            else:
                col = element.string
            rowdata[key] = col

        data.append(rowdata)

    df = pl.DataFrame(data).with_columns(
        ("01 " + pl.col("Release Date")).str.to_date("%d %B %Y").alias("Release Date")
    )

    return df


def _download_accdb(datapath: Path, url: str) -> str:
    """Download a single Access DB from the US IPEDs database."""
    file = requests.get(url)
    if file.headers["Content-Type"] == "application/x-zip-compressed":
        zf = ZipFile(BytesIO(file.content))
        for infolist in zf.infolist():
            zf.extract(infolist, path=datapath)
        return

    with open(url.split("/")[-1], "w") as f:
        f.write(file.content)


def download(data_prefix: Path | str) -> None:
    """Actually download the data from the US IPEDs database."""
    df = _scrape_and_build_database_table()
    datapath = Path(data_prefix) / "us-ipeds"
    datapath.mkdir(exist_ok=True, parents=True)

    df.write_ndjson(f"{datapath}.jsonl")

    track_kwargs = dict(
        sequence=df.iter_rows(named=True),
        total=len(df),
        description="Updating data-sources from the US Dept of Ed's 'IPEDS' database.",
    )

    with pbar:
        for row in pbar.track(**track_kwargs):
            _download_accdb(datapath, row["Database Name"])
