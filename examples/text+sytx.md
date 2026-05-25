# `text+sytx` bucket — worked examples

Combined: textual content differs AND code structure differs.

Auto-label vocabulary: **pick-a / pick-b / combine / custom / empty / marker-echo** describe what shape the model output is. Length ratios flag over- or under-generation vs the ground truth.

---

## Both models solve (at least one skill version)

### Case `0xfee37adb6b4a151d`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.710)</th>
<th align="left">v2-sys (max=0.422)</th>
<th align="left">v2.1-sys (max=0.576)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
from distutils import debug
from distutils.log import WARN
from distutils.errors import DistutilsTemplateError
from distutils.filelist import glob_to_re, translate_pattern, FileList

from test.support import captured_stdout, run_unittest
from distutils.tests import support

MANIFEST_IN = """\
include ok
include xo
exclude xo
include foo.tmp
include buildout.cfg
global-include *.x
global-include *.txt
global-exclude *.tmp
recursive-include f *.oo
recursive-exclude global *.x
graft dir
prune dir3
"""


def make_local_path(s):
    """Converts '/' in a string to os.sep"""
    return s.replace('/', os.sep)
=======
>>>>>>> b

```

</td>
<td valign="top">

```python
"""Tests for distutils.filelist."""
import unittest
from distutils import debug
from distutils.log import WARN
from distutils.errors import DistutilsTemplateError
from distutils.filelist import glob_to_re, translate_pattern, FileList

from test.support import captured_stdout, run_unittest
from distutils.tests import support

MANIFEST_IN = """\
include ok
include xo
exclude xo
include foo.tmp
include buildout.cfg
global-include *.x
global-include *.txt
global-exclude *.tmp
recursive-include f *.oo
recursive-exclude global *.x
graft dir
prune dir3
"""

def make_local_path(s):
    """Converts '/' in a string to os.sep"""
    return s.replace('/', os.sep)

class FileListTestCase(unittest.TestCase):
    def test_manifest_in(self):
        fl = FileList()
        fl.read_manifest(MANIFEST_IN)
        self.assertEqual(fl.files, [
            'ok', 'xo', 'foo.tmp', 'buildout.cfg', '*.x', '*.txt', '*.tmp', 'f/*.oo'
        ])
        self.assertEqual(fl.excludes, ['xo', '*.tmp'])
        self.assertEqual(fl.includes, ['ok', 'foo.tmp', 'buildout.cfg', '*.x', '*.txt', 'f/*.oo'])
        self.assertEqual(fl.recursive_includes, ['f/*.oo'])
        self.assertEqual(fl.recursive_excludes, ['global/*.x'])
        self.assertEqual(fl.grafts, ['dir'])
        self.assertEqual(fl.prunes, ['dir3'])
```

</td>
<td valign="top">

```python
from distutils.filelist import glob_to_re, translate_pattern, FileList

from test.support import captured_stdout, run_unittest
from distutils import debug

class FileListTestCase(unittest.TestCase):
    def test_manifest_in(self):
        # Test case for MANIFEST_IN
        # This test case is not fully implemented yet.
        # It will be added in the future.
        pass
```

</td>
<td valign="top">

```python
from distutils.filelist import glob_to_re, translate_pattern, FileList

from test.support import captured_stdout, run_unittest
from distutils import debug

class FileListTestCase(unittest.TestCase):
    def test_manifest_in(self):
        # Test parsing of MANIFEST.in
        manifest = """\
include ok
include xo
exclude xo
include foo.tmp
include buildout.cfg
global-include *.x
global-include *.txt
global-exclude *.tmp
recursive-include f *.oo
recursive-exclude global *.x
graft dir
prune dir3
"""
        filelist = FileList()
        filelist.read_manifest(manifest)
        self.assertEqual(filelist.includes, ['ok', 'xo', 'foo.tmp', 'buildout.cfg'])
        self.assertEqual(filelist.excludes, ['xo'])
        self.assertEqual(filelist.recursive_includes, [('f', '*.oo')])
        self.assertEqual(filelist.recursive_excludes, [('global', '*.x')])
        self.assertEqual(filelist.grafts, ['dir'])
        self.assertEqual(filelist.prunes, ['dir3'])
```

</td>
<td valign="top">

```python
import unittest
from distutils import debug
from distutils.log import WARN
from distutils.errors import DistutilsTemplateError
from distutils.filelist import glob_to_re, translate_pattern, FileList

from test.support import captured_stdout, run_unittest
from distutils.tests import support

MANIFEST_IN = """\
include ok
include xo
exclude xo
include foo.tmp
include buildout.cfg
global-include *.x
global-include *.txt
global-exclude *.tmp
recursive-include f *.oo
recursive-exclude global *.x
graft dir
prune dir3
"""


def make_local_path(s):
    """Converts '/' in a string to os.sep"""
    return s.replace('/', os.sep)
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 2.1× over-gen &nbsp;·&nbsp; max=**0.710**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.422**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 1.5× over-gen &nbsp;·&nbsp; max=**0.576**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.914)</th>
<th align="left">v2-sys (max=0.537)</th>
<th align="left">v2.1-sys (max=0.995)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
from distutils import debug
from distutils.log import WARN
from distutils.errors import DistutilsTemplateError
from distutils.filelist import glob_to_re, translate_pattern, FileList

from test.support import captured_stdout, run_unittest
from distutils.tests import support

MANIFEST_IN = """\
include ok
include xo
exclude xo
include foo.tmp
include buildout.cfg
global-include *.x
global-include *.txt
global-exclude *.tmp
recursive-include f *.oo
recursive-exclude global *.x
graft dir
prune dir3
"""


