import uvicorn
from html import escape
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from lic_manager import LicenseEncoder, LicenseDecoder, check_serial

app = FastAPI()


class KeyRequest(BaseModel):
    username: str = "Test"
    organization: str = "Test Studio"
    serial_number: str = "Abcd-1234"
    quantity: int = 1

    def __str__(self):
        out_str = f"Company: {self.organization}\n"
        out_str += f"Username: {self.username}\n"
        out_str += f"Serial: {self.serial_number}\n"
        out_str += f"Max users: {self.quantity}"
        return out_str


@app.get("/js/bcom.js", response_class=HTMLResponse)
async def get_bcom_js():
    js_content = """
    function validateForm() {
        const quantityInput = document.getElementById('quantity');
        const quantity = quantityInput.value;
        const errorElement = document.getElementById('quantityError');

        if (quantity === "") {
            quantityInput.value = 1;
            return true;
        }

        if (quantity <= 0 || !Number.isInteger(Number(quantity))) {
            errorElement.textContent = '请输入有效的正整数';
            return false;
        } else {
            errorElement.textContent = '';
            return true;
        }
    }

    function getFormData() {
        return {
            username: document.getElementById('username').value || "Test",
            organization: document.getElementById('organization').value || "Test Studio",
            serial_number: document.getElementById('serial_number').value || "Abcd-1234",
            quantity: parseInt(document.getElementById('quantity').value) || 1
        };
    }

    function copyToClipboard() {
        text = document.getElementById('keyValue').innerHTML.replaceAll('<br>', '\\r\\n');
        navigator.clipboard.writeText(text).then(() => {
            alert('密钥已复制到剪贴板');
        }).catch(err => {
            console.error('复制失败: ', err);
        });
    }
    
    function displayError(error) {
        if (error != null) { console.error('Error:', error); }
        document.getElementById('result').innerHTML = '<p style="color:red;">生成密钥时出错，请重试。</p>';
    }
    
    function updateKeyDetail(data) {
        const resultDiv = document.getElementById('result');
        resultDiv.style.display = 'block';
        if (data == null) { displayError(); return; }
        if (data.code != 0) { document.getElementById('result').innerHTML = `<p style="color:red;">${data.msg}</p>`; return; }
        resultDiv.innerHTML = `
            <h3>生成结果</h3>
            <div class="key-result">
                <span id="keyValue">${data.key}</span>                
            </div>
            <button class="copy-btn" onclick="copyToClipboard()">复制</button>
            <p><strong>状态:</strong> ${data.msg}</p>
            <h4>提交的数据:</h4>
            <ul class="data-list">
                <li><strong>版本:</strong> ${data.key_data.version}</li>
                <li><strong>用户名:</strong> ${data.key_data.username}</li>
                <li><strong>组织名:</strong> ${data.key_data.organization}</li>
                <li><strong>序列号:</strong> ${data.key_data.serial_number}</li>
                <li><strong>数量:</strong> ${data.key_data.quantity}</li>
                <li><strong>随机值:</strong> ${data.key_data.random}</li>
            </ul>
        `;
        return;
    }

    function generateKey() {
        if (!validateForm()) {
            return;
        }

        const formData = getFormData();

        fetch('/BComKeyGen', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => updateKeyDetail(data))
        .catch((error) => displayError(error));
    }
    """
    return HTMLResponse(content=js_content, media_type="application/javascript")


@app.get("/css/bcom.css", response_class=HTMLResponse)
async def get_bcom_css():
    css_content = """
    body {
        font-family: Arial, sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    h1 {
        color: #333;
        text-align: center;
    }
    .container {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 5px;
    }
    .form-group {
        margin-bottom: 15px;
    }
    label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }
    input {
        width: 100%;
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
        box-sizing: border-box;
    }
    button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
        width: 100%;
    }
    button:hover {
        background-color: #45a049;
    }
    #result {
        margin-top: 20px;
        padding: 15px;
        background-color: #e8f5e9;
        border-radius: 4px;
        display: none;
    }
    .error {
        color: red;
        font-size: 14px;
        margin-top: 5px;
    }
    .default-value {
        color: #666;
        font-style: italic;
        font-size: 12px;
        margin-top: 2px;
    }
    .key-result {
        margin: 10px 0;
        padding: 10px;
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 4px;
        word-wrap: break-word;
        word-break: break-all;
        overflow-wrap: break-word;
    }
    .data-list {
        list-style-type: none;
        padding: 0;
    }
    .data-list li {
        padding: 5px 0;
        border-bottom: 1px solid #eee;
    }
    .data-list li:last-child {
        border-bottom: none;
    }
    .copy-btn {
        background-color: #2196F3;
        color: white;
        padding: 5px 10px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 12px;
        margin-left: 10px;
    }
    .copy-btn:hover {
        background-color: #0b7dda;
    }
    """
    return HTMLResponse(content=css_content, media_type="text/css")


@app.get("/BComKeyGenerator", response_class=HTMLResponse)
async def get_bcom_key_generator_page():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Key Generator</title>
        <link rel="stylesheet" href="/css/bcom.css">
    </head>
    <body>
        <h1>密钥生成器</h1>
        <div class="container">
            <form id="keyForm">
                <div class="form-group">
                    <label for="username">用户名:</label>
                    <input type="text" id="username" name="username" value="Test">
                    <div class="default-value">默认值: Test</div>
                </div>

                <div class="form-group">
                    <label for="organization">组织名:</label>
                    <input type="text" id="organization" name="organization" value="Test Studio">
                    <div class="default-value">默认值: Test Studio</div>
                </div>

                <div class="form-group">
                    <label for="serial_number">序列号:</label>
                    <input type="text" id="serial_number" name="serial_number" value="Abcd-1234">
                    <div class="default-value">默认值: Abcd-1234</div>
                </div>

                <div class="form-group">
                    <label for="quantity">数量 (正整数):</label>
                    <input type="number" id="quantity" name="quantity" min="1" step="1" value="1">
                    <div class="default-value">默认值: 1</div>
                    <div id="quantityError" class="error"></div>
                </div>

                <button type="button" onclick="generateKey()">生成密钥</button>
            </form>

            <div id="result"></div>
        </div>

        <script src="/js/bcom.js"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/BComKeyGen")
async def gen_bcom_key(req: KeyRequest):
    serial_num = req.serial_number
    if not check_serial(serial_num):
        return {
            "code": -1,
            "msg": "序列号格式错误",
            "key": "",
            "key_data": None
        }

    key = LicenseEncoder(username=req.username, atsite=req.organization, user_num=req.quantity,
                         serial_num=req.serial_number).encode()
    dec = LicenseDecoder(key)
    num, atsite = dec.dec_org()
    version = dec.dec_version()
    rand, serial_num = dec.dec_random()
    username = dec.dec_uname()
    rsp_key = escape(key).replace("\r\n", "<br>")

    return {
        "code": 0,
        "msg": "Success",
        "key": rsp_key,
        "key_data": {
            "version": version,
            "username": username,
            "organization": atsite,
            "serial_number": serial_num,
            "quantity": num,
            "random": rand
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
