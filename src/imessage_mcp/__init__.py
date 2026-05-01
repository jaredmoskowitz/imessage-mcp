try:
    from imessage_mcp.server import mcp
except ModuleNotFoundError:
    mcp = None  # type: ignore[assignment]


def main():
    if mcp is None:
        raise ImportError("imessage_mcp.server is not available")
    mcp.run(transport="stdio")
