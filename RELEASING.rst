blosc2-openhtj2k release procedure
==================================

Preliminaries
-------------

* Check that `version` is correct in `pyproject.toml` file, and in sync with
  `blosc2_openhtj2k/__init__.py`.

* Make sure that the `src/OpenHTJ2K` submodule is updated to the latest version
  (or a specific version that should be documented in the `RELEASE_NOTES.md`)::

    cd src/OpenHTJ2K
    git pull
    git checkout <desired tag>
    cd ../..
    git commit -m "Update OpenHTJ2K sources" src/OpenHTJ2K
    git push

* Check that the current main branch is passing the tests in continuous integration.

* Build the package and make sure that examples work correctly::

    cd examples
    python compress.py kodim23.png /tmp/kodim23.b2nd
    python decompress.py /tmp/kodim23.b2nd /tmp/kodim23.png

* Make sure that `RELEASE_NOTES.md` and `ANNOUNCE.rst` are up to date with the latest news
  in the release.

* Commit the changes::

    git commit -a -m "Getting ready for release X.Y.Z"
    git push

* Double check that the supported Python versions for the wheels are the correct ones
  (`.github/workflows/cibuildwheels.yml`).  Add/remove Python version if needed.
  Also, update the `classifiers` field for the supported Python versions.

* Check that the metainfo for the package is correct::

    python -m build --sdist 
    twine check dist/*


Tagging
-------

* Create a (signed, if possible) tag ``X.Y.Z`` from ``main``.  Use the next message::

    git tag -a vX.Y.Z -m "Tagging version X.Y.Z"

* Push the tag to the github repo::

    git push --tags


Checking packaging
------------------

* Do an actual release in github by visiting:
  https://github.com/Blosc/blosc2_openhtj2k/releases/new
  Add the notes specific for this release.
  This will upload the wheels to PyPI too.

* Check that the package (and wheels!) have been uploaded to PyPI
  (they should have been created when GHA would finish the tag trigger):
  https://pypi.org/project/blosc2-openhtj2k

* Check that the packages and wheels are sane::

    python -m pip install blosc2-openhtj2k -U
    cd examples
    python compress.py kodim23.png /tmp/kodim23.b2nd
    python decompress.py /tmp/kodim23.b2nd /tmp/kodim23.png


Announcing
----------

* Send an announcement to the Blosc list.  Use the ``ANNOUNCE.rst`` file as skeleton
  (or possibly as the definitive version). Start the subject with ANN:.

* Announce in https://fosstodon.org/@Blosc2 account and rejoice.


Post-release actions
--------------------

* Change back to the actual  repo::

    cd $HOME/blosc/blosc2-openhtj2k

* Create new headers for adding new features in ``RELEASE_NOTES.md``
  add this place-holder:

  XXX version-specific blurb XXX

* Edit `version` in `pyproject.toml` file, and sync it with
  `blosc2_openhtj2k/__init__.py` in main branch. Increment it to the next
  minor one (i.e. X.Y.Z --> X.Y.(Z+1).dev0).

* Commit your changes with::

    git commit -a -m "Post X.Y.Z release actions done"
    git push


That's all folks!
