import pywinauto

def browserupload(address,filename):
    app = pywinauto.Desktop()
    dlg = app["打开"]
    buttons = [control for control in dlg.descendants() if control.class_name() == "Edit"]
    dlg["Toolbar3"].click()
    buttons[-1].type_keys(address+'{VK_RETURN}')
    buttons[0].type_keys(filename.replace(' ','{VK_SPACE}').replace('+','{VK_ADD}').replace('-','{VK_SUBTRACT}').replace('*','{VK_MULTIPLY}').replace('/','{VK_DIVIDE}').replace('%','{%}'))
    dlg["打开(&O)"].click()

wenkuupload('C:\\','test.txt')
