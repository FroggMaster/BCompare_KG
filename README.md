# Beyond Compare 5 Keygen
用于生成 Beyond Compare 5.x （截至 5.1 ver 31016）版本注册密钥
## 前置工作
使用 010Editor 等二进制工具，修改 Beyond Compare 可执行文件中内置的 RSA 密钥

修改前：
```
++11Ik:7EFlNLs6Yqc3p-LtUOXBElimekQm8e3BTSeGhxhlpmVDeVVrrUAkLTXpZ7mK6jAPAOhyHiokPtYfmokklPELfOxt1s5HJmAnl-5r8YEvsQXY8-dm6EFwYJlXgWOCutNn2+FsvA7EXvM-2xZ1MW8LiGeYuXCA6Yt2wTuU4YWM+ZUBkIGEs1QRNRYIeGB9GB9YsS8U2-Z3uunZPgnA5pF+E8BRwYz9ZE--VFeKCPamspG7tdvjA3AJNRNrCVmJvwq5SqgEQwINdcmwwjmc4JetVK76og5A5sPOIXSwOjlYK+Sm8rvlJZoxh0XFfyioHz48JV3vXbBKjgAlPAc7Np1+wk
```
修改后（修改字符串末尾的 `p1+wk` 为 `pn+wk` ）：
```
++11Ik:7EFlNLs6Yqc3p-LtUOXBElimekQm8e3BTSeGhxhlpmVDeVVrrUAkLTXpZ7mK6jAPAOhyHiokPtYfmokklPELfOxt1s5HJmAnl-5r8YEvsQXY8-dm6EFwYJlXgWOCutNn2+FsvA7EXvM-2xZ1MW8LiGeYuXCA6Yt2wTuU4YWM+ZUBkIGEs1QRNRYIeGB9GB9YsS8U2-Z3uunZPgnA5pF+E8BRwYz9ZE--VFeKCPamspG7tdvjA3AJNRNrCVmJvwq5SqgEQwINdcmwwjmc4JetVK76og5A5sPOIXSwOjlYK+Sm8rvlJZoxh0XFfyioHz48JV3vXbBKjgAlPAc7Npn+wk
```
<img src="asserts/01.png" alt="image-20240902170702727" style="zoom:50%;" /> 

## 生成注册密钥

```shell
git clone https://github.com/garfield-ts/BCompare_Keygen.git
cd BCompare_Keygen
pip3 install -r requirements.txt
python3 keygen.py
```
得到可用的注册密钥：
```
--- BEGIN LICENSE KEY ---
7uo7UY8gVANuMyCkDtSZRnNBkDXr1o4msYwtu7GFPaZ9B6naWXfsqEBgD5hM8jm3Sw2L4oFHY53VchaHv4j3q4QNiNxPgcv3qz89nKu3VSgQDVpPrAUWKgkjko5Gvck7BBBJmnKbGZJtDTi21WnJ5AMm7upD6QXgbf2BUS7toxB7jzhFLyotDj59KMGkgXMBXeUoa6T7Yt76MZN6UcHqYG5fMLuBp1JfGxpMXE7AMeUXXLwvAxsJGMkC5oS93WoVLopUoBW4SYNpS7YzzirkqZdRt58TbQpqcvwFeD32X2ZamVAv9SjeQUQhyEwktExFwTc541HrJeDV2xqfr4EgbUprSWEu8p
--- END LICENSE KEY -----
```
默认生成的注册密钥使用以下信息：
```
Version: 0x3d
Serial: Abcd-Efgh
Username: Test
Company: Home
Max users: 1
```
可以通过传入相关参数，自定义注册密钥的信息

<img src="asserts/06.png" alt="image-20240903162908919" style="zoom:50%;" /> 

## 使用密钥进行注册
打开 Beyond Compare 5，此时会弹出 `评估模式错误` 的提示，点击 `输入密钥` 按钮进入注册页面：

<img src="asserts/03.png" alt="image-20240902172200651" style="zoom:50%;" /> 

将脚本生成的注册密钥粘贴到输入框中，点击 `确定` 即可激活。

<img src="asserts/04.png" alt="image-20240902172404873" style="zoom:40%;" /> 

<img src="asserts/05.png" alt="image-20240902172829613" style="zoom:50%;" /> 

## 注意事项

1. 在 `macOS` 版中，RSA 密钥位于 `/Applications/Beyond Compare.app/Contents/MacOS/BCompare` 文件中；在 `Windows` 版中，RSA 密钥位于 `BCompare.exe` 文件中

2. `macOS` 版修改密钥后，需要关闭操作系统的 `SIP（System Integrity Protection，系统完整性保护）` 功能，否则会报错「**“Beyond Compare”意外退出**」且无法运行，详见 [少数派的这篇文章](https://sspai.com/post/55066) 。

3. 在 `macOS` 版中，`BCompare` 文件里可以搜到 2 个 RSA 密钥，实际要修改的是第二处密钥。`Windows` 版只有 1 处密钥，直接修改即可。

   <img src="asserts/07.png" alt="image-20250707104436903" style="zoom:100%;" /> 

## TODO

- 集成二进制文件 patch 功能
- ……
