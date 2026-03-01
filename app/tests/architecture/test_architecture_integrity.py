import os


def test_domain_has_no_selenium_imports():
    for root, _, files in os.walk("app/domain"):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file)) as f:
                    content = f.read()
                    assert "selenium" not in content
                    assert "playwright" not in content