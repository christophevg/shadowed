import os

import shadowed

def test_file_shadow_creation(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path    = "test.txt"
  content = "Hello World\nThis is a test.\n"

  fs = shadowed.FileSystem(real, shad)
  fs.create(path, content)
  
  assert os.path.isfile(real.join(path))
  assert os.path.isfile(shad.join(path))
  
  with open(real.join("test.txt")) as r:
    assert r.read() == content

  with open(shad.join("test.txt")) as s:
    assert s.read() == content

def test_existing_file_exception(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path    = "test.txt"
  content = "Hello World\nThis is a test.\n"

  with open(real.join(path), "w") as fp:
    fp.write(content)

  fs = shadowed.FileSystem(real, shad)
  try:
    fs.create(path, content)
    assert False, "Expected ValueError due to already existing real file"
  except ValueError as e:
    assert str(e) == f"Real file '{path}' exists. Use 'adopt()' to add shadow."

def test_only_file_path_are_valid_exception(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path    = ""
  content = "Hello World\nThis is a test.\n"

  fs = shadowed.FileSystem(real, shad)
  try:
    fs.create(path, content)
    assert False, "Expected ValueError due to path not being a file"
  except ValueError as e:
    assert str(e) == f"Real path '{path}' isn't a file path."

def test_content_helper_functions(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path    = "test.txt"
  content = "Hello World\nThis is a test.\n"

  fs = shadowed.FileSystem(real, shad)
  fs.create(path, content)
  
  assert fs.real_content(path) == content
  assert fs.shadow_content(path) == content

def test_adopting_existing_file(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path    = "test.txt"
  content = "Hello World\nThis is a test.\n"

  with open(real.join(path), "w") as fp:
    fp.write(content)

  fs = shadowed.FileSystem(real, shad)
  fs.adopt(path)

  assert os.path.isfile(shad.join(path))

  with open(shad.join("test.txt")) as s:
    assert s.read() == content

def test_missing_adoption_file_exception(tmpdir):
  real = tmpdir.mkdir("real")
  shad = tmpdir.mkdir("shad")

  path = "test.txt"

  fs = shadowed.FileSystem(real, shad)
  try:
    fs.adopt(path)
    assert False, "Expected ValueError due to missing existing real file"
  except ValueError as e:
    assert str(e) == f"Real file '{path} doesn't exist. Use 'create()' to create it."
