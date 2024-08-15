#!/usr/bin/env python
import json
import sys
import docker
import re
import functools
import signal
from datetime import datetime
import tomllib

jsonRegex = re.compile(r"^[\s]*{.*}[\s]*$")
numberRegex = re.compile(r"^\s*(\d+)%\s*$")

print = functools.partial(print, flush=True)
container = None
is_running = False


def print_logs(container, is_annotate=False):
    logs_stream = container.logs(stream=True, follow=True)
    progress = 0.0
    print(json.dumps({"progress": progress}))
    for line in logs_stream:
        line = line.strip().decode("utf-8", errors="replace")
        if numberRegex.match(line):
            if "%" in line:
                progress: float = float(line.replace("%", "")) / 100.0
                print(json.dumps({"progress": progress}))
                continue
        if is_annotate:
            dt_now = datetime.now().isoformat(timespec="milliseconds")
            line = f"[{dt_now}] {line}"
        print(line)


def handle_sigterm(signum, frame):
    global container
    if container is not None:
        print(f"Caught SIGTERM, stopping container: {container.name}")
        try:
            container.stop()  # Stop the container gracefully
        except:
            print(f"Container {container.name} not found. It might have already stopped or been removed.")


def main():
    global container, is_running  # Make container accessible to the signal handler
    try:
        stdinput = sys.stdin.readline()
        data = json.loads(stdinput)

        event_id = data["event"]
        docker_image = data["params"]["image"]
        contianer_name = data["params"]["name"]
        docker_command = data["params"]["cmd"]
        environment_variables = data["params"]["environ"].splitlines()
        docker_volumes = data["params"]["volume"].splitlines()
        container_auto_remove = data["params"]["auto_remove"]
        more_options = data["params"]["options"]
        is_repull = data["params"]["repull"]
        is_annotate = data["params"]["annotate"]

        accept_option = "network,network_mode,network_disabled,restart_policy,labels,hostname,domainname,working_dir,entrypoint,mem_limit,memswap_limit,dns,extra_hosts".split(",")
        opts = {}
        toml_opt = tomllib.loads(more_options)
        if toml_opt is not None:
            for k, v in toml_opt.items():
                if k in accept_option:
                    if isinstance(v, (str, dict, list)) and not v:
                        continue
                    opts[k] = v

        client: docker.DockerClient = docker.from_env()

        if is_repull:
            sp = docker_image.rsplit(":", 1)
            image_name: str = sp[0]
            tag = "latest"
            if len(sp) == 2:
                tag = sp[1]
            print(f"docker pull {image_name}:{tag}")
            client.images.pull(image_name, tag=tag)

        print(f"docker run {docker_image} {contianer_name} {docker_command}", file=sys.stdout, flush=True)
        container = client.containers.run(
            image=docker_image,
            name=contianer_name,
            command=docker_command,
            environment=environment_variables,
            volumes=docker_volumes,
            detach=True,
            auto_remove=True if container_auto_remove else False,
            **opts,
        )
        is_running = True
        # Register the signal handler
        signal.signal(signal.SIGTERM, handle_sigterm)

        print_logs(container, is_annotate=is_annotate)  # type: ignore
        if container is not None:
            print(f"Container {container.name} stopped.")
            container_response = container.wait()
            code = container_response.get("StatusCode")
            err = container_response.get("Error")
            if code != 0:
                err_msg = "Unknown error"
                if err is not None:
                    err_msg = err.get("Message")
                raise Exception(err_msg)
        print('{ "complete": 1 }')
    except Exception as e:
        print(json.dumps({"complete": 1, "code": 99, "description": str(e)}))
    except KeyboardInterrupt:
        print(json.dumps({"complete": 1, "code": 99, "description": "KeyboardInterrupt"}))
    finally:
        try:
            is_running = False
            container.stop()  # type: ignore
        except Exception as e:
            print(f"Failed to stop container: {e}")


if __name__ == "__main__":
    # asyncio.run(main())
    main()


# # Register the signal handler
# signal.signal(signal.SIGTERM, handle_sigterm)
