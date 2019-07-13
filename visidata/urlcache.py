import os
import os.path
import time
import urllib.request
import urllib.parse

from visidata import __version_info__, Path, options, asyncthread, modtime


def urlcache(url, days=1, text=True):
    'Return Path object to local cache of url contents.'
    p = Path(os.path.join(options.visidata_dir, 'cache', urllib.parse.quote(url, safe='')))
    if p.exists():
        secs = time.time() - modtime(p)
        if secs < days*24*60*60:
            return p

    if not p.parent.exists():
        os.makedirs(p.parent, exist_ok=True)

    assert p.parent.is_dir(), p.parent

    return p


@asyncthread
def _do_request(p, url, text=True):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as fp:
        ret = fp.read()
        if text:
            ret = ret.decode('utf-8').strip()
            with p.open_text(mode='w') as fpout:
                fpout.write(ret)
        else:
            with p.open_bytes(mode='w') as fpout:
                fpout.write(ret)
