Summary
Added a simple Python script scripts/hello_testing.py that prints "Hello Testing"
Updated scripts/BUILD.bazel to include the new py_binary target for hello_testing
Files Changed
scripts/hello_testing.py (new file)
scripts/BUILD.bazel (updated)
Test Plan
 Created the hello_testing.py script
 Updated BUILD.bazel with py_binary target
 Verified script executes correctly and prints "Hello Testing"
