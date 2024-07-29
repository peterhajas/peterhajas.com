# Running

```
podman run -it --log-level debug \
    -v /home/phajas/services/tiddlywiki_listener/base.html:/base.html:Z \
    -v /home/phajas/wiki:/wiki:Z
    -v /home/phajas/out:/out:Z
    --rm tiddlywiki_listener:latest
```
