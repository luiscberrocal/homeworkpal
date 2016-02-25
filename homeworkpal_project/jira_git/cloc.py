import fnmatch
import os
import logging
import re

logger = logging.getLogger(__name__)


class LinesOfCodeCounter(object):

    def __init__(self, folder):
        self.excluded_folders = ['.git','dojo-release-1.10.3']
        self.root_folder = folder
        self.code_files=  ['*.vb', '*.cs', '*.xml', '*.xsd', '*.js',
                           '*.xsx', '*.resx', '*.vdproj', '*.vbproj', '*.csproj'
                           '*.json','*.html', '*.css', '*.cshtml', '*.less',
                           '*.sql', '*.xslt', '*.config', '*.txt']

        self.blacjk_list = {'*.js': [re.compile(r'jquery[-]?[\w\.-]*(\.js)'),
                                     re.compile(r'bootstrap-?(\.?\w+)*(\.js)'),
                                     re.compile(r'highcharts-?(\.\w+)*(\.js)'),
                                     re.compile(r'modernizr-?(\.?\w+)*(\.js)'),
                                     re.compile(r'^dataTables(\.\w+)*(\.js)$'),
                                     re.compile(r'^(googlemaps|arcgismaps|select2)(\.\w+)*(\.js)$'),
                                     ],
                            '*.xml': [re.compile(r'(NLog|nunit\.framework)\.xml'),
                                      re.compile(r'^Newtonsoft(\.\w+)+\.(xml|XML)$'),
                                      re.compile(r'^System(\.\w+)+\.(xml|XML)$'),
                                      re.compile(r'^Microsoft(\.\w+)+\.(xml|XML)$'),
                                      re.compile(r'^EntityFramework(\.\w+)*\.(xml)$'),
                                      re.compile(r'^Ninject(\.\w+)*\.(xml)$')],
                            '*.xsd': [re.compile(r'Nlog\.xsd'),],
                            '*.css': [re.compile(r'jquery[-]?[\w\.-]*(\.css)'),
                                     re.compile(r'bootstrap-?(\.\w+)*(\.css)'),
                                     re.compile(r'^dataTables(\.\w+)+\.(css)$'),
                                     ],

                            }

    def _is_black_listed(self, filename, pattern):
        black_list_regexps = self.blacjk_list.get(pattern, None)
        if black_list_regexps is None:
            return False
        for regexp in black_list_regexps:
            if regexp.match(filename):
                return True
        return False

    def _walk_folders(self, root, patterns=['*'], recurse=True, ):
        for path, subdirs, files in os.walk(root, topdown=True):
            subdirs[:] = [d for d in subdirs if d not in self.excluded_folders]
            for name in files:
                found = False
                for pattern in patterns:
                    if fnmatch.fnmatch(name, pattern):
                        if not self._is_black_listed(name, pattern):
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
            try:
                for line in open(code_file).readlines():
                    line = line.strip()
                    if len(line) > 1:
                        content_count +=1
                path, filename = os.path.split(code_file)
                _ , base_folder = os.path.split(self.root_folder)
                extension = os.path.splitext(code_file)[1].lower()
                logger.debug('File: %s lines: %s' % (code_file, content_count))
                results.append({'file': code_file,
                                'filename': filename,
                                'base_folder': base_folder,
                                'extension': extension,
                                'lines': content_count})
            except UnicodeDecodeError:
                logger.error('Unicode error with file %s' % code_file)
            content_count = 0
        return results
