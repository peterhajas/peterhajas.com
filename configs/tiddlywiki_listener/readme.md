# Running

```
podman run -it --log-level debug \
    -v /home/phajas/services/tiddlywiki_listener/base.html:/base.html:ro,z \
    -v /home/phajas/phajas-wiki:/wiki:ro,z \
    -v /home/phajas/html/wiki:/out:z \
    --rm tiddlywiki_listener:latest
```
