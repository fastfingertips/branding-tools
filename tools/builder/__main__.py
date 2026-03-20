"""CLI Entry point for the release builder."""
import os
import argparse
from .builder import ReleaseBuilder

def main():
    """Entry point for the release builder."""
    parser = argparse.ArgumentParser(description='Build release packages for browser extensions')
    parser.add_argument('--path', help='Path to extension project (default: current dir)')
    parser.add_argument('--bump', choices=['major', 'minor', 'patch'], help='Bump version')
    parser.add_argument('--id', help='Firefox Gecko ID (e.g. app@example.com)')
    parser.add_argument('--no-firefox', action='store_true', help='Exclude Firefox package')
    parser.add_argument('--no-open', action='store_true', help='Do not open output folder')
    
    args = parser.parse_args()
    
    try:
        builder = ReleaseBuilder(project_root=args.path)
        
        if args.bump:
            old_v, new_v = builder.manifest.bump_version(args.bump)
            print(f"Version bumped: {old_v} -> {new_v}\n")
        
        result = builder.build_all(
            include_firefox=not args.no_firefox,
            gecko_id=args.id
        )
        builder.print_summary(result)
        
        if not args.no_open and os.name == 'nt':
            os.startfile(result['output_dir'])
    except Exception as e:
        print(f"Build failed: {e}")
        raise SystemExit(1)

if __name__ == '__main__':
    main()
