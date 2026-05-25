# `sytx` bucket — worked examples

**Syntactically-different code statements** without changing behaviour: variable renames, restructured imports, reorganised signatures.

Auto-label vocabulary: **pick-a / pick-b / combine / custom / empty / marker-echo** describe what shape the model output is. Length ratios flag over- or under-generation vs the ground truth.

---

## Both models solve (at least one skill version)

### Case `0x147e6bf42d889f40`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.420)</th>
<th align="left">v2-sys (max=0.514)</th>
<th align="left">v2.1-sys (max=0.514)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
from datetime import time, datetime, timedelta
=======
from datetime import time, datetime
>>>>>>> b
from itertools import izip
```

</td>
<td valign="top">

```python
# pylint: disable=E1101,E1103,W0232

from datetime import time, datetime
from itertools import izip
import numpy as np

from pandas.util.decorators import cache_readonly
import pandas.core.common as com
```

</td>
<td valign="top">

```python
from datetime import time, datetime
from itertools import izip
import numpy as np
from pandas.util.decorators import cache_readonly
from pandas.core.common import com
```

</td>
<td valign="top">

```python
from datetime import time, datetime
from itertools import izip
import numpy as np

from pandas.util.decorators import cache_readonly
from pandas.core.common import com
```

</td>
<td valign="top">

```python
from datetime import time, datetime, date
from itertools import izip
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 3.0× over-gen &nbsp;·&nbsp; max=**0.420**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 2.4× over-gen &nbsp;·&nbsp; max=**0.514**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 2.5× over-gen &nbsp;·&nbsp; max=**0.514**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.877)</th>
<th align="left">v2-sys (max=0.891)</th>
<th align="left">v2.1-sys (max=0.915)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
from datetime import time, datetime, timedelta
=======
from datetime import time, datetime
>>>>>>> b
from itertools import izip
```

</td>
<td valign="top">

```python
from datetime import time, datetime, timedelta
from itertools import izip
\
```

</td>
<td valign="top">

```python
from datetime import time, datetime, timedelta
from itertools import izip
```

</td>
<td valign="top">

```python
from datetime import time, datetime
from itertools import izip
```

</td>
<td valign="top">

```python
from datetime import time, datetime, date
from itertools import izip
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**combine** &nbsp;·&nbsp; max=**0.877**

</td>
<td valign="top">

**combine** &nbsp;·&nbsp; max=**0.891**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; max=**0.915**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

### Case `0x326f2cc83ba51580`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.689)</th>
<th align="left">v2-sys (max=0.804)</th>
<th align="left">v2.1-sys (max=0.804)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
=======
    from triton.fb import build_paths
    from triton.fb.build import _run_build_command

