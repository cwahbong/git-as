git-as
======
Apply or clear a bunch of settings in one command.

configuration
-------------

You need to specify keys applied by git-as first.  The following example adds
`user.name` and `user.email`.

```
> git config --global --add as.key user.name
> git config --global --add as.key user.email
```

Then add presets "example\_preset"

```
> git config --global as.preset.example_preset.user.name example_name
> git config --global as.preset.example_preset.user.email example_email
```

Finally, at your git repository, use the following command to apply your preset.

```
> git as preset example_preset
```

usage
-----

Apply git settings by predefined preset [name]
```
> git as preset [name]
```

Clear git settings by predefined keys.
```
> git as clear
```
