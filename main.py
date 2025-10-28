from mcp_sdk.mcp import MCPServer
from sefaria_jewish_library import sefaria_jewish_library

app = MCPServer(tools=[sefaria_jewish_library])
