"""
Root entrypoint for Render and local development.
Exports:
    app: FastAPI ASGI application for Render Web Service
    main: Function to start the application
"""
from bot.main import app, main

if __name__ == "__main__":
    main()
