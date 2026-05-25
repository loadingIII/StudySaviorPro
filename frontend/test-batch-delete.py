"""
测试批量删除功能的 Playwright 脚本
"""
from playwright.sync_api import sync_playwright
import time

def test_batch_delete():
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 导航到应用
        page.goto('http://localhost:5173')
        page.wait_for_load_state('networkidle')
        
        # 等待页面加载
        time.sleep(2)
        
        # 1. 检查是否能看到批量删除按钮
        print("步骤 1: 查找批量删除按钮...")
        batch_delete_btn = page.locator('button[title="批量删除"]')
        if batch_delete_btn.count() > 0:
            print("✓ 找到批量删除按钮")
            batch_delete_btn.click()
            print("✓ 已点击批量删除按钮，进入批量模式")
            time.sleep(1)
        else:
            print("✗ 未找到批量删除按钮")
        
        # 2. 检查复选框是否显示
        print("\n步骤 2: 查找消息复选框...")
        checkboxes = page.locator('.message-checkbox')
        count = checkboxes.count()
        print(f"找到 {count} 个复选框")
        
        if count > 0:
            print("✓ 复选框已显示")
            # 点击第一个复选框
            checkboxes.first.click()
            print("✓ 已点击第一个复选框")
            time.sleep(1)
            
            # 检查是否被选中
            checked = page.locator('.message-checkbox.checked')
            if checked.count() > 0:
                print("✓ 复选框已成功选中")
            else:
                print("✗ 复选框未被选中")
        else:
            print("✗ 复选框未显示，可能的问题:")
            print("  - isBatchDeleteMode 状态未正确设置")
            print("  - message.id 不存在")
            print("  - CSS 样式问题导致复选框不可见")
        
        # 3. 截图查看当前状态
        page.screenshot(path='batch-delete-test.png', full_page=True)
        print("\n✓ 已保存截图：batch-delete-test.png")
        
        # 4. 检查控制台日志
        print("\n步骤 3: 检查控制台日志...")
        logs = []
        page.on('console', msg: logs.append(f"{msg.type}: {msg.text}"))
        
        # 5. 尝试点击取消按钮
        cancel_btn = page.locator('button[title="取消"]')
        if cancel_btn.count() > 0:
            print("✓ 找到取消按钮")
            cancel_btn.click()
            print("✓ 已点击取消按钮")
        else:
            print("✗ 未找到取消按钮")
        
        # 再次截图
        time.sleep(1)
        page.screenshot(path='after-cancel.png', full_page=True)
        print("✓ 已保存截图：after-cancel.png")
        
        browser.close()
        print("\n测试完成!")

if __name__ == '__main__':
    try:
        test_batch_delete()
    except Exception as e:
        print(f"测试失败：{e}")
        import traceback
        traceback.print_exc()
