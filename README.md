# J2K wheel

By following the next steps you can edit J2K sources and work with the plugin in C-Blosc2.

## Configuring J2K params

In blosc2_htj2k.cpp you can change the default parameters as you want.
Moreover, in encoder you can use the j2k_params as C-Blosc2 cparams.codec_params to choose J2K parameters.

## Create the wheel

Once you have J2K parameters set, you have to create a wheel with the compressor inside:

```shell
python setup.py bdist_wheel
```

## Verify the wheel is working

```shell
pip install dist/blosc2_openhtj2k-*.whl
```

And then simulate that you are going to uninstall.  You will be presented where the plugin has been installed:

```shell
pip uninstall blosc2_openhtj2k
```

For example, the shared library should appear somewhere like:

```shell
ls -l /Users/faltet/miniconda3/lib/python3.9/site-packages/blosc2_openhtj2k
total 112
-rw-r--r--  1 faltet  staff   258B Mar  6 13:45 __init__.py
drwxr-xr-x  3 faltet  staff    96B Mar  6 13:45 __pycache__/
-rwxr-xr-x  1 faltet  staff    48K Mar  6 13:45 libblosc2_plugin_example.so*
```

In the future, you should be able to test that the wheel is working with this command:

```shell
blosc2_test_plugin plugin_example_name
```
## Work in C-Blosc2

Now that you have the wheel installed, work with it in C-Blosc2.

That's all folks!
