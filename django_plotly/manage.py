#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
from main.views import launch_streamlit

def main():
    # Add the project directory to Python path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_dir)
    
    # Start Streamlit in a separate thread
    streamlit_thread = threading.Thread(target=launch_streamlit)
    streamlit_thread.daemon = True
    streamlit_thread.start()

    # Run Django server
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'este.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
