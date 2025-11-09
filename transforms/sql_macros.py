import jinja2
from pathlib import Path

def get_sql_path(directory: str, file_name: str) -> Path:
    """Get the path to a SQL file."""
    return Path(__file__).parent / "sql" / directory / f"{file_name}.sql"

def render_sql(sql_path: Path, **kwargs) -> str:
    """Render a Jinja2 SQL template."""
    with open(sql_path, "r") as f:
        template_str = f.read()

    # Create a Jinja2 environment with a custom trim function
    env = jinja2.Environment()
    env.globals['trim'] = lambda s: f"TRIM({s})"
    env.globals['source'] = lambda project, table: f"raw_{project}_{table}"

    template = env.from_string(template_str)
    return template.render(**kwargs)