def make_local_path(s):
    """Converts '/' in a string to os.sep"""
    return s.replace('/', os.sep)
=======
>>>>>>> b

```

</td>
<td valign="top">

```python
from distutils.filelist import glob_to_re, translate_pattern, FileList
from test.support import captured_stdout, run_unittest
from distutils import debug
from distutils.log import WARN
from distutils.errors import DistutilsTemplateError

class FileListTestCase(unittest.TestCase):
    MANIFEST_IN = """\
include ok
include xo
exclude xo
include foo.tmp
include buildout.cfg
global-include *.x
global-include *.txt
global-exclude *.tmp
recursive-include f *.oo
recursive-exclude global *.x
graft dir
prune dir3
"""

    def make_local_path(self, s):
        """Converts '/' in a string to os.sep"""
        return s.replace('/', os.sep)
```

</td>
<td valign="top">

```python
from distutils.filelist import glob_to_re, translate_pattern, FileList
from test.support import captured_stdout, run_unittest
from distutils import debug
from distutils.log import WARN
from distutils.errors import DistutilsTemplateError

class FileListTestCase(unittest.TestCase):
    def test_filelist(self):
        pass
```

</td>
<td valign="top">

```python
from distutils import debug
from distutils.log import WARN
from distutils.errors import DistutilsTemplateError
from distutils.filelist import glob_to_re, translate_pattern, FileList

from test.support import captured_stdout, run_unittest
from distutils.tests import support

MANIFEST_IN = """\
include ok
include xo
exclude xo
include foo.tmp
include buildout.cfg
global-include *.x
global-include *.txt
global-exclude *.tmp
recursive-include f *.oo
recursive-exclude global *.x
graft dir
prune dir3
"""


def make_local_path(s):
    """Converts '/' in a string to os.sep"""
    return s.replace('/', os.sep)
```

</td>
<td valign="top">

```python
import unittest
from distutils import debug
from distutils.log import WARN
from distutils.errors import DistutilsTemplateError
from distutils.filelist import glob_to_re, translate_pattern, FileList

from test.support import captured_stdout, run_unittest
from distutils.tests import support

MANIFEST_IN = """\
include ok
include xo
exclude xo
include foo.tmp
include buildout.cfg
global-include *.x
global-include *.txt
global-exclude *.tmp
recursive-include f *.oo
recursive-exclude global *.x
graft dir
prune dir3
"""


def make_local_path(s):
    """Converts '/' in a string to os.sep"""
    return s.replace('/', os.sep)
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.914**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.537**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; max=**0.995**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

### Case `0xb1f8e2d8bce718cb`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.596)</th>
<th align="left">v2-sys (max=0.671)</th>
<th align="left">v2.1-sys (max=0.795)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
# Skip test if tk cannot be initialized.
from tkinter.test.support import check_tk_availability
check_tk_availability()

=======
>>>>>>> b
from _tkinter import TclError
```

</td>
<td valign="top">

```python
from _tkinter import TclError
from tkinter import ttk
from tkinter.test import runtktests
from tkinter.test.support import get_tk_root

try:
    # Skip this test if _tkinter wasn't built.
    support.import_module('_tkinter')

    # Skip test if tk cannot be initialized.
    from tkinter.test.support import check_tk_availability
    check_tk_availability()
except TclError:
    # If TclError occurs, skip the test.
    pass
else:
    # Run the tests if tk is available.
    runtktests()
```

</td>
<td valign="top">

```python
from test import support

# Skip this test if _tkinter wasn't built.
support.import_module('_tkinter')

from _tkinter import TclError
from tkinter import ttk
from tkinter.test import runtktests
from tkinter.test.support import get_tk_root

try:
    # Skip test if tk cannot be initialized.
    from tkinter.test.support import check_tk_availability
    check_tk_availability()
except TclError:
    pass
```

</td>
<td valign="top">

```python
from tkinter.test.support import check_tk_availability
check_tk_availability()

from _tkinter import TclError
```

</td>
<td valign="top">

```python

# Skip test if tk cannot be initialized.
from tkinter.test.support import check_tk_availability
check_tk_availability()

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 4.0× over-gen &nbsp;·&nbsp; max=**0.596**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 3.3× over-gen &nbsp;·&nbsp; max=**0.671**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.795**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.380)</th>
<th align="left">v2-sys (max=0.816)</th>
<th align="left">v2.1-sys (max=0.699)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
# Skip test if tk cannot be initialized.
from tkinter.test.support import check_tk_availability
check_tk_availability()

=======
>>>>>>> b
from _tkinter import TclError
```

</td>
<td valign="top">

```python
from test import support

# Skip this test if _tkinter wasn't built.
support.import_module('_tkinter')

from _tkinter import TclError
from tkinter import ttk
from tkinter.test import runtktests
from tkinter.test.support import get_tk_root

try:
```

</td>
<td valign="top">

```python
# Skip test if tk cannot be initialized.
from tkinter.test.support import check_tk_availability
check_tk_availability()

from _tkinter import TclError
from tkinter import ttk
from tkinter.test import runtktests
from tkinter.test.support import get_tk_root

try:
```

</td>
<td valign="top">

```python
from test import support

# Skip this test if _tkinter wasn't built.
support.import_module('_tkinter')

# Skip test if tk cannot be initialized.
from tkinter.test.support import check_tk_availability
check_tk_availability()

from _tkinter import TclError
from tkinter import ttk
from tkinter.test import runtktests
from tkinter.test.support import get_tk_root

