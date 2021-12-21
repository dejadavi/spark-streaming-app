import spark_app.cli  as cli

# This hook file can be deployed to an s3/gcs, (or any  highly-available/persistent filestore.)
# "artifacts" bucket to invoke a pip-installed.
# python package deployed to a cluster pre-runtime via a bootstrap.

if __name__ == "__main__":

    cli.cli(standalone_mode=False)