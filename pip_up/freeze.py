import os
import subprocess


class Freeze(object):
    """
    Handle getting information from 'pip freeze'
    """
    lines = []

    def get(self):
        output = subprocess.check_output(
            args=['pip', 'freeze'],
            cwd=os.getcwd(),
        )

        for i, line in enumerate(output.split('\n')):
            line = line.strip()
            self.lines.append(line)

    def write_to_clipboard(self, output):
        process = subprocess.Popen(
            'pbcopy', env={
                'LANG': 'en_US.UTF-8',
            },
            stdin=subprocess.PIPE,
        )
        process.communicate(output.encode('utf-8'))

    def find(self, pattern, clipboard=True):
        """ Find a pattern or package in pip list """
        FOUND = []

        # Get a pip freeze if we haven't already
        if not self.lines:
            self.get()

        for l in self.lines:
            if pattern in l:
                FOUND.append(l)

        if clipboard:
            # Write contents to clipboard
            self.write_to_clipboard("\n".join(FOUND))

        return FOUND
