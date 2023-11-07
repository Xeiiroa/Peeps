import argparse
import sys
from utils import Feed as feed
from database.data import data_commands as settings
from database import create_database


def main():
    create_database()
    
    
    parser = argparse.ArgumentParser(description="Run Video Feed")
    parser.add_argument("--settings")
    
    args = parser.parse_args()
    
    if args.settings:
        if len(args) !=2:
            settings()
            settings.help()
        
        else:
            settings()
            function_name = sys.argv[1]
            
            if hasattr(settings, function_name):
                selected_function = getattr(settings, function_name)
                
                if sys.argv[2] is not None:
                    selected_function(sys.argv[2])
                
                else:
                    selected_function()
            
            else:
                print(f"function{function_name} not found")
                sys.exit()
                    
    else:
        feed()
        feed.get_livefeed()
    
    
if __name__ == "__main__":
    main()
    
    