"""Tests for argument parsing and command construction in fledge-docker."""

import importlib.util
import importlib.machinery
from pathlib import Path

# Load the plugin script as a module (it has no .py extension).
_plugin_path = str(Path(__file__).resolve().parent.parent / "bin" / "fledge-docker")
_loader = importlib.machinery.SourceFileLoader("fledge_docker", _plugin_path)
_spec = importlib.util.spec_from_loader("fledge_docker", _loader, origin=_plugin_path)
fledge_docker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fledge_docker)


# --- parse_args ---


class TestParseArgs:
    def test_defaults(self):
        result = fledge_docker.parse_args([])
        assert result["sub"] == "build"
        assert result["json"] is False
        assert result["tag"] is None
        assert result["version"] == "latest"
        assert result["registry"] is None
        assert result["file"] == "Dockerfile"
        assert result["foreground"] is False
        assert result["extra"] == []

    def test_subcommand_push(self):
        result = fledge_docker.parse_args(["push"])
        assert result["sub"] == "push"

    def test_subcommand_up(self):
        result = fledge_docker.parse_args(["up", "--foreground"])
        assert result["sub"] == "up"
        assert result["foreground"] is True

    def test_subcommand_down(self):
        result = fledge_docker.parse_args(["down"])
        assert result["sub"] == "down"

    def test_subcommand_logs(self):
        result = fledge_docker.parse_args(["logs"])
        assert result["sub"] == "logs"

    def test_json_flag(self):
        result = fledge_docker.parse_args(["build", "--json"])
        assert result["json"] is True

    def test_tag_option(self):
        result = fledge_docker.parse_args(["build", "--tag", "myimage"])
        assert result["tag"] == "myimage"

    def test_version_option(self):
        result = fledge_docker.parse_args(["build", "--version", "v2.0.0"])
        assert result["version"] == "v2.0.0"

    def test_registry_option(self):
        result = fledge_docker.parse_args(["push", "--registry", "ghcr.io/org"])
        assert result["sub"] == "push"
        assert result["registry"] == "ghcr.io/org"

    def test_file_option(self):
        result = fledge_docker.parse_args(["build", "--file", "Dockerfile.prod"])
        assert result["file"] == "Dockerfile.prod"

    def test_unknown_args_go_to_extra(self):
        result = fledge_docker.parse_args(["build", "--unknown"])
        assert "--unknown" in result["extra"]

    def test_combined_flags(self):
        result = fledge_docker.parse_args([
            "push", "--registry", "ghcr.io/myorg",
            "--version", "v1.2.3", "--json"
        ])
        assert result["sub"] == "push"
        assert result["registry"] == "ghcr.io/myorg"
        assert result["version"] == "v1.2.3"
        assert result["json"] is True


# --- image_ref ---


class TestImageRef:
    def test_defaults_to_project_name(self):
        opts = {"tag": None, "version": "latest", "registry": None}
        assert fledge_docker.image_ref(opts, "myapp") == "myapp:latest"

    def test_tag_overrides_project(self):
        opts = {"tag": "custom", "version": "latest", "registry": None}
        assert fledge_docker.image_ref(opts, "myapp") == "custom:latest"

    def test_version(self):
        opts = {"tag": None, "version": "v1.0.0", "registry": None}
        assert fledge_docker.image_ref(opts, "svc") == "svc:v1.0.0"

    def test_registry_prefix(self):
        opts = {"tag": None, "version": "latest", "registry": "ghcr.io/org"}
        assert fledge_docker.image_ref(opts, "svc") == "ghcr.io/org/svc:latest"

    def test_registry_trailing_slash(self):
        opts = {"tag": None, "version": "latest", "registry": "ghcr.io/org/"}
        assert fledge_docker.image_ref(opts, "svc") == "ghcr.io/org/svc:latest"

    def test_fallback_name(self):
        opts = {"tag": None, "version": "latest", "registry": None}
        assert fledge_docker.image_ref(opts, None) == "app:latest"


# --- shell_quote ---


class TestShellQuote:
    def test_simple_string(self):
        assert fledge_docker.shell_quote("hello") == "'hello'"

    def test_string_with_spaces(self):
        assert fledge_docker.shell_quote("hello world") == "'hello world'"

    def test_string_with_single_quote(self):
        assert fledge_docker.shell_quote("it's") == "'it'\\''s'"

    def test_image_ref_with_colon(self):
        assert fledge_docker.shell_quote("myapp:v1.0") == "'myapp:v1.0'"
