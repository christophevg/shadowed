import shadowed

def test_update_with_user_changes_with_merge(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path    = "test.txt"
  content = "Hello World\nThis is a test.\n"

  fs = shadowed.FileSystem(real, shad)
  fs.create(path, content)

  with open(real.join(path), "w") as fp:
    fp.write("Title\nHello World\nThis is a NICE test.\n")

  new_content = "Hello Merged World\nThis is another test.\n"

  fs.update(path, new_content, merge=True)
  
  assert fs.real_content(path) == "Title\nHello Merged World\nThis is another NICE test.\n"

def test_merge_with_user_changes(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path    = "test.txt"
  content = "Hello World\nThis is a test.\n"

  fs = shadowed.FileSystem(real, shad)
  fs.create(path, content)

  with open(real.join(path), "w") as fp:
    fp.write("Title\nHello World\nThis is a NICE test.\n")

  new_content = "Hello Merged World\nThis is another test.\n"

  fs.merge(path, new_content)
  
  assert fs.real_content(path) == "Title\nHello Merged World\nThis is another NICE test.\n"

def test_merge_with_conflicting_user_changes(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path    = "test.txt"
  content = "Hello World\nThis is a test.\n"

  fs = shadowed.FileSystem(real, shad)
  fs.create(path, content)

  with open(real.join(path), "w") as fp:
    fp.write("Hello World\nThis is ANOTHER test.\n")

  new_content = "Hello World\nThis is another test.\n"

  fs.merge(path, new_content)
  
  assert fs.real_content(path) == "Hello World\nThis is ANOTHER test.\n"

def test_merge_no_changes_with_user_changes(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path    = "test.txt"
  content = "Hello World\nThis is a test.\n"

  fs = shadowed.FileSystem(real, shad)
  fs.create(path, content)

  with open(real.join(path), "w") as fp:
    fp.write("Title\nHello World\nThis is a NICE test.\n")

  new_content = content

  fs.merge(path, new_content)
  
  assert fs.real_content(path) == "Title\nHello World\nThis is a NICE test.\n"