>>>>>>> b
    from torch._inductor.fb.utils import (
        log_global_cache_errors,
```

</td>
<td valign="top">

```python
_HERE = os.path.abspath(__file__)
_TORCH_PATH = os.path.dirname(os.path.dirname(_HERE))

if config.is_fbcode():
    from triton.fb import build_paths
    from triton.fb.build import _run_build_command
    from torch._inductor.fb.utils import (
        log_global_cache_errors,
        log_global_cache_stats,
        log_global_cache_vals,
        use_global_cache,
    )
```

</td>
<td valign="top">

```python
from triton.fb import build_paths
from triton.fb.build import _run_build_command

from torch._inductor.fb.utils import (
    log_global_cache_errors,
    log_global_cache_stats,
    log_global_cache_vals,
    use_global_cache,
)
```

</td>
<td valign="top">

```python
from triton.fb import build_paths
from triton.fb.build import _run_build_command
from torch._inductor.fb.utils import (
    log_global_cache_errors,
    log_global_cache_stats,
    log_global_cache_vals,
    use_global_cache,
)
```

</td>
<td valign="top">

```python
if config.is_fbcode():
    from triton.fb import build_paths
    from triton.fb.build import _run_build_command

    from torch._inductor.fb.utils import (  # type: ignore[import]
        log_global_cache_errors,
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 1.8× over-gen &nbsp;·&nbsp; max=**0.689**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.804**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; max=**0.804**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.699)</th>
<th align="left">v2-sys (max=0.863)</th>
<th align="left">v2.1-sys (max=0.804)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
=======
    from triton.fb import build_paths
    from triton.fb.build import _run_build_command

>>>>>>> b
    from torch._inductor.fb.utils import (
        log_global_cache_errors,
```

</td>
<td valign="top">

```python
_HERE = os.path.abspath(__file__)
_TORCH_PATH = os.path.dirname(os.path.dirname(_HERE))

if config.is_fbcode():
    from triton.fb import build_paths
    from triton.fb.build import _run_build_command

    from torch._inductor.fb.utils import (
        log_global_cache_errors,
        log_global_cache_stats,
        log_global_cache_vals,
        use_global_cache,
    )
    from triton.fb import build_paths
```

</td>
<td valign="top">

```python
if config.is_fbcode():
    from triton.fb import build_paths
    from triton.fb.build import _run_build_command
    from torch._inductor.fb.utils import (
        log_global_cache_errors,
        log_global_cache_stats,
        log_global_cache_vals,
        use_global_cache,
    )
```

</td>
<td valign="top">

```python
from triton.fb import build_paths
    from triton.fb.build import _run_build_command

    from torch._inductor.fb.utils import (
        log_global_cache_errors,
        log_global_cache_stats,
        log_global_cache_vals,
        use_global_cache,
    )
```

</td>
<td valign="top">

```python
if config.is_fbcode():
    from triton.fb import build_paths
    from triton.fb.build import _run_build_command

    from torch._inductor.fb.utils import (  # type: ignore[import]
        log_global_cache_errors,
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 1.9× over-gen &nbsp;·&nbsp; max=**0.699**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; max=**0.863**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; max=**0.804**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

## Both models fail

### Case `0xab382083003c453c`

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
            import encodings
            import formatter
            import getpass
>>>>>>> b
            import html.entities
```

</td>
<td valign="top">

```python
import distutils.command.install_lib
import distutils.command.register
import distutils.command.sdist
import distutils.command.upload

try:
    import tty  # Not available on Windows
except ImportError:
    if support.verbose:
        pass

import encodings
import formatter
import getpass
import html.entities
```

</td>
<td valign="top">

```python
import distutils.command.install_lib
import distutils.command.register
import distutils.command.sdist
import distutils.command.upload

import encodings
import formatter
import getpass
import html.entities

try:
    import tty  # Not available on Windows
except ImportError:
    if support.verbose:
```

</td>
<td valign="top">

```python
import encodings
import formatter
import getpass
import html.entities
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

**custom** &nbsp;·&nbsp; 310.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 297.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**custom** &nbsp;·&nbsp; 69.0× over-gen &nbsp;·&nbsp; max=**0.000**

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
            import encodings
            import formatter
            import getpass
>>>>>>> b
            import html.entities
```

</td>
<td valign="top">

```python
import distutils.command.install_lib
            import distutils.command.register
            import distutils.command.sdist
            import distutils.command.upload
            import encodings
            import formatter
            import getpass
            import html.entities

            try:
                import tty  # Not available on Windows
            except ImportError:
                if support.verbose:
```

</td>
<td valign="top">

```python
import distutils.command.install_lib
            import distutils.command.register
            import distutils.command.sdist
            import distutils.command.upload

            import encodings
            import formatter
            import getpass
            import html.entities

            try:
                import tty  # Not available on Windows
            except ImportError:
                if support.verbose:
```

</td>
<td valign="top">

```python
import distutils.command.install_lib
            import distutils.command.register
            import distutils.command.sdist
            import distutils.command.upload

            import encodings
            import formatter
            import getpass
            import html.entities

            try:
                import tty  # Not available on Windows
            except ImportError:
                if support.verbose:
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

**pick-b** &nbsp;·&nbsp; 428.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 429.0× over-gen &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 429.0× over-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.000**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---

### Case `0x15e530c25ca1e871`

#### Apertus-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.090)</th>
<th align="left">v2-sys (max=0.090)</th>
<th align="left">v2.1-sys (max=0.087)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
    def set_fs_attributes_if_different(self, file_args, changed):
=======
    def set_file_attributes_if_different(self, file_args, changed):
>>>>>>> b
        # set modes owners and context as needed
```

</td>
<td valign="top">

```python
def set_file_attributes_if_different(self, file_args, changed):
        # set modes owners and context as needed
        changed = self.set_context_if_different(
            file_args['path'], file_args['secontext'], changed
        )
        changed = self.set_owner_if_different(
            file_args['path'], file_args['owner'], changed
        )
        return changed
```

</td>
<td valign="top">

```python
def set_file_attributes_if_different(self, file_args, changed):
    # set modes owners and context as needed
    changed = self.set_context_if_different(
        file_args['path'], file_args['secontext'], changed
    )
    changed = self.set_owner_if_different(
        file_args['path'], file_args['owner'], changed
    )
    return changed
```

</td>
<td valign="top">

```python
def set_file_attributes_if_different(self, file_args, changed):
    # set modes owners and context as needed
    changed = self.set_context_if_different(
        file_args['path'], file_args['secontext'], changed
    )
    changed = self.set_owner_if_different(
        file_args['path'], file_args['owner'], changed
    )
```

</td>
<td valign="top">

```python
    def _symbolic_mode_to_octal(self, path_stat, symbolic_mode):
        new_mode = stat.S_IMODE(path_stat.st_mode)

        mode_re = re.compile(r'^(?P<users>[ugoa]+)(?P<operator>[-+=])(?P<perms>[rwxXst]*|[ugo])$')
        for mode in symbolic_mode.split(','):
            match = mode_re.match(mode)
            if match:
                users = match.group('users')
                operator = match.group('operator')
                perms = match.group('perms')

                if users == 'a': users = 'ugo'

                for user in users:
                    mode_to_apply = self._get_octal_mode_from_symbolic_perms(path_stat, user, perms)
                    new_mode = self._apply_operation_to_mode(user, operator, mode_to_apply, new_mode)
            else:
                raise ValueError("bad symbolic permission for mode: %s" % mode)
        return new_mode
    
    def _apply_operation_to_mode(self, user, operator, mode_to_apply, current_mode):
        if operator  ==  '=':
            if user == 'u': mask = stat.S_IRWXU | stat.S_ISUID
            elif user == 'g': mask = stat.S_IRWXG | stat.S_ISGID
            elif user == 'o': mask = stat.S_IRWXO | stat.S_ISVTX
            
            # mask out u, g, or o permissions from current_mode and apply new permissions   
            inverse_mask = mask ^ 07777
            new_mode = (current_mode & inverse_mask) | mode_to_apply
        elif operator == '+':
            new_mode = current_mode | mode_to_apply
        elif operator == '-':
            new_mode = current_mode - (current_mode & mode_to_apply)
        return new_mode
        
    def _get_octal_mode_from_symbolic_perms(self, path_stat, user, perms):
        prev_mode = stat.S_IMODE(path_stat.st_mode)
        
        is_directory = stat.S_ISDIR(path_stat.st_mode)
        has_x_permissions = (prev_mode & 00111) > 0
        apply_X_permission = is_directory or has_x_permissions

        # Permission bits constants documented at:
        # http://docs.python.org/2/library/stat.html#stat.S_ISUID
        user_perms_to_modes = {
            'u': {
                'r': stat.S_IRUSR,
                'w': stat.S_IWUSR,
                'x': stat.S_IXUSR,
                'X': stat.S_IXUSR if apply_X_permission else 0,
                's': stat.S_ISUID,
                't': 0,
                'u': prev_mode & stat.S_IRWXU,
                'g': (prev_mode & stat.S_IRWXG) << 3,
                'o': (prev_mode & stat.S_IRWXO) << 6 },
            'g': {
                'r': stat.S_IRGRP,
                'w': stat.S_IWGRP,
                'x': stat.S_IXGRP,
                'X': stat.S_IXGRP if apply_X_permission else 0,
                's': stat.S_ISGID,
                't': 0,
                'u': (prev_mode & stat.S_IRWXU) >> 3,
                'g': prev_mode & stat.S_IRWXG,
                'o': (prev_mode & stat.S_IRWXO) << 3 },
            'o': {
                'r': stat.S_IROTH,
                'w': stat.S_IWOTH,
                'x': stat.S_IXOTH,
                'X': stat.S_IXOTH if apply_X_permission else 0,
                's': 0,
                't': stat.S_ISVTX,
                'u': (prev_mode & stat.S_IRWXU) >> 6,
                'g': (prev_mode & stat.S_IRWXG) >> 3,
                'o': prev_mode & stat.S_IRWXO }
        }

        or_reduce = lambda mode, perm: mode | user_perms_to_modes[user][perm]
        return reduce(or_reduce, perms, 0)

    def set_fs_attributes_if_different(self, file_args, changed):
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; max=**0.090**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; max=**0.090**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; max=**0.087**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

#### Qwen3-8B

<table>
<tr>
<th align="left">Conflict</th>
<th align="left">v1-sys (max=0.090)</th>
<th align="left">v2-sys (max=0.086)</th>
<th align="left">v2.1-sys (max=0.086)</th>
<th align="left">Ground truth</th>
</tr>
<tr>
<td valign="top">

```python
<<<<<<< a
    def set_fs_attributes_if_different(self, file_args, changed):
=======
    def set_file_attributes_if_different(self, file_args, changed):
>>>>>>> b
        # set modes owners and context as needed
```

</td>
<td valign="top">

```python
def set_file_attributes_if_different(self, file_args, changed):
        # set modes owners and context as needed
        changed = self.set_context_if_different(
            file_args['path'], file_args['secontext'], changed
        )
        changed = self.set_owner_if_different(
            file_args['path'], file_args['owner'], changed
        )
        return changed
```

</td>
<td valign="top">

```python
def set_file_attributes_if_different(self, file_args, changed):
        # set modes owners and context as needed
        changed = self.set_context_if_different(
            file_args['path'], file_args['secontext'], changed
        )
        changed = self.set_owner_if_different(
            file_args['path'], file_args['owner'], changed
```

</td>
<td valign="top">

```python
def set_file_attributes_if_different(self, file_args, changed):
        # set modes owners and context as needed
        changed = self.set_context_if_different(
            file_args['path'], file_args['secontext'], changed
        )
        changed = self.set_owner_if_different(
            file_args['path'], file_args['owner'], changed
```

</td>
<td valign="top">

```python
    def _symbolic_mode_to_octal(self, path_stat, symbolic_mode):
        new_mode = stat.S_IMODE(path_stat.st_mode)

        mode_re = re.compile(r'^(?P<users>[ugoa]+)(?P<operator>[-+=])(?P<perms>[rwxXst]*|[ugo])$')
        for mode in symbolic_mode.split(','):
            match = mode_re.match(mode)
            if match:
                users = match.group('users')
                operator = match.group('operator')
                perms = match.group('perms')

                if users == 'a': users = 'ugo'

                for user in users:
                    mode_to_apply = self._get_octal_mode_from_symbolic_perms(path_stat, user, perms)
                    new_mode = self._apply_operation_to_mode(user, operator, mode_to_apply, new_mode)
            else:
                raise ValueError("bad symbolic permission for mode: %s" % mode)
        return new_mode
    
    def _apply_operation_to_mode(self, user, operator, mode_to_apply, current_mode):
        if operator  ==  '=':
            if user == 'u': mask = stat.S_IRWXU | stat.S_ISUID
            elif user == 'g': mask = stat.S_IRWXG | stat.S_ISGID
            elif user == 'o': mask = stat.S_IRWXO | stat.S_ISVTX
            
            # mask out u, g, or o permissions from current_mode and apply new permissions   
            inverse_mask = mask ^ 07777
            new_mode = (current_mode & inverse_mask) | mode_to_apply
        elif operator == '+':
            new_mode = current_mode | mode_to_apply
        elif operator == '-':
            new_mode = current_mode - (current_mode & mode_to_apply)
        return new_mode
        
    def _get_octal_mode_from_symbolic_perms(self, path_stat, user, perms):
        prev_mode = stat.S_IMODE(path_stat.st_mode)
        
        is_directory = stat.S_ISDIR(path_stat.st_mode)
        has_x_permissions = (prev_mode & 00111) > 0
        apply_X_permission = is_directory or has_x_permissions

        # Permission bits constants documented at:
        # http://docs.python.org/2/library/stat.html#stat.S_ISUID
        user_perms_to_modes = {
            'u': {
                'r': stat.S_IRUSR,
                'w': stat.S_IWUSR,
                'x': stat.S_IXUSR,
                'X': stat.S_IXUSR if apply_X_permission else 0,
                's': stat.S_ISUID,
                't': 0,
                'u': prev_mode & stat.S_IRWXU,
                'g': (prev_mode & stat.S_IRWXG) << 3,
                'o': (prev_mode & stat.S_IRWXO) << 6 },
            'g': {
                'r': stat.S_IRGRP,
                'w': stat.S_IWGRP,
                'x': stat.S_IXGRP,
                'X': stat.S_IXGRP if apply_X_permission else 0,
                's': stat.S_ISGID,
                't': 0,
                'u': (prev_mode & stat.S_IRWXU) >> 3,
                'g': prev_mode & stat.S_IRWXG,
                'o': (prev_mode & stat.S_IRWXO) << 3 },
            'o': {
                'r': stat.S_IROTH,
                'w': stat.S_IWOTH,
                'x': stat.S_IXOTH,
                'X': stat.S_IXOTH if apply_X_permission else 0,
                's': 0,
                't': stat.S_ISVTX,
                'u': (prev_mode & stat.S_IRWXU) >> 6,
                'g': (prev_mode & stat.S_IRWXG) >> 3,
                'o': prev_mode & stat.S_IRWXO }
        }

        or_reduce = lambda mode, perm: mode | user_perms_to_modes[user][perm]
        return reduce(or_reduce, perms, 0)

    def set_fs_attributes_if_different(self, file_args, changed):
```

</td>
</tr>
<tr>
<td valign="top">&mdash;</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; max=**0.090**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; max=**0.086**

</td>
<td valign="top">

**pick-b** &nbsp;·&nbsp; 0.1× under-gen &nbsp;·&nbsp; = prev version &nbsp;·&nbsp; max=**0.086**

</td>
<td valign="top">&mdash;</td>
</tr>
</table>

---