try:
```

</td>
<td valign="top">

```python

# Skip test if tk cannot be initialized.
from tkinter.test.support import check_tk_availability
check_tk_availability()

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 2.0× over-gen &nbsp;·&nbsp; max=**0.380**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; 2.2× over-gen &nbsp;·&nbsp; max=**0.816**

</td>
<td valign="top">

**pick-a** &nbsp;·&nbsp; 3.0× over-gen &nbsp;·&nbsp; max=**0.699**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

## Both models fail

### Case `0xa17ed9c50818a981`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.000)</th>
<th align="left">v2-sys (max=0.000)</th>
<th align="left">v2.1-sys (max=0.000)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
=======
# Only with Python implementation
def simplefind():
    """
    Test find methods using the elementpath fallback.

    >>> from xml.etree import ElementTree

    >>> CurrentElementPath = ElementTree.ElementPath
    >>> ElementTree.ElementPath = ElementTree._SimpleElementPath()
    >>> elem = ElementTree.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ElementTree.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ElementTree.ElementTree(elem).findtext("tag")
    'text'
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag']

    Path syntax doesn't work in this case.

    >>> elem.find("section/tag")
    >>> elem.findtext("section/tag")
    >>> summarize_list(elem.findall("section/tag"))
    []

    >>> ElementTree.ElementPath = CurrentElementPath
    """

def find():
    """
    Test find methods (including xpath syntax).

    >>> elem = ET.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.find("section/tag").tag
    'tag'
    >>> elem.find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("/tag").tag
    'tag'
    >>> elem[2] = ET.XML(SAMPLE_SECTION)
    >>> elem.find("section/nexttag").tag
    'nexttag'
    >>> ET.ElementTree(elem).find("section/tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tog")
    >>> ET.ElementTree(elem).find("tog/foo")
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("section/nexttag")
    ''
    >>> elem.findtext("section/nexttag", "default")
    ''
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("tag")
    'text'
    >>> ET.ElementTree(elem).findtext("tog/foo")
    >>> ET.ElementTree(elem).findtext("tog/foo", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("./tag")
    'text'
    >>> ET.ElementTree(elem).findtext("/tag")
    'text'
    >>> elem.findtext("section/tag")
    'subtext'
    >>> ET.ElementTree(elem).findtext("section/tag")
    'subtext'
    >>> summarize_list(elem.findall("."))
    ['body']
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("tog"))
    []
    >>> summarize_list(elem.findall("tog/foo"))
    []
    >>> summarize_list(elem.findall("*"))
    ['tag', 'tag', 'section']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("section/tag"))
    ['tag']
    >>> summarize_list(elem.findall("section//tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("section/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("section//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("section/.//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("*//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/tag"))
    ['tag']
    >>> summarize_list(elem.findall("*/./tag"))
    ['tag']
    >>> summarize_list(elem.findall("./tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("././tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class]"))
    ['tag', 'tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class='a']"))
    ['tag']
    >>> summarize_list(elem.findall(".//tag[@class='b']"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@id]"))
    ['tag']
    >>> summarize_list(elem.findall(".//section[tag]"))
    ['section']
    >>> summarize_list(elem.findall(".//section[element]"))
    []
    >>> summarize_list(elem.findall("../tag"))
    []
    >>> summarize_list(elem.findall("section/../tag"))
    ['tag', 'tag']
    >>> summarize_list(ET.ElementTree(elem).findall("./tag"))
    ['tag', 'tag']

    Following example is invalid in 1.2.
    A leading '*' is assumed in 1.3.

    >>> elem.findall("section//") == elem.findall("section//*")
    True

    ET's Path module handles this case incorrectly; this gives
    a warning in 1.3, and the behaviour will be modified in 1.4.

    >>> summarize_list(ET.ElementTree(elem).findall("/tag"))
    ['tag', 'tag']

    >>> elem = ET.XML(SAMPLE_XML_NS)
    >>> summarize_list(elem.findall("tag"))
    []
    >>> summarize_list(elem.findall("{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    >>> summarize_list(elem.findall(".//{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    """

