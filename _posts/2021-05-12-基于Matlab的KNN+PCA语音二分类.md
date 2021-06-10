---
layout: post
title: 基于Matlab的KNN+PCA语音二分类
date: 2021-05-12 23:06:47 +0800
categories: 语音识别
tag: MATLAB
---

* content
{:toc}
**山东大学 语音信号处理**期末课程作业“KNN+PCA实现电力系统正常/故障二分类处理”。本实验通过MFCC对环境声音信息进行特征抽样提取，对MFCC数据信息进行PCA降维处理，并使用KNN进行二分类进行正常/故障声音信息判决操作，其识别率近乎可以达到100%

### 实验目的

机器运行正常与否，一般人可以通过分辨机器运行的声音来判决。

**但是**，我们不可能一直守在机器旁保证机器正常工作，因此基于语音识别的一种语音二分类判决被提出，通过其他设备对音频进行读取分析，判断机器工作状况

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210606100854.png!small" alt="image-20210606100854217" style="zoom:67%;" />

### PCA简要介绍

PCA也称“主元分析”，主要用于数据降维，类似**最优有损压缩**方法

🌰例子：

对一个二维数据，找到一条直线使所有数据距离线的距离之和最短，该线称为**最佳投影线**，此时该点到原点连成的线段在线上投影的距离“最长”（即到原点的距离一定，到直线距离最短，因此在直线上的投影最长），即可以保留最多的有效信息。

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210515234051.png" alt="image-20210512233141030"  />

同样拓展到高$N$维空间数据也可以通过PCA进行$N-1$维降维进行数据压缩，这样可以大幅度减少计算复杂度，提高计算效率

### KNN简要介绍

KNN称“K邻近算法”，主要用于判据数据属于哪一分类

🌰例子：

 对于一组数据，现将其分成A、B两组。现在有一未知节点，为寻找其组别，算法会寻早其距离最近的K个节点，若K节点中A组节点数>B组节点数，则节点归为A组，反之同理。

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210515234059.png" alt="image-20210512233808658"  />

### 识别过程

#### 读入训练集数据和训练集标签

读取训练目录所有的声音数据和标签，由于提供的标签为[1,2]​分布的值，故这里将其转化为​[-1,1]分布便于进行二分类判决

```matlab
train_wav_path_list = dir(strcat(train_path,'*.wav')); % 读取所有 wav 文件
train_wav_length = length(train_wav_path_list); % 处理训练集数据
train_selection_wav = zeros(train_wav_length,171); % 训练集保存
train_lable = [1 1 ... 2 2 2 ... 1];
train_lable = (train_lable - 1.5)*2;
```

#### 训练集数据进行预处理

对所有的数据进行特征值选择，并保存在选择后的矩阵中

```matlab
for i = 1:train_wav_length
    wav = audioread([train_path, num2str(i), '.wav'])'; % 读入数据
    wav = wav(1:max_audio);
    selection_wav = feature_selection(wav); % 特征选择函数
    selection_wav = selection_wav'; % 转置
    train_selection_wav(i,:) = selection_wav(:);
end
```

注意到函数`feature_selection(wav)`即为特征值选择函数。

函数首先对所有数据进行归一化操作，将数据进行0点对齐使得所有数据和为0，这样是为了更好的做PCA运算，归一化公式为

$x^*=\frac{x-\mu}{\sigma}$

函数如下：

```matlab
function new_data = normalization(data) % 数据归一化函数
    data_mean = mean(data); % 求均值μ
    data_norm = norm(data);
    new_data = (data - data_mean) / data_norm;
end
```

进行归一化后将8000bit语音信号进行分帧，分帧数通过公式

$fn=\frac{N-wlen}{inc}+1=\frac{8000-800}{400}+1=19$

进行计算。取分帧长度为800帧，帧移为400，计算可得需要分成19帧，帧与帧之间通过Hamming码进行连接，分帧函数如下：

