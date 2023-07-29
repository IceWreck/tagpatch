import functools
import click
import pathlib


def src(f):
    @click.option(
        "-s",
        "--src",
        required=False,
        default=pathlib.Path().resolve(),
        show_default=True,
        type=click.Path(exists=True, writable=True, path_type=pathlib.Path),
    )
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


def dst(f):
    @click.option(
        "-d",
        "--dst",
        required=False,
        type=click.Path(writable=True, path_type=pathlib.Path),
    )
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


def assume_yes(f):
    @click.option(
        "-y",
        "--assume-yes",
        required=False,
        default=False,
        is_flag=True,
    )
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


def nested(f):
    @click.option(
        "-n",
        "--nested",
        required=False,
        default=False,
        is_flag=True,
    )
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper
