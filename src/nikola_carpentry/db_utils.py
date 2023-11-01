import argparse
from nikola_carpentry import db, app



def reset_database():
    print("Dropping database...")
    with app.app_context():
        db.drop_all()
        print("Done!")
        
def build_database():
    print("Creating database...")
    with app.app_context():
        db.create_all()
        print("Done!")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    description='Database utilities for Nikola Custom Carpentry',
                    epilog='For help RTFM then email jon@jrickman.net')
    
    parser.add_argument('-d', '--drop', action='store_true', help="Drop databases")
    parser.add_argument('-c', '--create', action='store_true', help="Create databases")

    args = parser.parse_args()

    if args.create:
        build_database()

    if args.drop:
        reset_database()

    print("Done!")
