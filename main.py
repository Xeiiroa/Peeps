import argparse
import sys
import inspect
from utils import Feed as FEED
from database.data import data_commands as Settings
from database import create_database


def main():
    create_database()

    parser = argparse.ArgumentParser(description="Run Video Feed")
    parser.add_argument("--settings", help="allows changes to settings", type=str) #value = None when called
    args = parser.parse_args()
    
    if args.settings:
        settings = Settings()
        
        
        try:
            if hasattr(settings, args.settings):
                getattr(settings, args.settings)()    
            else:
                raise ValueError("Command does not exist")
        except Exception as e:
            print(f"Error: {e}")
        
        sys.exit()
              
    else:
        feed = FEED()
        feed.get_livefeed()
    
    
if __name__ == "__main__":
    main()
    
    