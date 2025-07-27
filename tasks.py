import datetime
import shlex
import shutil
import sys
from pathlib import Path

from invoke import task
from invoke.main import program
from pelican import main as pelican_main
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

SETTINGS_FILE_BASE = "pelicanconf.py"
SETTINGS = DEFAULT_CONFIG.copy()
SETTINGS.update(get_settings_from_file(SETTINGS_FILE_BASE))

CONFIG = {
    "settings_base": SETTINGS_FILE_BASE,
    "settings_publish": "publishconf.py",
    # Output path. Can be absolute or relative to tasks.py. Default: 'output'
    "deploy_path": SETTINGS["OUTPUT_PATH"],
    # Github Pages configuration
    "github_pages_branch": "main",
    "commit_message": f"'Publish site on {datetime.date.today().isoformat()}'",
    # Host and port for `serve`
    "host": "localhost",
    "port": 8000,
}


@task
def clean(c):
    """Remove generated files"""
    deploy_path = Path(CONFIG["deploy_path"])
    if deploy_path.exists():
        shutil.rmtree(deploy_path)
        deploy_path.mkdir(parents=True, exist_ok=True)


@task
def build(c):
    """Build local version of site"""
    pelican_run(f"-s {CONFIG['settings_base']}")


@task
def rebuild(c):
    """`build` with the delete switch"""
    pelican_run(f"-d -s {CONFIG['settings_base']}")


@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    pelican_run(f"-r -s {CONFIG['settings_base']}")


@task
def serve(c):
    """Serve site at http://$HOST:$PORT/ (default is localhost:8000)"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG["deploy_path"],
        (CONFIG["host"], CONFIG["port"]),
        ComplexHTTPRequestHandler,
    )

    sys.stderr.write(f"Serving at {CONFIG['host']}:{CONFIG['port']} ...\n")
    server.serve_forever()


@task
def reserve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)


@task
def preview(c):
    """Build production version of site"""
    pelican_run(f"-s {CONFIG['settings_publish']}")


@task
def livereload(c):
    """Automatically reload browser tab upon file modification."""
    from livereload import Server

    build(c)
    server = Server()
    # Watch the base settings file
    server.watch(CONFIG["settings_base"], lambda: build(c))
    # Watch content source files
    content_file_extensions = [".md", ".rst"]
    for extension in content_file_extensions:
        content_blob = f"{SETTINGS['PATH']}/**/*{extension}"
        server.watch(content_blob, lambda: build(c))
    # Watch the theme's templates and static assets
    theme_path = SETTINGS["THEME"]
    server.watch(f"{theme_path}/templates/*.html", lambda: build(c))
    static_file_extensions = [".css", ".js"]
    for extension in static_file_extensions:
        static_file = f"{theme_path}/static/**/*{extension}"
        server.watch(static_file, lambda: build(c))
    # Serve output path on configured host and port
    server.serve(host=CONFIG["host"], port=CONFIG["port"], root=CONFIG["deploy_path"])


@task
def publish(c):
    """Publish to production via rsync"""
    pelican_run(f"-s {CONFIG['settings_publish']}")
    deploy_path = CONFIG["deploy_path"].rstrip("/") + "/"
    c.run(
        f'rsync --delete --exclude ".DS_Store" -pthrvz -c '
        f'-e "ssh -p {CONFIG["ssh_port"]}" '
        f"{deploy_path} {CONFIG['ssh_user']}@{CONFIG['ssh_host']}:{CONFIG['ssh_path']}"
    )


@task
def gh_pages(c):
    """Publish to GitHub Pages"""
    preview(c)
    c.run(
        f"ghp-import -b {CONFIG['github_pages_branch']} "
        f"-m {CONFIG['commit_message']} "
        f"{CONFIG['deploy_path']} -p"
    )


def pelican_run(cmd):
    cmd += " " + program.core.remainder  # allows to pass-through args to pelican
    pelican_main(shlex.split(cmd))
