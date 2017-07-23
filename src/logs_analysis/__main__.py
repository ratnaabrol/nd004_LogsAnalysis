#!/usr/bin/env python3

"""Main script for the package. Will output text report to stdout."""

import logs_analysis.cmd_line_app as app


def main():
    """Main function to be run by this script."""
    app.CmdLineApp().run()


if __name__ == '__main__':
    main()
