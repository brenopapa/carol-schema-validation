import argparse

PARSER = argparse.ArgumentParser()

PARSER.add_argument(
    "-d", 
    "--default", 
    type=str, 
    help="Default tenant with default schema",
)
PARSER.add_argument(
    "-t", 
    "--target", 
    type=str, 
    help="Target tenant to compare with default schema",
)
PARSER.add_argument(
    "-c", 
    "--connector", 
    type=str, 
    help="Filter connector to check schema",
)