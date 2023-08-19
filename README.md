# Ibanez TS-9 Plot

## Development Setup

### Development Setup Using pyenv

Use the following commands to create a Python virtualenv using [pyenv][] and
[pyenv-virtualenv][], install the requirements in the virtualenv named, and list
the available [Invoke][] tasks.

```bash
$ pyenv virtualenv 3.11 ibanez
$ pyenv activate ibanez
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ inv -l
```

## License

[ibanez_ts9][] is released under the MIT license. Please see the
[LICENSE.txt][] file for more information.

[ibanez_ts9]: https://github.com/matthewrankin/ibanez_ts9
[invoke]: https://www.pyinvoke.org/
[LICENSE.txt]: https://github.com/matthewrankin/ibanez_ts9/blob/master/LICENSE.txt
[pyenv]: https://github.com/pyenv/pyenv
[pyenv-virtualenv]: https://github.com/pyenv/pyenv-virtualenv
