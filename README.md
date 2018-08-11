# check-package tester

Helper files to test changes in check-package script.

### Prerequisites

* a clone from [buildroot](https://github.com/buildroot/buildroot.git)
* [Buildroot prerequisites](http://nightly.buildroot.org/#requirement-mandatory)
* Python 2 (2.6 or any later)
* Python 3 (3.6 or any later)
* flake8 for both Python 2 and Python 3
* pytest

### Installing

```
make -C /path/to/buidroot BR2_EXTERNAL=/path/to/this-repo O=/path/to/output defconfig
cd /path/to/output
```

Before adding any changes to the check-package script in the buildroot tree,
save the output of the script for all files in the current buildroot tree:
```
make update-reference-log
```

If your setup is OK this command must not end on error:
```
make check-check-package
```

## Running the tests

Do your changes to check-package script in the buildroot tree.

Depending on what changes you made, the expected result for the tests can be
different.

If you added changes that should not change the script behaviour in the main use
case, this target must build without any error.
```
make check-check-package
```

If you added a new check for the script the target above will fail, but it
generates the file *log.diff* in the output directory to be manually inspected.

## License

Copyright (C) 2018  Ricardo Martincoski

This project is licensed under GNU GPL version 2 or any later - see the
[LICENSE](LICENSE) file for details.

## Acknowledgments

* Billie Thompson for this [README.md Template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)

