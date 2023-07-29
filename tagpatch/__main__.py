import click
import pathlib
import tabulate
import sys
from tagpatch.patches import artist_name as artist_name_patch
from tagpatch.patches import embed_lrc as embed_lrc_patch
from tagpatch import utils
from tagpatch import options


@click.group()
def cli():
    pass


@cli.command(help=artist_name_patch.ArtistNamePatch.help())
@options.src
@options.dst
@options.assume_yes
@options.nested
def artist_name(
    src: pathlib.Path, dst: pathlib.Path | None, assume_yes: bool, nested: bool
):
    src, dst = utils.prepare_src_dst(src, dst)

    # Display the dry run table and ask for confirmation.
    patch = artist_name_patch.ArtistNamePatch(src, dst, nested)
    table = patch.prepare()
    if len(table) == 0:
        click.echo("No music files found in src.")
        sys.exit(0)
    click.echo(
        tabulate.tabulate(
            table,
            headers=patch.table_headers,
            tablefmt=patch.table_format,
            maxcolwidths=patch.table_max_col_width,
        )
    )
    if not assume_yes:
        click.confirm("Do you want to continue?", abort=True)

    # Apply the patch.
    patch.apply()
    click.echo("Applied.")


@cli.command(help=embed_lrc_patch.EmbedLyricsPatch.help())
@options.src
@options.dst
@options.assume_yes
@options.nested
def embed_lrc(
    src: pathlib.Path, dst: pathlib.Path | None, assume_yes: bool, nested: bool
):
    src, dst = utils.prepare_src_dst(src, dst)

    # Display the dry run table and ask for confirmation.
    patch = embed_lrc_patch.EmbedLyricsPatch(src, dst, nested)
    table = patch.prepare()
    if len(table) == 0:
        click.echo("No music files found in src.")
        sys.exit(0)
    click.echo(
        tabulate.tabulate(
            table,
            headers=patch.table_headers,
            tablefmt=patch.table_format,
            maxcolwidths=patch.table_max_col_width,
        )
    )
    if not assume_yes:
        click.confirm("Do you want to continue?", abort=True)

    # Apply the patch.
    patch.apply()
    click.echo("Applied.")


def main():
    # Invoke the click group.
    cli()


if __name__ == "__main__":
    main()
