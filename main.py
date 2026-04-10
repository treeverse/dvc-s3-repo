#! /usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import docker

dpath = Path(__file__).parent


class DockerBuilder:
    working_dir = Path("/dvc-s3-repo")
    volumes = {str(dpath.resolve()): {"bind": str(working_dir), "mode": "rw"}}

    def __init__(self, pkg: str, tag: str, target: Optional[str] = None):
        self.client = docker.from_env()
        self.dir = f"docker/{pkg}"
        self.pkg = pkg
        self.tag = tag
        self.target = target

    @staticmethod
    def _pretty_print(log: List[Dict[str, Any]]) -> None:
        for line in log:
            if "stream" in line:
                print(line["stream"], end="")
            elif "error" in line:
                print(line["error"], file=sys.stderr)
            else:
                print(line, file=sys.stderr)

    def build(self, **kwargs) -> docker.models.images.Image:
        print(f'* Building "{self.tag}" from "{self.dir}"')
        try:
            image, log = self.client.images.build(
                path=self.dir, tag=self.tag, target=self.target, **kwargs
            )

        except docker.errors.BuildError as exc:
            print("* Build failed: ")
            log = list(exc.build_log)
            self._pretty_print(log)
            raise
        finally:
            self._pretty_print(log)
        return image

    def run(
        self, command: str, auto_remove=True, volumes=None, working_dir=None, **kwargs
    ) -> int:
        """Runs the given command and returns the status code"""
        print(f"* Starting container {self.tag} with cmd: {command}")
        container = self.client.containers.run(
            self.tag,
            command=command,
            stdout=True,
            stderr=True,
            detach=True,
            auto_remove=auto_remove,
            volumes=volumes or self.volumes,
            working_dir=str(working_dir) if working_dir else str(self.working_dir),
            **kwargs,
        )

        for line in container.logs(stream=True):
            print(line.strip().decode("UTF-8"))

        status = container.wait()
        ret = status["StatusCode"]
        if ret != 0:
            print(f"Failed to run {command!r} for {self.pkg} package", file=sys.stderr)
        return ret


def test(pkg):
    image = DockerBuilder(pkg=pkg, tag=f"dvc-s3-repo-{pkg}", target="pyenv")
    return image.run(command=f"./test.sh {pkg}")


def upload(pkg):
    env_passthrough = [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_SESSION_TOKEN",
        "AWS_DEFAULT_REGION",
        "AWS_S3_BUCKET",
        "AWS_S3_PREFIX",
        "GPG_ITERATIVE_ASC",
        "GPG_ITERATIVE_PASS",
    ]
    image = DockerBuilder(pkg=pkg, tag=f"dvc-{pkg}", target="uploader")
    image.build()
    return image.run(
        command="./upload.sh",
        working_dir=image.working_dir / image.pkg,
        environment={key: os.environ.get(key) for key in env_passthrough},
    )


def build(pkg):
    image = DockerBuilder(pkg=pkg, tag=f"dvc-s3-repo-{pkg}", target="builder")
    image.build()

    (dpath / "dvc" / "dvc" / "_build.py").write_text(f'PKG = "{pkg}"')
    return image.run(command=f"./build.sh {pkg}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    for func in [test, upload, build]:
        name = func.__name__
        subparser = subparsers.add_parser(name)
        subparser.add_argument("pkg", choices=["deb", "rpm"], help="package type")
        subparser.set_defaults(func=func)

    args = parser.parse_args()
    sys.exit(args.func(args.pkg))
