---
layout: post
title: 基于Matlab的KNN+PCA语音二分类
date: 2021-05-12 23:06:47 +0800
categories: MATLAB
tag: MATLAB语音识别
---

* content
{:toc}

KNN+PCA实现电力系统正常/故障二分类处理

<!-- ![]({{ '/styles/article-image/20210512230647_1.jpg' | prepend: site.baseurl }}){:height='80%' width='80%'} -->

### PCA简要介绍

PCA也称“主元分析”，主要用于数据降维，类似**最优有损压缩**方法

🌰例子：

对一个二维数据，找到一条直线使所有数据距离线的距离之和最短，该线称为**最佳投影线**，此时该点到原点连成的线段在线上投影的距离“最长”（即到原点的距离一定，到直线距离最短，因此在直线上的投影最长），即可以保留最多的有效信息。

