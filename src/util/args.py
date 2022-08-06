import argparse

def read_args():
    parser = argparse.ArgumentParser(prog='Gescroll', description='One-handed gesture controller for mouse')
    parser.add_argument('--debug', '-d', action='store_true', default=False)
    parser.add_argument('--touch-thresh', '-t', type=int, default=70)
    parser.add_argument('--scroll', '-s', type=int, default=45)
    return parser.parse_args()
