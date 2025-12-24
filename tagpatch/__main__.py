import pathlib
import sys

import tabulate
import typer

from tagpatch import utils
from tagpatch.patches import artist_name as artist_name_patch
from tagpatch.patches import download_lrc as download_lrc_patch
from tagpatch.patches import embed_lrc as embed_lrc_patch

app = typer.Typer(help="CLI tool which applies common patches to music tags.")


@app.command(help=artist_name_patch.ArtistNamePatch.help())
def artist_name(
    src: pathlib.Path = typer.Option(
        pathlib.Path().resolve(),
        "-s",
        "--src",
        exists=True,
        writable=True,
        show_default=True,
        resolve_path=True,
    ),
    dst: pathlib.Path | None = typer.Option(
        None,
        "-d",
        "--dst",
        writable=True,
        resolve_path=True,
    ),
    assume_yes: bool = typer.Option(False, "-y", "--assume-yes"),
    nested: bool = typer.Option(False, "-n", "--nested"),
) -> None:
    src, dst = utils.prepare_src_dst(src, dst)

    patch = artist_name_patch.ArtistNamePatch(src, dst, nested)
    table = patch.prepare()
    if len(table) == 0:
        typer.echo("No music files found in src.")
        sys.exit(0)
    typer.echo(
        tabulate.tabulate(
            table,
            headers=patch.table_headers,
            tablefmt=patch.table_format,
            maxcolwidths=patch.table_max_col_width,
        )
    )
    if not assume_yes:
        typer.confirm("Do you want to continue?", abort=True)

    patch.apply()
    typer.echo("Applied.")


@app.command(help=embed_lrc_patch.EmbedLyricsPatch.help())
def embed_lrc(
    src: pathlib.Path = typer.Option(
        pathlib.Path().resolve(),
        "-s",
        "--src",
        exists=True,
        writable=True,
        show_default=True,
        resolve_path=True,
    ),
    dst: pathlib.Path | None = typer.Option(
        None,
        "-d",
        "--dst",
        writable=True,
        resolve_path=True,
    ),
    assume_yes: bool = typer.Option(False, "-y", "--assume-yes"),
    nested: bool = typer.Option(False, "-n", "--nested"),
) -> None:
    src, dst = utils.prepare_src_dst(src, dst)

    patch = embed_lrc_patch.EmbedLyricsPatch(src, dst, nested)
    table = patch.prepare()
    if len(table) == 0:
        typer.echo("No music files found in src.")
        sys.exit(0)
    typer.echo(
        tabulate.tabulate(
            table,
            headers=patch.table_headers,
            tablefmt=patch.table_format,
            maxcolwidths=patch.table_max_col_width,
        )
    )
    if not assume_yes:
        typer.confirm("Do you want to continue?", abort=True)

    patch.apply()
    typer.echo("Applied.")


@app.command(help=download_lrc_patch.DownloadLrcPatch.help())
def download_lrc(
    src: pathlib.Path = typer.Option(
        pathlib.Path().resolve(),
        "-s",
        "--src",
        exists=True,
        writable=True,
        show_default=True,
        resolve_path=True,
    ),
    dst: pathlib.Path | None = typer.Option(
        None,
        "-d",
        "--dst",
        writable=True,
        resolve_path=True,
    ),
    assume_yes: bool = typer.Option(False, "-y", "--assume-yes"),
    nested: bool = typer.Option(False, "-n", "--nested"),
) -> None:
    src, dst = utils.prepare_src_dst(src, dst)

    patch = download_lrc_patch.DownloadLrcPatch(src, dst, nested)
    table = patch.prepare()
    if len(table) == 0:
        typer.echo("No music files found in src.")
        sys.exit(0)
    typer.echo(
        tabulate.tabulate(
            table,
            headers=patch.table_headers,
            tablefmt=patch.table_format,
            maxcolwidths=patch.table_max_col_width,
        )
    )
    if not assume_yes:
        typer.confirm("Do you want to continue?", abort=True)

    patch.apply()
    typer.echo("Applied.")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
