import click
from job import Job
from settings import IN_PATH


@click.command()
@click.option('--in-path',"-p", default=IN_PATH,
              type=click.Path(exists=True),
              required=False,
              envvar="IN_PATH",
              help='HDFS-style path of the log files.')
def cli(in_path: str,) -> None:

    click.echo(f"Reading logs from {in_path}")

    Job.run(in_path)


if __name__ == '__main__':
    cli()