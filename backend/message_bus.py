from fastapi import WebSocket
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"❌ Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients."""
        if not self.active_connections:
            print("⚠️  No active connections to broadcast to")
            return

        # Ensure message is JSON-serializable
        if isinstance(message, str):
            try:
                message = json.loads(message)
            except:
                message = {"message": message}

        dead_connections = []
        for connection in self.active_connections:
            try:
                await asyncio.wait_for(connection.send_json(message), timeout=2.0)
            except asyncio.TimeoutError:
                print(f"⚠️  Connection timeout while broadcasting")
                dead_connections.append(connection)
            except Exception as e:
                print(f"⚠️  Error broadcasting to connection: {e}")
                dead_connections.append(connection)

        # Clean up dead connections
        for conn in dead_connections:
            self.disconnect(conn)

        print(f"✅ Broadcasted to {len(self.active_connections)} clients")

# Global instance
manager = ConnectionManager()
