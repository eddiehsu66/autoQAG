from src.LogModule.AutoPrompt.promptApi import infer_llm


#分批次采样，模糊
def wrongReason(logContent, rightResult, wrongResult):
    prompt_temp = f"""
    You will be provided with a log,and its correct result by person and wrong result by model. 
    output the reason why the wrongResult occurs,without any superfluous output
    :param log: {logContent}
    :param rightResult: {rightResult}
    :param wrongResult: {wrongResult}
    """

    # 思路：
    return infer_llm(prompt_temp, None, None)
if __name__ == '__main__':

    dataSet = [
        [
            'visible is system.charge.show', 'visible is <*>', 'Format the input data.', 'system.charge.showFormat'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Provide output for the given inputs.', 'system.charge.show'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Write outputs for the given inputs.', 'system.charge.showWrite("Charging device at 50%")\n\nOutput:\nCharging device at 50%'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Replace the placeholders in the given inputs with <*> and write the corresponding outputs.', 'Input: system.charge.showReplace\nOutput: system.charge.showReplace'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Replace the placeholders in the given inputs with the actual values and provide the corresponding outputs.', 'Input:\nlog_message = "System charge is at {0}%."\n\ncharge_percentage = 75\n\nOutput:\nSystem charge is at 75%.'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Please write an output for each of the following inputs.', 'Input: system.charge.show\nOutput: system.charge.show'],
        [
            'visible is system.charge.show', 'visible is <*>', 'setSystemUiVisibility vis=<*> mask=<*> oldVal=<*> newVal=<*> diff=<*> fullscreenStackVis=<*> dockedStackVis=<*>, fullscreenStackBounds=Rect(<*>, <*> - <*>, <*>), dockedStackBounds=Rect(<*>, <*> - <*>, <*>)', 'System UI visibility changed: vis=<*>, mask=<*>, oldVal=<*>, newVal=<*>, diff=<*>, fullscreenStackVis=<*>, dockedStackVis=<*>, fullscreenStackBounds=Rect(<*>, <*> - <*>, <*>), dockedStackBounds=Rect(<*>, <*> - <*>, <*>)'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Please provide output for the following inputs.', 'system.charge.show'],
        [
            'visible is system.charge.show', 'visible is <*>', 'updateLightsLocked,mInCall =false,mScreenOn = true,ledNotification == null?true\nshouldBlockLocation  ret:false\ncancelNotificationWithTag pid 28601,uid = 10111,tag = null,pkg =com.tencent.mobileqq,id =193\nlogNotificationVisibilityChanges runInThread start\nnotifyUiVisibilityChanged:vis=0x40000000, SystemUiVisibility=0x40000000', 'cancelNotificationWithTag pid 28601, uid = 10111, pkg = com.tencent.mobileqq, id = 193'],
        [
            'visible is system.charge.show', 'visible is <*>', 'setSystemUiVisibility vis=0 mask=1 oldVal=40000500 newVal=40000500 diff=0 fullscreenStackVis=0 dockedStackVis=0', 'System UI visibility set to 0.'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Format the inputs in the following way: \nInput: [input]', 'Input: system.charge.show\nOutput: visible'],
        [
            'visible is system.charge.show', 'visible is <*>', 'setSystemUiVisibility vis=0 mask=1 oldVal=40000500 newVal=40000500 diff=0 fullscreenStackVis=0 dockedStackVis=0', 'System UI visibility set to 0.'],
        [
            'visible is system.charge.show', 'visible is <*>', 'updateDimmedActivatedHideSensitive overlap:false\ninterceptKeyBeforeQueueing: key <*>, result : <*>\nAnimating brightness: target=<*>, rate=<*>\nsetSystemUiVisibility vis=<*> mask=<*> oldVal=<*> newVal=<*> diff=<*> fullscreenStackVis=<*> dockedStackVis=<*>\nshouldBlockLocation  ret:false', 'interceptKeyBeforeQueueing: key <*>, result : <*>\nAnimating brightness: target=<*>, rate=<*>\nsetSystemUiVisibility vis=<*> mask=<*> oldVal=<*> newVal=<*> diff=<*> fullscreenStackVis=<*> dockedStackVis=<*>\nshouldBlockLocation  ret:false'],
        [
            'visible is system.charge.show', 'visible is <*>', 'setSystemUiVisibility vis=0 mask=1 oldVal=40000500 newVal=40000500 diff=0 fullscreenStackVis=0 dockedStackVis=0', 'System UI visibility set to 0'],
        [
            'visible is system.charge.show', 'visible is <*>', 'updateLightsLocked,mInCall =false,mScreenOn = true,ledNotification == null?true\nshouldBlockLocation  ret:false\ncancelNotificationWithTag pid <*>,uid = <*>,tag = null,pkg =<*>,id =<*>\nlogNotificationVisibilityChanges runInThread start\nnotifyUiVisibilityChanged:vis=<*>, SystemUiVisibility=<*>', 'logNotificationVisibilityChanges runInThread start\nnotifyUiVisibilityChanged:vis=<*>, SystemUiVisibility=<*>'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Mask sensitive information and only provide necessary details.', 'system.charge.showMask'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Please provide outputs for the following inputs: \n1. HBM brightnessIn =38\n2. userActivityNoUpdateLocked: eventTime=261980925, event=2, flags=0x0, uid=1000\n3. setLightsOn(true)\n4. Received TIME_TICK alarm; rescheduling\n5. acquire lock=120758482, flags=0x1, tag="RILJ_ACK_WL", name=com.android.phone, ws=null, uid=1001, pid=2626', '1. system.charge.show HBM brightnessIn=38\n2. system.charge.show userActivityNoUpdateLocked: eventTime=261980925, event=2, flags=0x0, uid=1000\n3. system.charge.show setLightsOn(true)\n4. system.charge.show Received TIME_TICK alarm; rescheduling\n5. system.charge.show acquire lock=120758482, flags=0x1, tag="RILJ_ACK_WL", name=com.android.phone, ws=null, uid=1001, pid=2626'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Write the output for each input without making any changes.', 'system.charge.show'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Animating brightness: target=<*>, rate=<*>\nonExpandingFinished\nSkipping, withExcluded: false, tr.intent:Intent { flg=<*>, cmp=<*> (has extras) }\ngetRunningAppProcesses: caller <*> does not hold REAL_GET_TASKS; limiting output\noverlapAmount:<*>.<*>, previousNotificationEnd:<*>.<*>, newYTranslation:<*>.<*>, location:<*>, i:<*>, getTopPadding:<*>.<*>, getLocationOnScreen():<*>', 'brightness: target=<*>, rate=<*>\nonExpandingFinished\noverlapAmount:<*>.<*>, previousNotificationEnd:<*>.<*>, newYTranslation:<*>.<*>, location:<*>, i:<*>, getTopPadding:<*>.<*>, getLocationOnScreen():<*>'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Please output the inputs as they are without any changes.', 'system.charge.show'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Please provide outputs for the following inputs.', 'system.charge.show'],
        [
            'visible is system.charge.show', 'visible is <*>', 'updateDimmedActivatedHideSensitive overlap:false\ninterceptKeyBeforeQueueing: key <*>, result : <*>\nAnimating brightness: target=<*>, rate=<*>\nsetSystemUiVisibility vis=<*> mask=<*> oldVal=<*> newVal=<*> diff=<*> fullscreenStackVis=<*> dockedStackVis=<*>\nshouldBlockLocation  ret:false', 'system.charge.showupdateDimmedActivatedHideSensitive\ninterceptKeyBeforeQueueing: key <*>, result : <*>\nAnimating brightness: target=<*>, rate=<*>\nsetSystemUiVisibility vis=<*> mask=<*> oldVal=<*> newVal=<*> diff=<*> fullscreenStackVis=<*> dockedStackVis=<*>\nshouldBlockLocation  ret:false'],
        [
            'visible is system.charge.show', 'visible is <*>', 'HBM brightnessIn =<*>\nuserActivityNoUpdateLocked: eventTime=<*>, event=<*>, flags=<*>, uid=<*>\nsetLightsOn(true)\nReceived TIME_TICK alarm; rescheduling\nacquire lock=<*>, flags=<*>, tag="<*>", name=<*>, ws=<*>, uid=<*>, pid=<*>', 'system.charge.showHBM brightnessIn =<*>\nuserActivityNoUpdateLocked: eventTime=<*>, event=<*>, flags=<*>, uid=<*>\nsetLightsOn(true)\nReceived TIME_TICK alarm; rescheduling\nacquire lock=<*>, flags=<*>, tag="<*>", name=<*>, ws=<*>, uid=<*>, pid=<*>'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Output: Replace the placeholders with the corresponding values for each input.', 'system.charge.showOutput: Replace the placeholders with the corresponding values for each input.'],
        [
            'visible is system.charge.show', 'visible is <*>', 'notifyUiVisibilityChanged:vis=0x40000500, SystemUiVisibility=0x40000500', 'SystemUiVisibility=0x40000500'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Replace specific values in the inputs with placeholders.', 'system.charge.show'],
        [
            'visible is system.charge.show', 'visible is <*>', 'Replace all specific values in the input with placeholders.', 'You will be provided with a log message.visible is system.charge.show'],
    ]
    for data in dataSet:
        # prompt = (
        #     "ready=true,policy=3,wakefulness=1,wksummary=0x1,uasummary=0x1,bootcompleted=true,boostinprogress=false,"
        #     "waitmodeenable=false,mode=false,manual=38,auto=-1,adj=0.0userId=0")
        # rightResult = "ready=true,policy=<*>,wakefulness=<*>,wksummary=<*>,uasummary=<*>,bootcompleted=true,boostinprogress=false,waitmodeenable=false,mode=false,manual=<*>,auto=<*>,adj=<*>.0userId=<*>"
        # wrongResult = "ready=true,policy=3,wakefulness=1,wksummary=0x1,uasummary=0x1,bootcompleted=true,boostinprogress=false,waitmodeenable=false,mode=false,manual=38,auto=-1,adj=0.0userId=0"
        print(wrongReason(data[0], data[1], data[3]))
#['ready=true,policy=3,wakefulness=1,wksummary=0x1,uasummary=0x1,bootcompleted=true,boostinprogress=false,waitmodeenable=false,mode=false,manual=38,auto=-1,adj=0.0userId=0'
# , 'ready=true,policy=<*>,wakefulness=<*>,wksummary=<*>,uasummary=<*>,bootcompleted=true,boostinprogress=false,waitmodeenable=false,mode=false,manual=<*>,auto=<*>,adj=<*>.0userId=<*>',
# 'Replace the placeholders in the given inputs with <*> and provide the corresponding outputs.',
# 'ready=true,policy=3,wakefulness=1,wksummary=0x1,uasummary=0x1,bootcompleted=true,boostinprogress=false,waitmodeenable=false,mode=false,manual=38,auto=-1,adj=0.0userId=0']