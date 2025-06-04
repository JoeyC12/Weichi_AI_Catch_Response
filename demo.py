import json
from playwright.sync_api import sync_playwright
import time

# 修复 cookie 结构，使其兼容 Playwright
def fix_cookie(c):
    same_site = str(c.get("sameSite", "Lax")).lower()
    if same_site in ["no_restriction", "unspecified", "", None]:
        same_site = "Lax"
    elif same_site not in ["lax", "strict", "none"]:
        same_site = "Lax"

    cookie = {
        "name": c["name"],
        "value": c["value"],
        "domain": c["domain"],
        "path": c.get("path", "/"),
        "httpOnly": c.get("httpOnly", False),
        "secure": c.get("secure", False),
        "sameSite": same_site.capitalize()
    }

    if "expirationDate" in c:
        cookie["expires"] = int(c["expirationDate"])

    return cookie

# 加载并修复 cookies
with open("cookies.json", "r") as f:
    raw_cookies = json.load(f)
    cookies = [fix_cookie(c) for c in raw_cookies]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    context.add_cookies(cookies)

    page = context.new_page()
    page.goto("https://chat.openai.com")

    input("✅ 请确认页面已登录 ChatGPT，模型界面已加载。完成后按 Enter 继续...")

    # 提问内容
    prompt = "请告诉我今天法国总统选举的最新情况"

    # 等待 textarea 存在且可用
    input_box = page.locator('div[contenteditable="true"][id="prompt-textarea"]')
    input_box.wait_for(state="visible", timeout=999999999999)
    input_box.type(prompt)
    input_box.press("Enter")

    print("⏳ 正在等待 GPT 回答...")

    # 等待 markdown 回答块出现
    page.wait_for_selector("div.markdown", timeout=999999999999)
    time.sleep(5)  # 给模型完成回答的时间

    # 抓取回答内容
    answers = page.query_selector_all("div.markdown")
    full_answer = "\n\n".join([a.inner_text() for a in answers])

    # 输出与保存
    print("\n📌 GPT 回答如下：\n")
    print(full_answer)

    with open("answer.txt", "w", encoding="utf-8") as f:
        f.write(full_answer)

    print("\n✅ 回答已保存为 answer.txt")

   
