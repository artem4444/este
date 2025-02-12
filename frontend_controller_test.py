# Example usage in Python: use from web framework app
from frontend_controller import ReactFrontend, FrontendConfig

config = FrontendConfig(
    theme={
        "backgroundColor": "#ffffff",
        "primaryColor": "#007b00"
    },
    components={
        "showHeader": True,
        "showSidebar": False
    },
    layout={
        "containerWidth": "1200px"
    },
    custom_props={
        "apiEndpoint": "http://localhost:8000"
    }
)

# Method 1: Using context manager
with ReactFrontend("./frontend_react", port=3000) as frontend:
    frontend.configure(config)
    # Your backend code here
    input("Press Enter to stop the frontend server...")

# Method 2: Manual control
# frontend = ReactFrontend("./frontend", port=3000)
# frontend.configure(config)
# frontend.start()
# input("Press Enter to stop the frontend server...")
# frontend.stop()