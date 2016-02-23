import fnmatch
import os
import logging

logger = logging.getLogger(__name__)

class LinesOfCodeCounter(object):

    def __init__(self, folder):
        self.root_folder = folder
        self.code_files= ['*.vb', '*.cs', '*.xml', '*.xsd', '*.js', '*.xsx', '*.resx']

    def _walk_folders(self, root, patterns=['*'], recurse=True, ):
        for path, subdirs, files in os.walk(root):
            for name in files:
                found = False
                for pattern in patterns:
                    if fnmatch.fnmatch(name, pattern):
                        found = True
                        yield os.path.join(path, name)
                        break
                    if not found:
                        logger.debug('NOT Matched %s' % name)
            if not recurse:
                break

    def count(self):
        blank_count = 0
        content_count = 0
        results = list()

        for code_file in self._walk_folders(self.root_folder, self.code_files):
            for line in open(code_file).readlines():
                line = line.strip()
                if len(line) > 1:
                    content_count +=1
            logger.debug('File: %s lines: %s' % (code_file, content_count))
            results.append({'file': code_file,
                            'lines': content_count})
            content_count = 0
        return results
