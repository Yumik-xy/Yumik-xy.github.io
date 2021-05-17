---
layout: post
title: "GitHub Pages 绑定阿里云域名"
date: 2021-05-14 13:45:20 +0800
categories: GitHub
tag: 
- GitHub
- 阿里云
- 自定义域名
top: true
---

* content
{:toc}
从头开始申请阿里的域名，绑定免费的SSL，并关联新域名至GitHub Pages

------

<!-- ![](https://latex.codecogs.com/gif.latex?) -->

### 配置GitHub Pages

网上有很多搭建GitHub Pages的教程目录，这里就不再赘述，一下给出的是两个主要框架

[Jekyll](http://jekyllcn.com/) 最简易的静态博客网站，可以直接将整个项目文件提交至GitHub，GitHub会自动编译，其在文章较多时可以有效减少每次提交的请求大小，加快提交速度

[Hexo](https://hexo.io/zh-cn/) 拥有更多的主题模板和优化方案，著名的 [NexT](http://theme-next.iissnan.com/) 就是基础此进行开发，其中包括了大量配置好的第三方插件和主题信息，对于追求博客质量的用户友好。但是其每次提交都是本地进行项目打包，大量文章会导致打包和推送速度缓慢

### 申请阿里云域名

当使用任意一个框架配置好GitHub Pages，并且可以通过`<GitHub username>.github.io`进行访问后，就可以开始配置一个属于自己的域名了

> 所谓的*自定义域名*并不会送你一个域名，还是得自己去申请的

访问 [阿里域名注册](https://wanwang.aliyun.com/) 网站，选购自己喜欢的域名，查询域名相关信息

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210515235412.png" alt="image-20210515134726815" style="zoom: 67%;" />

这里建议选择`.top`域名，加入清单并购买

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210516000352.png" alt="image-20210515134836035" style="zoom: 67%;" />

购买中要注意选择域名的持有者为`个人`并配置属于自己的`信息模板`，依据配置信息完整配置好自己的相关信息，在购买域名后阿里会帮助我们进行域名申请，这个过程据说会持续3-5天，但实际上只需要5-10min即可审核完成

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210516000359.png" alt="image-20210515135045431" style="zoom:67%;" />

申请完成后即可在个人`搜索`中直接搜索`域名`找到自己的域名信息，这里给出的是我之前申请的博客地址，域名状态显示为正常后即可

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210516000403.png" alt="image-20210515135458294" style="zoom:67%;" />

点击`解析`即可看到当前域名已经可以被正确解析

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210516000406.png" alt="image-20210515135637818" style="zoom:67%;" />

### 申请免费SSL

域名申请完后即可通过`http`进行访问，但是这会在部分网站提示信息不安全，我们可以申请一个免费的SSL证书

同样`搜索`关于`SSL`信息，进入到如下界面中

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210516000410.png" alt="image-20210515135911781" style="zoom:67%;" />

点击立即购买，即可购买20份`DIgicert 免费单域名证书`

>**原DIgicert 免费单域名证书**，建议用于测试、个人试用等场景，org、jp等特殊域名存在无法申请的情况，正式环境建议使用付费证书。
>
>每个实名主体个人/企业，一个自然年内可以领取一次数量为20的云盾单域名试用证书，如需更多云盾单域名试用证书需要额外付费购买。
>
>云盾单域名试用证书在自然年结束时，会自动清除未签发的数量（每个自然年12月31日24:00）
>
>**云盾单域名试用证书不支持续费补齐时间**

购买完成后点击`创建证书`并点击`证书申请`，在申请页面中填写自己刚刚申请到的域名信息，其中`域名验证方式`选择手工DNS验证即可

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210516000415.png" alt="image-20210515140224377" style="zoom:67%;" />

点击下一步，在验证信息中获取到了如下信息

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210516001939.png" alt="image-20210515140419808" style="zoom:67%;" />



回到之前的`域名解析页面`选择添加记录，并按上图配置自己的信息

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210516001935.png" alt="image-20210515140610856" style="zoom: 67%;" />

配置完成后点击验证，等待SSL证书验证通过后，你的网站即拥有了免费的SSL证书，可以通过HTTPS进行访问

### 绑定域名

同样在域名管理页面添加两条**CNAME**信息，其记录值是你在GitHub Pages配置的博客的访问地址		

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210516001206.png" alt="image-20210515140731041" style="zoom:67%;" />

其中首位的www/@称为主机记录，主机记录就是域名前缀，官方提供用法如下：

> **www：**解析后的域名为www.aliyun.com。
>
> **@：**直接解析主域名 aliyun.com。
>
> ***：**泛解析，匹配其他所有域名 *.aliyun.com。

可以根据自己的需要进行配置



在阿里云配置完成后需要在GitHub Pages 继续设置，来到`Settings`->`Pages`

在Custom domain中填写你购买的域名地址保存，并勾选`Enforce HTTPS`

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210516001200.png" alt="image-20210515141135901" style="zoom:67%;" />

接下来就是等待约5-10分钟，等待DNS同步完成后即可通过新的域名访问你的博客啦~