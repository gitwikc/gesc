from util.args import read_args
from util.cvscroll import capture_video


def main():
    args = read_args()
    capture_video(
        touch_threshold=args.touch_thresh,
        scroll_speed=args.scroll,
        debug=args.debug
    )

if __name__ == '__main__':
    main()
