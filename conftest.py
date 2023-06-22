import os
import sys

# Get the path of the root directory
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the root directory to the Python import path
sys.path.insert(0, root_path)
