# Running

```
podman run -it --log-level debug \
    -v /home/phajas/services/tiddlywiki_listener/base.html:/base.html:z \
    -v /home/phajas/wiki:/wiki:z \
    -v /home/phajas/out:/out:z \
    --rm tiddlywiki_listener:latest
```
