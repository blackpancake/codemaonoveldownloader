try:
    import pyi_splash  # 编写时请忽视包不存在，pyinstaller打包时会自动把包写入到程序，不会报错

    pyi_splash.update_text('正在进入……')

    pyi_splash.close()  # 如果丢失这行代码，闪屏动画（加载界面）将会与主程序一同结束！而不是主界面加载完成时结束！

except:
    pass