>>>>>>> b
def file_init():
```

</td>
<td valign="top">

```python
'<tag>hello</tag>'
    >>> serialize(ET.XML("<tag><![CDATA[hello]]></tag>"))
    '<tag>hello</tag>'
    """

<<<<<<< a
=======
# Only with Python implementation
def simplefind():
    """
    Test find methods using the elementpath fallback.

    >>> from xml.etree import ElementTree

    >>> CurrentElementPath = ElementTree.ElementPath
    >>> ElementTree.ElementPath = ElementTree._SimpleElementPath()
    >>> elem = ElementTree.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ElementTree.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ElementTree.ElementTree(elem).findtext("tag")
    'text'
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag']

    Path syntax doesn't work in this case.

    >>> elem.find("section/tag")
    >>> elem.findtext("section/tag")
    >>> summarize_list(elem.findall("section/tag"))
    []

    >>> ElementTree.ElementPath = CurrentElementPath
    """

def find():
    """
    Test find methods (including xpath syntax).

    >>> elem = ET.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.find("section/tag").tag
    'tag'
    >>> elem.find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("/tag").tag
    'tag'
    >>> elem[2] = ET.XML(SAMPLE_SECTION)
    >>> elem.find("section/nexttag").tag
    'nexttag'
    >>> ET.ElementTree(elem).find("section/tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tog")
    >>> ET.ElementTree(elem).find("tog/foo")
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("section/nexttag")
    ''
    >>> elem.findtext("section/nexttag", "default")
    ''
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("tag")
    'text'
    >>> ET.ElementTree(elem).findtext("tog/foo")
    >>> ET.ElementTree(elem).findtext("tog/foo", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("./tag")
    'text'
    >>> ET.ElementTree(elem).findtext("/tag")
    'text'
    >>> elem.findtext("section/tag")
    'subtext'
    >>> ET.ElementTree(elem).findtext("section/tag")
    'subtext'
    >>> summarize_list(elem.findall("."))
    ['body']
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("tog"))
    []
    >>> summarize_list(elem.findall("tog/foo"))
    []
    >>> summarize_list(elem.findall("*"))
    ['tag', 'tag', 'section']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("section/tag"))
    ['tag']
    >>> summarize_list(elem.findall("section//tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("section/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("section//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("section/.//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("*//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/tag"))
    ['tag']
    >>> summarize_list(elem.findall("*/./tag"))
    ['tag']
    >>> summarize_list(elem.findall("./tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("././tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class]"))
    ['tag', 'tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class='a']"))
    ['tag']
    >>> summarize_list(elem.findall(".//tag[@class='b']"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@id]"))
    ['tag']
    >>> summarize_list(elem.findall(".//section[tag]"))
    ['section']
    >>> summarize_list(elem.findall(".//section[element]"))
    []
    >>> summarize_list(elem.findall("../tag"))
    []
    >>> summarize_list(elem.findall("section/../tag"))
    ['tag', 'tag']
    >>> summarize_list(ET.ElementTree(elem).findall("./tag"))
    ['tag', 'tag']

    Following example is invalid in 1.2.
    A leading '*' is assumed in 1.3.

    >>> elem.findall("section//") == elem.findall("section//*")
    True

    ET's Path module handles this case incorrectly; this gives
    a warning in 1.3, and the behaviour will be modified in 1.4.

    >>> summarize_list(ET.ElementTree(elem).findall("/tag"))
    ['tag', 'tag']

    >>> elem = ET.XML(SAMPLE_XML_NS)
    >>> summarize_list(elem.findall("tag"))
    []
    >>> summarize_list(elem.findall("{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    >>> summarize_list(elem.findall(".//{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    """

def file_init():
    """
    >>> import io

    >>> stringfile = io.BytesIO(SAMPLE_XML.encode("utf-8"))
    >>> tree = ET.ElementTree(file=stringfile)
    """
```

</td>
<td valign="top">

```python
def simplefind():
    """
    Test find methods using the elementpath fallback.

    >>> from xml.etree import ElementTree

    >>> CurrentElementPath = ElementTree.ElementPath
    >>> ElementTree.ElementPath = ElementTree._SimpleElementPath()
    >>> elem = ElementTree.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ElementTree.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ElementTree.ElementTree(elem).findtext("tag")
    'text'
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag']

    Path syntax doesn't work in this case.

    >>> elem.find("section/tag")
    >>> elem.findtext("section/tag")
    >>> summarize_list(elem.findall("section/tag"))
    []

    >>> ElementTree.ElementPath = CurrentElementPath
    """

def find():
    """
    Test find methods (including xpath syntax).

    >>> elem = ET.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.find("section/tag").tag
    'tag'
    >>> elem.find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("/tag").tag
    'tag'
    >>> elem[2] = ET.XML(SAMPLE_SECTION)
    >>> elem.find("section/nexttag").tag
    'nexttag'
    >>> ET.ElementTree(elem).find("section/tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tog")
    >>> ET.ElementTree(elem).find("tog/foo")
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("section/nexttag")
    ''
    >>> elem.findtext("section/nexttag", "default")
    ''
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("tag")
    'text'
    >>> ET.ElementTree(elem).findtext("tog/foo")
    >>> ET.ElementTree(elem).findtext("tog/foo", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("./tag")
    'text'
    >>> ET.ElementTree(elem).findtext("/tag")
    'text'
    >>> elem.findtext("section/tag")
    'subtext'
    >>> ET.ElementTree(elem).findtext("section/tag")
    'subtext'
    >>> summarize_list(elem.findall("."))
    ['body']
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("tog"))
    []
    >>> summarize_list(elem.findall("tog/foo"))
    []
    >>> summarize_list(elem.findall("*"))
    ['tag', 'tag', 'section']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("section/tag"))
    ['tag']
    >>> summarize_list(elem.findall("section//tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("section/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("section//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("section/.//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("*//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/tag"))
    ['tag']
    >>> summarize_list(elem.findall("*/./tag"))
    ['tag']
    >>> summarize_list(elem.findall("./tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("././tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class]"))
    ['tag', 'tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class='a']"))
    ['tag']
    >>> summarize_list(elem.findall(".//tag[@class='b']"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@id]"))
    ['tag']
    >>> summarize_list(elem.findall(".//section[tag]"))
    ['section']
    >>> summarize_list(elem.findall(".//section[element]"))
    []
    >>> summarize_list(elem.findall("../tag"))
    []
    >>> summarize_list(elem.findall("section/../tag"))
    ['tag', 'tag']
    >>> summarize_list(ET.ElementTree(elem).findall("./tag"))
    ['tag', 'tag']

    Following example is invalid in 1.2.
    A leading '*' is assumed in 1.3.

    >>> elem.findall("section//") == elem.findall("section//*")
    True

    ET's Path module handles this case incorrectly; this gives
    a warning in 1.3, and the behaviour will be modified in 1.4.

    >>> summarize_list(ET.ElementTree(elem).findall("/tag"))
    ['tag', 'tag']

    >>> elem = ET.XML(SAMPLE_XML_NS)
    >>> summarize_list(elem.findall("tag"))
    []
    >>> summarize_list(elem.findall("{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    >>> summarize_list(elem.findall(".//{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    """

def file_init():
    """
    >>> import io

    >>> stringfile = io.BytesIO(SAMPLE_XML.encode("utf-8"))
    >>> tree = ET.ElementTree(file=stringfile)
    """
```

</td>
<td valign="top">

```python
def simplefind():
    """
    Test find methods using the elementpath fallback.

    >>> from xml.etree import ElementTree

    >>> CurrentElementPath = ElementTree.ElementPath
    >>> ElementTree.ElementPath = ElementTree._SimpleElementPath()
    >>> elem = ElementTree.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ElementTree.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ElementTree.ElementTree(elem).findtext("tag")
    'text'
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag']

    Path syntax doesn't work in this case.

    >>> elem.find("section/tag")
    >>> elem.findtext("section/tag")
    >>> summarize_list(elem.findall("section/tag"))
    []

    >>> ElementTree.ElementPath = CurrentElementPath
    """

def find():
    """
    Test find methods (including xpath syntax).

    >>> elem = ET.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.find("section/tag").tag
    'tag'
    >>> elem.find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("/tag").tag
    'tag'
    >>> elem[2] = ET.XML(SAMPLE_SECTION)
    >>> elem.find("section/nexttag").tag
    'nexttag'
    >>> ET.ElementTree(elem).find("section/tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tog")
    >>> ET.ElementTree(elem).find("tog/foo")
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("section/nexttag")
    ''
    >>> elem.findtext("section/nexttag", "default")
    ''
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("tag")
    'text'
    >>> ET.ElementTree(elem).findtext("tog/foo")
    >>> ET.ElementTree(elem).findtext("tog/foo", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("./tag")
    'text'
    >>> ET.ElementTree(elem).findtext("/tag")
    'text'
    >>> elem.findtext("section/tag")
    'subtext'
    >>> ET.ElementTree(elem).findtext("section/tag")
    'subtext'
    >>> summarize_list(elem.findall("."))
    ['body']
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("tog"))
    []
    >>> summarize_list(elem.findall("tog/foo"))
    []
    >>> summarize_list(elem.findall("*"))
    ['tag', 'tag', 'section']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("section/tag"))
    ['tag']
    >>> summarize_list(elem.findall("section//tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("section/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("section//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("section/.//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("*//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/tag"))
    ['tag']
    >>> summarize_list(elem.findall("*/./tag"))
    ['tag']
    >>> summarize_list(elem.findall("./tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("././tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class]"))
    ['tag', 'tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class='a']"))
    ['tag']
    >>> summarize_list(elem.findall(".//tag[@class='b']"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@id]"))
    ['tag']
    >>> summarize_list(elem.findall(".//section[tag]"))
    ['section']
    >>> summarize_list(elem.findall(".//section[element]"))
    []
    >>> summarize_list(elem.findall("../tag"))
    []
    >>> summarize_list(elem.findall("section/../tag"))
    ['tag', 'tag']
    >>> summarize_list(ET.ElementTree(elem).findall("./tag"))
    ['tag', 'tag']

    Following example is invalid in 1.2.
    A leading '*' is assumed in 1.3.

    >>> elem.findall("section//") == elem.findall("section//*")
    True

    ET's Path module handles this case incorrectly; this gives
    a warning in 1.3, and the behaviour will be modified in 1.4.

    >>> summarize_list(ET.ElementTree(elem).findall("/tag"))
    ['tag', 'tag']

    >>> elem = ET.XML(SAMPLE_XML_NS)
    >>> summarize_list(elem.findall("tag"))
    []
    >>> summarize_list(elem.findall("{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    >>> summarize_list(elem.findall(".//{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    """

def file_init():
    """
    >>> import io

    >>> stringfile = io.BytesIO(SAMPLE_XML.encode("utf-8"))
    >>> tree = ET.ElementTree(file=stringfile)
    """
```

</td>
<td valign="top">

```python

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**marker-echo** &nbsp;·&nbsp; 5244.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 5083.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 5083.0× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.000)</th>
<th align="left">v2-sys (max=0.000)</th>
<th align="left">v2.1-sys (max=0.000)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
=======
# Only with Python implementation
def simplefind():
    """
    Test find methods using the elementpath fallback.

    >>> from xml.etree import ElementTree

    >>> CurrentElementPath = ElementTree.ElementPath
    >>> ElementTree.ElementPath = ElementTree._SimpleElementPath()
    >>> elem = ElementTree.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ElementTree.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ElementTree.ElementTree(elem).findtext("tag")
    'text'
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag']

    Path syntax doesn't work in this case.

    >>> elem.find("section/tag")
    >>> elem.findtext("section/tag")
    >>> summarize_list(elem.findall("section/tag"))
    []

    >>> ElementTree.ElementPath = CurrentElementPath
    """

def find():
    """
    Test find methods (including xpath syntax).

    >>> elem = ET.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.find("section/tag").tag
    'tag'
    >>> elem.find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("/tag").tag
    'tag'
    >>> elem[2] = ET.XML(SAMPLE_SECTION)
    >>> elem.find("section/nexttag").tag
    'nexttag'
    >>> ET.ElementTree(elem).find("section/tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tog")
    >>> ET.ElementTree(elem).find("tog/foo")
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("section/nexttag")
    ''
    >>> elem.findtext("section/nexttag", "default")
    ''
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("tag")
    'text'
    >>> ET.ElementTree(elem).findtext("tog/foo")
    >>> ET.ElementTree(elem).findtext("tog/foo", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("./tag")
    'text'
    >>> ET.ElementTree(elem).findtext("/tag")
    'text'
    >>> elem.findtext("section/tag")
    'subtext'
    >>> ET.ElementTree(elem).findtext("section/tag")
    'subtext'
    >>> summarize_list(elem.findall("."))
    ['body']
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("tog"))
    []
    >>> summarize_list(elem.findall("tog/foo"))
    []
    >>> summarize_list(elem.findall("*"))
    ['tag', 'tag', 'section']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("section/tag"))
    ['tag']
    >>> summarize_list(elem.findall("section//tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("section/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("section//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("section/.//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("*//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/tag"))
    ['tag']
    >>> summarize_list(elem.findall("*/./tag"))
    ['tag']
    >>> summarize_list(elem.findall("./tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("././tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class]"))
    ['tag', 'tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class='a']"))
    ['tag']
    >>> summarize_list(elem.findall(".//tag[@class='b']"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@id]"))
    ['tag']
    >>> summarize_list(elem.findall(".//section[tag]"))
    ['section']
    >>> summarize_list(elem.findall(".//section[element]"))
    []
    >>> summarize_list(elem.findall("../tag"))
    []
    >>> summarize_list(elem.findall("section/../tag"))
    ['tag', 'tag']
    >>> summarize_list(ET.ElementTree(elem).findall("./tag"))
    ['tag', 'tag']

    Following example is invalid in 1.2.
    A leading '*' is assumed in 1.3.

    >>> elem.findall("section//") == elem.findall("section//*")
    True

    ET's Path module handles this case incorrectly; this gives
    a warning in 1.3, and the behaviour will be modified in 1.4.

    >>> summarize_list(ET.ElementTree(elem).findall("/tag"))
    ['tag', 'tag']

    >>> elem = ET.XML(SAMPLE_XML_NS)
    >>> summarize_list(elem.findall("tag"))
    []
    >>> summarize_list(elem.findall("{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    >>> summarize_list(elem.findall(".//{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    """

>>>>>>> b
def file_init():
```

</td>
<td valign="top">

```python
def simplefind():
    """
    Test find methods using the elementpath fallback.

    >>> from xml.etree import ElementTree

    >>> CurrentElementPath = ElementTree.ElementPath
    >>> ElementTree.ElementPath = ElementTree._SimpleElementPath()
    >>> elem = ElementTree.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ElementTree.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ElementTree.ElementTree(elem).findtext("tag")
    'text'
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag']

    Path syntax doesn't work in this case.

    >>> elem.find("section/tag")
    >>> elem.findtext("section/tag")
    >>> summarize_list(elem.findall("section/tag"))
    []

    >>> ElementTree.ElementPath = CurrentElementPath
    """

def find():
    """
    Test find methods (including xpath syntax).

    >>> elem = ET.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.find("section/tag").tag
    'tag'
    >>> elem.find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("/tag").tag
    'tag'
    >>> elem[2] = ET.XML(SAMPLE_SECTION)
    >>> elem.find("section/nexttag").tag
    'nexttag'
    >>> ET.ElementTree(elem).find("section/tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tog")
    >>> ET.ElementTree(elem).find("tog/foo")
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("section/nexttag")
    ''
    >>> elem.findtext("section/nexttag", "default")
    ''
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("tag")
    'text'
    >>> ET.ElementTree(elem).findtext("tog/foo")
    >>> ET.ElementTree(elem).findtext("tog/foo", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("./tag")
    'text'
    >>> ET.ElementTree(elem).findtext("/tag")
    'text'
    >>> elem.findtext("section/tag")
    'subtext'
    >>> ET.ElementTree(elem).findtext("section/tag")
    'subtext'
    >>> summarize_list(elem.findall("."))
    ['body']
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("tog"))
    []
    >>> summarize_list(elem.findall("tog/foo"))
    []
    >>> summarize_list(elem.findall("*"))
    ['tag', 'tag', 'section']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("section/tag"))
    ['tag']
    >>> summarize_list(elem.findall("section//tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("section/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("section//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("section/.//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("*//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/tag"))
    ['tag']
    >>> summarize_list(elem.findall("*/./tag"))
    ['tag']
    >>> summarize_list(elem.findall("./tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("././tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class]"))
    ['tag', 'tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class='a']"))
    ['tag']
    >>> summarize_list(elem.findall(".//tag[@class='b']"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@id]"))
    ['tag']
    >>> summarize_list(elem.findall(".//section[tag]"))
    ['section']
    >>> summarize_list(elem.findall(".//section[element]"))
    []
    >>> summarize_list(elem.findall("../tag"))
    []
    >>> summarize_list(elem.findall("section/../tag"))
    ['tag', 'tag']
    >>> summarize_list(ET.ElementTree(elem).findall("./tag"))
    ['tag', 'tag']

    Following example is invalid in 1.2.
    A leading '*' is assumed in 1.3.

    >>> elem.findall("section//") == elem.findall("section//*")
    True

    ET's Path module handles this case incorrectly; this gives
    a warning in 1.3, and the behaviour will be modified in 1.4.

    >>> summarize_list(ET.ElementTree(elem).findall("/tag"))
    ['tag', 'tag']

    >>> elem = ET.XML(SAMPLE_XML_NS)
    >>> summarize_list(elem.findall("tag"))
    []
    >>> summarize_list(elem.findall("{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    >>> summarize_list(elem.findall(".//{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    """

def file_init():
    """
    >>> import io

    >>> stringfile = io.BytesIO(SAMPLE_XML.encode("utf-8"))
    >>> tree = ET.ElementTree(file=stringfile)
```

</td>
<td valign="top">

```python
def simplefind():
    """
    Test find methods using the elementpath fallback.

    >>> from xml.etree import ElementTree

    >>> CurrentElementPath = ElementTree.ElementPath
    >>> ElementTree.ElementPath = ElementTree._SimpleElementPath()
    >>> elem = ElementTree.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ElementTree.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ElementTree.ElementTree(elem).findtext("tag")
    'text'
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag']

    Path syntax doesn't work in this case.

    >>> elem.find("section/tag")
    >>> elem.findtext("section/tag")
    >>> summarize_list(elem.findall("section/tag"))
    []

    >>> ElementTree.ElementPath = CurrentElementPath
    """

def find():
    """
    Test find methods (including xpath syntax).

    >>> elem = ET.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.find("section/tag").tag
    'tag'
    >>> elem.find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("/tag").tag
    'tag'
    >>> elem[2] = ET.XML(SAMPLE_SECTION)
    >>> elem.find("section/nexttag").tag
    'nexttag'
    >>> ET.ElementTree(elem).find("section/tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tog")
    >>> ET.ElementTree(elem).find("tog/foo")
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("section/nexttag")
    ''
    >>> elem.findtext("section/nexttag", "default")
    ''
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("tag")
    'text'
    >>> ET.ElementTree(elem).findtext("tog/foo")
    >>> ET.ElementTree(elem).findtext("tog/foo", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("./tag")
    'text'
    >>> ET.ElementTree(elem).findtext("/tag")
    'text'
    >>> elem.findtext("section/tag")
    'subtext'
    >>> ET.ElementTree(elem).findtext("section/tag")
    'subtext'
    >>> summarize_list(elem.findall("."))
    ['body']
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("tog"))
    []
    >>> summarize_list(elem.findall("tog/foo"))
    []
    >>> summarize_list(elem.findall("*"))
    ['tag', 'tag', 'section']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("section/tag"))
    ['tag']
    >>> summarize_list(elem.findall("section//tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("section/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("section//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("section/.//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("*//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/tag"))
    ['tag']
    >>> summarize_list(elem.findall("*/./tag"))
    ['tag']
    >>> summarize_list(elem.findall("./tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("././tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class]"))
    ['tag', 'tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class='a']"))
    ['tag']
    >>> summarize_list(elem.findall(".//tag[@class='b']"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@id]"))
    ['tag']
    >>> summarize_list(elem.findall(".//section[tag]"))
    ['section']
    >>> summarize_list(elem.findall(".//section[element]"))
    []
    >>> summarize_list(elem.findall("../tag"))
    []
    >>> summarize_list(elem.findall("section/../tag"))
    ['tag', 'tag']
    >>> summarize_list(ET.ElementTree(elem).findall("./tag"))
    ['tag', 'tag']

    Following example is invalid in 1.2.
    A leading '*' is assumed in 1.3.

    >>> elem.findall("section//") == elem.findall("section//*")
    True

    ET's Path module handles this case incorrectly; this gives
    a warning in 1.3, and the behaviour will be modified in 1.4.

    >>> summarize_list(ET.ElementTree(elem).findall("/tag"))
    ['tag', 'tag']

    >>> elem = ET.XML(SAMPLE_XML_NS)
    >>> summarize_list(elem.findall("tag"))
    []
    >>> summarize_list(elem.findall("{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    >>> summarize_list(elem.findall(".//{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    """

def file_init():
    """
    >>> import io

    >>> stringfile = io.BytesIO(SAMPLE_XML.encode("utf-8"))
    >>> tree = ET.ElementTree(file=stringfile)
```

</td>
<td valign="top">

```python
'<tag>hello</tag>'
    >>> serialize(ET.XML("<tag><![CDATA[hello]]></tag>"))
    '<tag>hello</tag>'
    """

# Only with Python implementation
def simplefind():
    """
    Test find methods using the elementpath fallback.

    >>> from xml.etree import ElementTree

    >>> CurrentElementPath = ElementTree.ElementPath
    >>> ElementTree.ElementPath = ElementTree._SimpleElementPath()
    >>> elem = ElementTree.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ElementTree.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ElementTree.ElementTree(elem).findtext("tag")
    'text'
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag']

    Path syntax doesn't work in this case.

    >>> elem.find("section/tag")
    >>> elem.findtext("section/tag")
    >>> summarize_list(elem.findall("section/tag"))
    []

    >>> ElementTree.ElementPath = CurrentElementPath
    """

def find():
    """
    Test find methods (including xpath syntax).

    >>> elem = ET.XML(SAMPLE_XML)
    >>> elem.find("tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tag").tag
    'tag'
    >>> elem.find("section/tag").tag
    'tag'
    >>> elem.find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("./tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("/tag").tag
    'tag'
    >>> elem[2] = ET.XML(SAMPLE_SECTION)
    >>> elem.find("section/nexttag").tag
    'nexttag'
    >>> ET.ElementTree(elem).find("section/tag").tag
    'tag'
    >>> ET.ElementTree(elem).find("tog")
    >>> ET.ElementTree(elem).find("tog/foo")
    >>> elem.findtext("tag")
    'text'
    >>> elem.findtext("section/nexttag")
    ''
    >>> elem.findtext("section/nexttag", "default")
    ''
    >>> elem.findtext("tog")
    >>> elem.findtext("tog", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("tag")
    'text'
    >>> ET.ElementTree(elem).findtext("tog/foo")
    >>> ET.ElementTree(elem).findtext("tog/foo", "default")
    'default'
    >>> ET.ElementTree(elem).findtext("./tag")
    'text'
    >>> ET.ElementTree(elem).findtext("/tag")
    'text'
    >>> elem.findtext("section/tag")
    'subtext'
    >>> ET.ElementTree(elem).findtext("section/tag")
    'subtext'
    >>> summarize_list(elem.findall("."))
    ['body']
    >>> summarize_list(elem.findall("tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("tog"))
    []
    >>> summarize_list(elem.findall("tog/foo"))
    []
    >>> summarize_list(elem.findall("*"))
    ['tag', 'tag', 'section']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("section/tag"))
    ['tag']
    >>> summarize_list(elem.findall("section//tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall("section/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("section//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("section/.//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/*"))
    ['tag', 'nexttag', 'nextsection']
    >>> summarize_list(elem.findall("*//*"))
    ['tag', 'nexttag', 'nextsection', 'tag']
    >>> summarize_list(elem.findall("*/tag"))
    ['tag']
    >>> summarize_list(elem.findall("*/./tag"))
    ['tag']
    >>> summarize_list(elem.findall("./tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag"))
    ['tag', 'tag', 'tag', 'tag']
    >>> summarize_list(elem.findall("././tag"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class]"))
    ['tag', 'tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@class='a']"))
    ['tag']
    >>> summarize_list(elem.findall(".//tag[@class='b']"))
    ['tag', 'tag']
    >>> summarize_list(elem.findall(".//tag[@id]"))
    ['tag']
    >>> summarize_list(elem.findall(".//section[tag]"))
    ['section']
    >>> summarize_list(elem.findall(".//section[element]"))
    []
    >>> summarize_list(elem.findall("../tag"))
    []
    >>> summarize_list(elem.findall("section/../tag"))
    ['tag', 'tag']
    >>> summarize_list(ET.ElementTree(elem).findall("./tag"))
    ['tag', 'tag']

    Following example is invalid in 1.2.
    A leading '*' is assumed in 1.3.

    >>> elem.findall("section//") == elem.findall("section//*")
    True

    ET's Path module handles this case incorrectly; this gives
    a warning in 1.3, and the behaviour will be modified in 1.4.

    >>> summarize_list(ET.ElementTree(elem).findall("/tag"))
    ['tag', 'tag']

    >>> elem = ET.XML(SAMPLE_XML_NS)
    >>> summarize_list(elem.findall("tag"))
    []
    >>> summarize_list(elem.findall("{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    >>> summarize_list(elem.findall(".//{http://effbot.org/ns}tag"))
    ['{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag', '{http://effbot.org/ns}tag']
    """

def file_init():
    """
    >>> import io

    >>> stringfile = io.BytesIO(SAMPLE_XML.encode("utf-8"))
    >>> tree = ET.ElementTree(file=stringfile)
```

</td>
<td valign="top">

```python

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 5075.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 5075.0× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 5218.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

### Case `0x391d7c7eac3c3111`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.000)</th>
<th align="left">v2-sys (max=0.000)</th>
<th align="left">v2.1-sys (max=0.000)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
try:
<<<<<<< a
    import tables  # pylint:disable=g-import-not-at-top
=======
    import tables
>>>>>>> b
except ImportError:
    tables = None


```

</td>
<td valign="top">

```python
try:
    import h5py  # pylint:disable=g-import-not-at-top
except ImportError:
    h5py = None

try:
    import tables  # pylint:disable=g-import-not-at-top
except ImportError:
    tables = None


class HDF5Matrix(object):
    """Representation of HDF5 dataset to be used instead of a Numpy array.

    # Example
```

</td>
<td valign="top">

```python
try:
    import h5py  # pylint:disable=g-import-not-at-top
except ImportError:
    h5py = None

try:
    import tables  # pylint:disable=g-import-not-at-top
except ImportError:
    tables = None


class HDF5Matrix(object):
    """Representation of HDF5 dataset to be used instead of a Numpy array.

    # Example
```

</td>
<td valign="top">

```python
try:
    import h5py  # pylint:disable=g-import-not-at-top
except ImportError:
    h5py = None

try:
    import tables  # pylint:disable=g-import-not-at-top
except ImportError:
    tables = None


class HDF5Matrix(object):
    """Representation of HDF5 dataset to be used instead of a Numpy array.

    # Example
```

</td>
<td valign="top">

```python

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**combine** &nbsp;·&nbsp; 312.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**combine** &nbsp;·&nbsp; 312.0× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**combine** &nbsp;·&nbsp; 312.0× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.000)</th>
<th align="left">v2-sys (max=0.000)</th>
<th align="left">v2.1-sys (max=0.000)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
try:
<<<<<<< a
    import tables  # pylint:disable=g-import-not-at-top
=======
    import tables
>>>>>>> b
except ImportError:
    tables = None


```

</td>
<td valign="top">

```python
try:
    import tables  # pylint:disable=g-import-not-at-top
except ImportError:
    tables = None


class HDF5Matrix(object):
    """Representation of HDF5 dataset to be used instead of a Numpy array.

    # Example
```

</td>
<td valign="top">

```python
try:
    import tables  # pylint:disable=g-import-not-at-top
except ImportError:
    tables = None
```

</td>
<td valign="top">

```python
try:
    import tables  # pylint:disable=g-import-not-at-top
except ImportError:
    tables = None
```

</td>
<td valign="top">

```python

```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**combine** &nbsp;·&nbsp; 216.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**combine** &nbsp;·&nbsp; 98.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**combine** &nbsp;·&nbsp; 98.0× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---
