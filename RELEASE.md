# Release

* Update [CHANGELOG.md](https://github.com/lektor/lektor-atom/blob/master/CHANGELOG.md)

* Update package version on [setup.py](https://github.com/lektor/lektor-atom/blob/master/setup.py)

* Commit changes
  ```bash
  git add .
  git commit -m "Prepare release version"
  ```

* Tag the release
  ```bash
  git tag -a vX.X.X -m "Version X.X.X"
  ```

* Push changes
  ```bash
  git push origin master
  git push origin --tags
  ```

* The new tag will trigger a Github action workflow on CI and will create [pre release](https://github.com/lektor/lektor-atom/releases).

* Once that release is moved from prerelease to release another Github Action will publish to PyPI using the `getlektor` account.

## Retrigger events

If the release process needs to be fixed or retriggered you will need to delete the tag and recreate it, or create a new tag from scratch.

* To delete and recreate a tag:
  ```bash
  git push --delete origin refs/tags/<tag-name>
  git tag -a <recreated-tag-name> -m "Version X.X.X"
  git push origin --tags
  ```
