---
layout: post
title:  "基于Matlab的DTW+MFCC语音识别"
date:   2021-05-12 14:22:00 +8000
categories: 
---

**山东大学 语音信号处理**期末课程作业“基于Matlab的DTW+MFCC语音识别”。本实验基于DTW+MFCC算法进行识别，在个人测试中可以对个人的训练词有很好的识别效果，5个训练词可以达到接近100%识别率。但是对不同口音不同性别的人识别率很低。



最后更新：2021年5月12日 15点01分



### 实验分析

一个人的语音信号一般是由浊音、清音和爆破音构成。其中浊音是气流通过一开一闭口产生的**周期性振动的声音**，而清音则是气流通过声带狭长部位产生的类似**白噪声的声音**，而爆破音就是爆发而出，气体快速通过的声音。而浊音和清音包含了大部分的元音和辅音字母，因此一般使用浊音激励和清音激励构建语音信号模型。

不考虑模型的实际架构，我们对于一个录制的语音信号

<img src="https://raw.githubusercontent.com/Yumik-xy/blogImage/main/img/20210512143932.png" alt="image-20210512143931597" style="zoom:67%;" />

其存在不包含任何信息的[0]段空腔和人呼吸或环境产生的噪声。在语音识别时必须挑选出真正在说话的部分，而排除掉部分空腔和噪声的干扰，以提高算法的识别效率，该做法成为**端点检测**。

### 端点检测实现

#### 计算帧能量

这里固定每256帧取为一个短时帧长，计算短时帧内的总能量。通过上图可以看出，包含语音的部分其能量较大，而一般噪声只在0范围震荡。

```matlab
function energy = calEnergy(data)
frame = 256;
ret_len = floor(length(data)/frame);
energy = zeros(ret_len,1);
for i = 1:ret_len
    energy(i) = sum(data((i-1)*frame+1:i*frame).^2);
end
end
```

#### 计算帧过零数

高斯噪声会产生高频率震动，体现在每一帧产生一个过零点现象，而人声的频率一般在300~3400Hz，小于噪声的频率，其过零点间隔也会响应的增大，因此计算过零率也可以分辨人声和噪声。

这里同样是256取一个短时帧，计算短时间的过零点数

```matlab
function zeroCrossingRate = calZeroCrossingRate(data)
frame = 256;
ret_len = floor(length(data)/frame);
zeroCrossingRate = zeros(ret_len,1);
for i = 1:ret_len
    zeroCrossingRate(i) = sum((data((i-1)*frame+1:i*frame-1).*data((i-1)*frame+2:i*frame))<0);
end
end
```

#### 结合短时能量和过零率计算人声部分

这里一步一步进行分析：

`Ml` `MH`表示的是能量的门限值，如果能量高于MH，则说明这一部分一定是语音信号，而能量高于ML而低于MH的部分可以认为是人声的开始和结束部分，类似于一个词说完拖音或刚开口吐气的部分，而低于ML的就可以认为是环境噪声。

因此我们需要找到合适的阈值，由于这是算法类实验，所有的参数都是基于 Fs = 16000Hz 情况下手工调试得到，未使用CNN进行自动修正，因此其取值会严重影响判决。

因此判决算法首先通过高门限MH寻找到语音信号峰的左右标度，再通过低门限ML进行左右拓展，最后使用过零点门限判据是否不包含其他低频部分。如此即可排除掉绝大部分的噪声干扰，得到一个较为纯粹的语音波形。该波形通过MATLAB函数`sound()`播放后可以很轻易被人耳识别！

```matlab
function endPointDetect = calEndPointDetect(energy,zeroCrossingRate)
energyAvg = sum(energy)/length(energy);
energy5sum = sum(energy(1:5));

emptyLen = 8;

ML = energy5sum / 5;
MH = energyAvg / 4;
ML = (ML+MH) / 4;
if ML > MH
    ML = MH / 4;
end

zeroC5sum = sum(zeroCrossingRate(1:5));
Zs = zeroC5sum / 5;

checkA = [];
checkB = [];
checkC = [];

flag = 0;
for i = 1:length(energy)
    if isempty(checkA) && ~flag && energy(i) > MH
        checkA = [checkA;i];
        flag = 1;
    elseif ~flag && energy(i) > MH && i - emptyLen > checkA(end)
        checkA = [checkA;i];
        flag = 1;
    elseif ~flag && energy(i) > MH && i - emptyLen <= checkA(end)
        checkA = checkA(1:end-1);
        flag = 1;
    end
    if flag && energy(i) < MH
        if i - checkA(end) <= 2
            checkA = checkA(1:end-1);
        else
            checkA = [checkA;i];
        end
        flag = 0;
    end
end
if mod(length(checkA),2) == 1
    checkA = [checkA;length(checkA)];
end

for j = 1:length(checkA)
    i = checkA(j);
    if mod(j,2) == 0
        while i < length(energy) && energy(i) > ML
            i = i + 1;
        end
        checkB = [checkB;i];
    else
        while i > 1 && energy(i) > ML
            i = i - 1;
        end
        checkB = [checkB;i];
    end
end

for j = 1:length(checkB)
    i = checkB(j);
    if mod(j,2) == 0
        while i < length(zeroCrossingRate) && zeroCrossingRate(i) >= 3 * Zs
            i = i + 1;
        end
        checkC = [checkC;i];
    else
        while i > 1 && zeroCrossingRate(i) >= 3 * Zs
            i = i - 1;
        end
        checkC = [checkC;i];
    end
end

endPointDetect = checkC;

end
```

### MFCC特征

……

### DTW识别

……