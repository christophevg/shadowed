import shadowed

def test_changes_tests(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path    = "test.txt"
  content = "Hello World\nThis is a test.\n"

  fs = shadowed.FileSystem(real, shad)
  fs.create(path, content)

  assert fs.is_unchanged(path)
  assert not fs.was_changed(path)

  with open(real.join(path), "w") as fp:
    fp.write("Someone changed this.")

  assert not fs.is_unchanged(path)
  assert fs.was_changed(path)

def test_update_without_user_changes(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path    = "test.txt"
  content = "Hello World\nThis is a test.\n"

  fs = shadowed.FileSystem(real, shad)
  fs.create(path, content)

  new_content = "Hello World\nThis is another test.\n"
  
  fs.update(path, new_content)

  with open(real.join("test.txt")) as r:
    assert r.read() == new_content

  with open(shad.join("test.txt")) as s:
    assert s.read() == new_content

def test_update_with_user_changes_but_no_merge(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path    = "test.txt"
  content = "Hello World\nThis is a test.\n"

  fs = shadowed.FileSystem(real, shad)
  fs.create(path, content)

  with open(real.join(path), "w") as fp:
    fp.write("Someone changed this.")

  new_content = "Hello World\nThis is another test.\n"

  try:
    fs.update(path, new_content)
    assert False, "Expected ValueError due to user changes and no merge requested."
  except ValueError as e:
    assert str(e) == f"Real file '{path}' was changed and merging is not requested."