```matlab
function f=enframe(data,win,inc)
    nx=length(data); % 数据长度
    nwin=length(win); % 窗函数，这里使用Hamming窗
    if (nwin == 1)
       len = win;
    else
       len = nwin;
    end
    if (nargin < 3)
       inc = len;
    end
    nf = fix((nx-len+inc)/inc); % 分帧数，公式即上面给出的
    f=zeros(nf,len);
    indf= inc*(0:(nf-1)).';
    inds = (1:len);
    f(:) = data(indf(:,ones(1,len))+inds(ones(nf,1),:)); % 分帧
    if (nwin > 1)
        w = win(:)';
        f = f .* w(ones(nf,1),:); % 加窗
    end
end
```

分帧后的即对每一帧进行特征值选择。对分帧后数据进行傅里叶变换，计算得到子带能量和总的频带能量作为该帧的特征值，由此可以得到9×19​的特征值矩阵，特征值选择函数如下：

```matlab
function selection_data = feature_selection(data) % 特征选择函数
    enframe_data = enframe(data,hamming(800),400); % 声音分成19帧信号
    E = [];
    for i = 1:size(enframe_data,1)
        wav_std = normalization(enframe_data(i,:)); % 数据归一化
        wav_std_fft = abs(fft(wav_std,2048)); % 做2048的fft变换
        % 计算频带能量
        E0 = sum(wav_std_fft(1:1024).^2); % 总能量
        E1 = sum(wav_std_fft(1:120).^2); % 子带能量
        E2 = sum(wav_std_fft(121:250).^2); % 子带能量
        E3 = sum(wav_std_fft(251:360).^2); % 子带能量
        E4 = sum(wav_std_fft(361:480).^2); % 子带能量
        E5 = sum(wav_std_fft(481:600).^2); % 子带能量
        E6 = sum(wav_std_fft(601:730).^2); % 子带能量
        E7 = sum(wav_std_fft(731:850).^2); % 子带能量
        E8 = sum(wav_std_fft(851:1024).^2); % 子带能量    
        E = [E; E0 E1 E2 E3 E4 E5 E6 E7 E8];
    end
    selection_data = E;
end
```

#### 读入测试集数据和测试集标签

测试集的处理方式与训练集完全一致，这里不再过多赘述。

若训练集或测试集较大，可以将预先提取得到的特征值变量写入为*.mat*文件进行保存，方便后期调用。

#### 计算特征值的特征向量

得到训练集的特征向量数组后，经过PCA算法进行降维，将171维数据进行降维，降维后维度根据给出的数据精度$\mu$进行动态计算，计算步骤如下：

1. 对协方差矩阵$\Sigma_X$写出行列式：$\|\Sigma_x-\lambda E\|$
2. 令$\|\Sigma_x-\lambda E\|=0$，得到的$\lambda_1,\lambda_2,\cdots,\lambda_n$就是协方差矩阵$\Sigma_x$的特征值（即奇异值分解）
3. 将$\lambda=\lambda_i$带入，$\|\Sigma_x-\lambda E\|=0$，解出的基础解系就是$v_1,v_2,\cdots,v_n$协方差矩阵$\Sigma_x$就是该特征值对应的特征向量。
4. 根据定义，主元1应该匹配奇异值最大的解系，主元n对应分第n大的解系，因此对特征向量从大到小进行排序
5. 根据数据精度$\mu=\frac{\sum_{i=0}^{k}(v_i)}{\sum_{i=0}^{n}(v_i)}$，计算得到的特征方向向量的维度k，即PCA降维的维度为k维

```matlab
function [principal_eigenvector, i] = principal_eigenvector(data,mu)
    [row, ~] = size(data);
    mean_data = mean(data);
    ajust_data = data - repmat(mean_data,row,1);
    ajust_data = ajust_data'; % 计算零点归一化数据
    cov_data = ajust_data*ajust_data'/(size(ajust_data,1)-1); % 求数据的自相关矩阵
        
    [v, d] = eig(cov_data);
    v_sort = zeros(size(v));
    [m, n] = sort(diag(d),'descend');
    
    for i = 1:row % 按从大到小的顺序构建d，重新排序v
        v_sort(:,i) = v(:,n(i));
    end
    
    for i = 1:row
        if sum(m(1:i))/sum(m) > mu
            break;
        end
    end
    principal_eigenvector = v_sort(:,1:i);
end
```

