# 372A1-35

Usage: in two separate terminal processes, in order, first `cd` to `src\server` and run `python server.py`. In the second terminal process, `cd` to `src\client` and run `python client.py`. 

No external dependencies are required, python STL dependencies are `socket, os, time, pathlib`. Technically pathlib is not on the instructions list, but it does not provide at all in any way external networking frameworks or is an existing chat/file-transfer library. I decided to include it for parity across our teammate's machines since I use a mac and some do not. 

Test logs can be viewed in `src\client\logs` and `src\server\logs` respectively. 