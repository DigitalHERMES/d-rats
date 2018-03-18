import sys

from d_rats.version import DRATS_VERSION
import os

def win32_build():
    from distutils.core import setup
    import py2exe

    try:
        # if this doesn't work, try import modulefinder
        import py2exe.mf as modulefinder
        import win32com
        for p in win32com.__path__[1:]:
            modulefinder.AddPackagePath("win32com", p)
        for extra in ["win32com.shell"]: #,"win32com.mapi"
            __import__(extra)
            m = sys.modules[extra]
            for p in m.__path__[1:]:
                modulefinder.AddPackagePath(extra, p)
    except ImportError:
        # no build path setup, no worries.
        pass


    opts = {
        "py2exe" : {
            "includes" : "pango,atk,gobject,cairo,pangocairo,win32gui,win32com,win32com.shell,email.iterators,email.generator",
            "compressed" : 1,
            "optimize" : 2,
            "bundle_files" : 3,
            #        "packages" : ""
            }
        }

    setup(
        windows=[{'script' : "d-rats",
                  'icon_resources': [(0x0004, 'd-rats2.ico')]},
                 {'script' : 'd-rats_repeater'},
                 {'script' : 'd-rats_mapdownloader'}],
        data_files=["C:\\GTK\\bin\\jpeg62.dll"],
        options=opts)

def macos_build():
    from setuptools import setup
    import shutil

    APP = ['d-rats-%s.py' % DRATS_VERSION]
    shutil.copy("d-rats", APP[0])
    DATA_FILES = [('../Frameworks',
                   ['/opt/local/lib/libpangox-1.0.0.2203.1.dylib']),
                  ('../Resources/pango/1.6.0/modules', ['/opt/local/lib/pango/1.6.0/modules/pango-basic-atsui.so']),
                  ('../Resources',
                   ['images', 'ui']),
                  ]
    OPTIONS = {'argv_emulation': True, "includes" : "gtk,atk,pangocairo,cairo"}

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
        )

def default_build():
    from distutils.core import setup
    from glob import glob

    desktop_files = glob("share/*.desktop")
    form_files = glob("forms/*.x?l")
    image_files = glob("images/*")
    image_files.append("d-rats2.ico")
    image_files.append("share/d-rats2.xpm")
    ui_files = glob("ui/*")
    _locale_files = glob("locale/*/LC_MESSAGES/D-RATS.mo")
    _man_files = glob("share/*.1")

    man_files = []
    for f in _man_files:
        os.system("gzip -c %s > %s" % (f, f+".gz"))
	man_files.append(f+".gz")

    locale_files = []
    for f in _locale_files:
        locale_files.append(("/usr/share/d-rats/%s" % os.path.dirname(f), [f]))

    print "LOC: %s" % str(ui_files)

    setup(
        name="d-rats",
        description="D-RATS",
        long_description="A communications tool for D-STAR",
        author="Dan Smith, KK7DS",
        author_email="kk7ds@danplanet.com",
        packages=["d_rats", "d_rats.geopy", "d_rats.ui", "d_rats.sessions"],
        version=DRATS_VERSION,
        scripts=["d-rats", "d-rats_mapdownloader", "d-rats_repeater"],
        data_files=[('/usr/share/applications', desktop_files),
                    ('/usr/share/icons', ["share/d-rats2.xpm"]),
                    ('/usr/share/d-rats/forms', form_files),
                    ('/usr/share/d-rats/images', image_files),
                    ('/usr/share/d-rats/ui', ui_files),
                    ('/usr/share/d-rats/libexec', ["libexec/lzhuf"]),
                    ('/usr/share/man/man1', man_files),
                    ('/usr/share/doc/d-rats', ['COPYING']),
                    ] + locale_files)
                    
if sys.platform == "darwin":
    macos_build()
elif sys.platform == "win32":
    win32_build()
else:
    default_build()


