from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # 使用系统安装的 Chrome
    )
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://chat.openai.com")

    input("请在打开的 Chrome 中完成登录与验证，然后按下回车键继续...")

    # 保存已登录状态
    context.storage_state(path="chatgpt_state.json")
    print("✅ 登录状态已保存为 chatgpt_state.json")

    browser.close()
