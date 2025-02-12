# frontend_controller.py
from dataclasses import dataclass
from typing import Dict, Any, Optional
import json
from pathlib import Path
import subprocess
import os

@dataclass #simply for config list initialization: where User will add gui parameters
class FrontendConfig:
    """Configuration for the React frontend"""
    theme: Dict[str, str]  # Colors, fonts, etc.
    components: Dict[str, bool]  # Enable/disable components
    layout: Dict[str, Any]  # Layout configuration
    custom_props: Dict[str, Any]  # Additional custom properties



class ReactFrontend:
    def __init__(
        self,
        app_path: str,
        port: int = 3000,
        dev_mode: bool = True
    ):
        self.app_path = Path(app_path)
        self.port = port
        self.dev_mode = dev_mode
        self.config_path = self.app_path / 'src' / 'config.json'
        self._process = None

    #converts python list with dictionaries into a json
    def configure(self, config: FrontendConfig):
        """Update frontend configuration"""
        config_dict = {
            "theme": config.theme,
            "components": config.components,
            "layout": config.layout,
            "customProps": config.custom_props
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)




###### manage.py analogue for managing frontend app

    def start(self):
        """Start the React development server"""
        if self._process is not None:
            raise RuntimeError("Frontend is already running")

        env = os.environ.copy()
        env["PORT"] = str(self.port)
        
        if self.dev_mode:
            self._process = subprocess.Popen(
                ["npm", "start"],
                cwd=self.app_path,
                env=env
            )
        else:
            # Build and serve production version
            subprocess.run(["npm", "run", "build"], cwd=self.app_path)
            self._process = subprocess.Popen(
                ["npx", "serve", "-s", "build", "-l", str(self.port)],
                cwd=self.app_path,
                env=env
            )

    def stop(self):
        """Stop the frontend server"""
        if self._process is not None:
            self._process.terminate()
            self._process = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()