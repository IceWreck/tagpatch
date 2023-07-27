import click
import pathlib
import tabulate
import sys
from tagpatch.patches import artist_name as artist_name_patch


@click.group()
def cli():
    pass


@cli.command(help=artist_name_patch.ArtistNamePatch.help())
@click.option(
    "-s",
    "--src",
    required=False,
    default=pathlib.Path().resolve(),
    show_default=True,
    type=click.Path(exists=True, writable=True, path_type=pathlib.Path),
)
@click.option(
    "-d",
    "--dst",
    required=False,
    type=click.Path(writable=True, path_type=pathlib.Path),
)
@click.option(
    "-y",
    "--assume-yes",
    required=False,
    default=False,
    is_flag=True,
)
@click.option(
    "-n",
    "--nested",
    required=False,
    default=False,
    is_flag=True,
)
def artist_name(src: pathlib.Path, dst: pathlib.Path | None, assume_yes: bool, nested: bool):
    # If destination isn't provided, overwrite the source.
    if dst is None:
        dst: pathlib.Path = src

    # Create destination if it doesn't exist.
    if not dst.exists():
        if dst.suffix == "":
            dst.mkdir(parents=True, exist_ok=True)
        else:
            dst.touch()

    # Source and destination must be of the same type.
    if not ((src.is_dir() and dst.is_dir()) or (src.is_file() and dst.is_file())):
        raise click.BadParameter(
            "Source and destination must be both files or both directories."
        )

    # Display the dry run table and ask for confirmation.
    patch = artist_name_patch.ArtistNamePatch(src, dst, nested)
    table = patch.mock()
    if len(table) == 0:
        click.echo("No music files found in src.")
        sys.exit(0)
    click.echo(
        tabulate.tabulate(
            table, headers=patch.table_headers, tablefmt=patch.table_format, maxcolwidths=30
        )
    )
    if not assume_yes:
        click.confirm("Do you want to continue?", abort=True)

    # Apply the patch.
    patch.apply()
    click.echo("Applied.")


@cli.command()
def embed_lrc():
    click.echo("TODO.")


def main():
    # Invoke the click group.
    cli()


if __name__ == "__main__":
    main()