#### 进行KNN邻近算法，求解测试集分类

由KNN邻近算法的定义可知，现在需要找n个距离目标节点最近的点，根据其包含的正常/异常类的数量推导出目标节点的类型。

上一步我们先求出了归一化直线的**特征向量**，我们现在可以求解出训练集和测试集每一点到该向量方向的投影坐标，通过坐标值计算出即可计算测试集的某个点到所有训练集点的距离，找出距离最小的n个点，和这n个点的数据即可判决该点属于哪一类。

本次实验去knn的n值为3，当求解diff大于1时，判决为异常类；小于1时判决为正常类，这是由于我们预先对数据标签进行了[-1,1]的处理，即正常用-1表示，异常用1表示，只要求解出几个点的标签和，即可知道其距离内包含的哪种类型的点更多。

```matlab
knn = 3;

[train_vector, k] = principal_eigenvector(train_selection_wav,mu(mu_i)); % 计算得到特征向量

train_selection_mean = mean(train_selection_wav); % 归0化训练集
train_len = (train_selection_wav - repmat(train_selection_mean,train_wav_length,1)) * train_vector; % 求训练集矢量

test_selection_mean = mean(train_selection_wav); % 归0化测试集
test_len = (test_selection_wav - repmat(test_selection_mean,test_wav_length,1)) * train_vector; % 求测试集矢量
    
diff = zeros(test_wav_length,1); % 计算第k个目标节点的差异值
for i = 1:test_wav_length
    test_wav = test_len(i); % 取出测试集距离
    dvalue_len = abs(train_len-repmat(test_len(i),train_wav_length,1)); % 计算距离最小的值
    [svalue_len,n] = sort(dvalue_len);
    for j = 1:knn
        diff(i) = diff(i) + train_lable(n(j));
    end
    if diff(i)*test_lable(i)<0
        ['第' num2str(i) '出现错误']
    end
end
err = sum(diff.*test_lable'<0);
errP = err/test_wav_length;
out = ['当mu=' num2str(mu(mu_i)) '，k=' num2str(k) '时，错误率为：' num2str(errP*100) '%']

```

### 实验结果分析

判决结果如下：

```matlab
out = '当mu=0.5，k=1时，错误率为：0%'
out = '当mu=0.55，k=1时，错误率为：0%'
out = '当mu=0.6，k=1时，错误率为：0%'
out = '当mu=0.65，k=1时，错误率为：0%'
out = '当mu=0.7，k=1时，错误率为：0%'
out = '当mu=0.75，k=2时，错误率为：0%'
out = '当mu=0.8，k=2时，错误率为：0%'
out = '当mu=0.85，k=2时，错误率为：0%'
out = '当mu=0.9，k=2时，错误率为：0%'
out = '当mu=0.95，k=7时，错误率为：0%'
out = '当mu=1，k=128时，错误率为：0%'
```

μ和k的关系如下图，不难看出当k取1时，μ值已经达到0.7~0.75之间，这是由于特征值向量中有一向量占比很大，其体现了数据的**主要判决准则**

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210606100743.png!small" alt="img" style="zoom:67%;" />

下图给出了训练集和测试集在不同μ的取值下，所展现的投影长度分布如下，红色部分为需要警告的部分，可以看出其被较好的分离出来，该实验取得了较好的成功！

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210515234116.png!small" alt="image-20210513082543621" style="zoom:67%;" />

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210515234559.png!small" alt="image-20210513082549545" style="zoom:67%;" />

### 参考文献

1. [语音识别的技术原理是什么？](https://www.zhihu.com/question/20398418/answer/18080841)
2. [如何通俗易懂地讲解什么是 PCA 主成分分析](https://www.zhihu.com/question/41120789/answer/481966094)
3. [深入浅出KNN算法（一） 介绍篇](https://zhuanlan.zhihu.com/p/61341071)