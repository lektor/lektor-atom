# Release

* Update [CHANGELOG.md](https://github.com/lektor/lektor-atom/blob/master/CHANGELOG.md)

* Commit changes
  ```bash
  git add .
  git commit -m "Prepare release version"
  ```

* Tag the release
  ```bash
  git tag -s vX.X.X -m "Version X.X.X"
  ```

* Push changes
  ```bash
  git push origin master
  git push origin --tags
  ```

* The new tag will trigger a Github action workflow on CI which will publish to PyPI using the `getlektor` account.

## Retrigger events

If the release process needs to be fixed or retriggered you will need to delete the tag and recreate it, or create a new tag from scratch.

* To delete and recreate a tag:
  ```bash
  git push --delete origin refs/tags/<tag-name>
  git tag -s <recreated-tag-name> -m "Version X.X.X"
  git push origin --tags
  ```
