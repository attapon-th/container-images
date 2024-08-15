#!/usr/bin/env python
import json
import sys
import docker
import re
import functools
import signal
from datetime import datetime
import tomllib
from typing import Dict, Union, List, Any

import docker.constants

jsonRegex = re.compile(r"^[\s]*{.*}[\s]*$")
numberRegex = re.compile(r"^\s*(\d+)%\s*$")

print = functools.partial(print, flush=True)
container = None
is_running = False


def main() -> None:
    """
    Main function to start the container.
    """
    global container, is_running
    try:
        stdinput = sys.stdin.readline()
        data = json.loads(stdinput)

        event_id = data["event"]
        docker_image = data["params"]["image"]
        container_name = data["params"]["name"]
        docker_command = data["params"]["cmd"]
        environment_variables = data["params"]["environ"].splitlines()
        docker_volumes = data["params"]["volume"].splitlines()
        container_auto_remove = True if data["params"]["auto_remove"] == 1 else False
        is_repull = True if data["params"]["repull"] == 1 else False
        is_annotate = True if data["params"]["annotate"] == 1 else False
        more_options = data["params"]["options"]

        environment_variables.append(f"CRONICLE_EVENT_ID={event_id}")

        image_registry: Union[dict, None] = None
        accept_option: List[str] = [
            "network",
            "network_mode",
            "network_disabled",
            "restart_policy",
            "labels",
            "hostname",
            "domainname",
            "working_dir",
            "entrypoint",
            "mem_limit",
            "memswap_limit",
            "dns",
            "extra_hosts",
        ]
        opts: Dict[str, Any] = {}
        try:
            toml_opt = tomllib.loads(more_options)
        except Exception as e:
            raise Exception(f"Invalid `Docker run Options` not format toml file error {e}")

        if toml_opt is not None:
            for k, v in toml_opt.items():
                if k == "registry":
                    image_registry = v
                if k in accept_option:
                    if isinstance(v, (str, dict, list)) and not v:
                        continue
                    opts[k] = v

        client: docker.DockerClient = docker.from_env()

        if is_repull:
            image_name, tag = docker_image.rsplit(":", 1) if ":" in docker_image else (docker_image, "latest")
            print(f"docker pull {image_name}:{tag}")
            if image_registry is not None and ("username" not in image_registry or "password" not in image_registry):
                image_registry = None
            client.images.pull(image_name, tag=tag, auth_config=image_registry)

        print(f"docker run {docker_image} {container_name} {docker_command}", file=sys.stdout, flush=True)
        container = client.containers.run(
            image=docker_image,
            name=container_name,
            command=docker_command,
            environment=environment_variables,
            volumes=docker_volumes,
            detach=True,
            tty=True,
            auto_remove=container_auto_remove,
            **opts,
        )  # type: ignore
        is_running = True
        # Register the signal handler
        signal.signal(signal.SIGTERM, handle_sigterm)

        print_container_logs(container, is_annotate)
        if container is not None:
            print(f"Container {container.name} stopped.")
            container_response = container.wait()
            code = container_response.get("StatusCode", 0)
            err_msg = container_response.get("Error", {}).get("Message", "Unknown error")
            if code != 0:
                raise Exception(err_msg)
            print(json.dumps({"complete": 1, "code": code, "description": err_msg}))
        else:
            print('{ "complete": 1 }')
    except KeyboardInterrupt:
        print(json.dumps({"complete": 1, "code": 99, "description": "KeyboardInterrupt"}))
    except Exception as e:
        print(json.dumps({"complete": 1, "code": 99, "description": str(e)}))
    finally:
        try:
            is_running = False
            container.stop() if container is not None else None
        except Exception as e:
            print(f"Failed to stop container: {e}")


def handle_sigterm(signum: int, _) -> None:
    """
    Handle SIGTERM signal by stopping the container gracefully.
    """
    global container
    if container is not None:
        try:
            container.stop()
        except Exception as e:
            print(f"Failed to stop container: {e}")


def print_container_logs(container, is_annotate: bool) -> None:
    """
    Print container logs with optional timestamp annotation.
    """
    logs = container.logs(stream=True, follow=True)
    progress = 0.0
    print(json.dumps({"progress": progress}))

    for log_line in logs:
        log_line = log_line.strip().decode("utf-8", errors="replace")
        if match := re.match(r"^\s*(\d+)%\s*$", log_line):
            progress = float(match.group(1)) / 100.0
            print(json.dumps({"progress": progress}))
            continue

        if is_annotate:
            datetime_now = datetime.now().isoformat(timespec="milliseconds")
            log_line = f"[{datetime_now}] {log_line}"

        print(log_line)


if __name__ == "__main__":
    main()
