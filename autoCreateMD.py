# coding=utf-8
# 自动生成一个md格式文件，并在开头添加头部文件
'''
---
layout: post
title:  Jekyll 语法简单笔记
date:   2019-02-24 17:08:00 +0800
categories: jekyll
tag: jekyll使用相关
---
* content
{:toc}
'''
 
import os, sys
import time
import re
 
class Create_newMD:
    def __init__(self):
        self.contentlist = ["---"]
        # 日期格式规则
        self.date_patt = re.compile(r'\d{4}-\d{2}-\d{2}')
        # 时间格式规则
        self.time_patt = re.compile(r'\d{2}:\d{2}:\d{2}')
        # 存储所有文件的分类名
        self.categories_list = []
        # 存储所有文件的分类名
        self.tags_list = []
 
    def create(self):
        self.path = "./_posts"
        if (not os.path.exists(self.path)):
            print("当前目录下没有'_posts'文件夹，请核实，5秒后自动退出系统！")
            time.sleep(5)
            sys.exit()
        else:
            # 先获取_posts目录下的所有文件
            filelist = os.listdir(self.path)
            for file in filelist:
                with open(self.path+"/"+file,'r',encoding='utf-8')as f:
                    # 不用死循环，如果找20行还没找到就不用找了
                    switch = 0
                    while switch <= 20:
                        content = f.readline()
                        # 获取分类
                        if "categories: " in content:
                            category_ = content.split("categories: ")[1].strip().replace("\n","")
                            self.categories_list.append(category_)
                        # 获取标签
                        if "tag: " in content:
                            tag_ = content.split("tag: ")[1].strip().replace("\n","")
                            self.tags_list.append(tag_)
                        # else:
                            # 如果到了结尾就停止循环，这样太耗内存，一般20行以内就能确定分类和标签
                        #     if not content:
                        #         break
                        switch += 1
            all_categories = list(set(self.categories_list)) # 去掉重复的名字，并排序
            all_categories.sort()
            all_tags = list(set(self.tags_list))
            all_tags.sort()
 
            while True:
                input_date = input("\n" + "文章发布日期(格式2019-02-21,不输入默认为当前日期):").strip()
                re_date = self.date_patt.findall(input_date)
                if input_date != '':
                    if len(re_date) != 0:
                        break
                    else:
                        print("\n" + "发布日期格式有误，请重新输入！")
                        continue
                else:
                    break
            while True:
                input_time = input("\n" + "文章发布时间(格式07:08:00,不输入默认为当前时间):").strip()
                re_time = self.time_patt.findall(input_time)
                if input_time != '':
                    if len(re_time) != 0:
                        break
                    else:
                        print("\n" + "发布时间格式有误，请重新输入！")
                        continue
                else:
                    break
            while True:
                # 标题不能含特殊符号，否则博客js报错：Syntax error, unrecognized expression
                input_title = input("\n" + "文章标题:").strip()
                if input_title != "":
                    title = "title: " + input_title.replace("(","（").replace(")","）").replace(",","，").\
                    replace("[","【").replace("]","】").replace("/","_").replace("%","_").replace("#","_").\
                    replace("<", "《").replace(">", "》").replace("&", "_").replace("'", '"').replace("`", "_"). \
                    replace("^", "_").replace("@", "_").replace("$", "_").replace("!", "！").replace("?", "？").replace(";", "；")
                    # 结尾不能是英文冒号
                    if title[-1] == ":":
                        title = title.rsplit(":",1)[0] + "："
                    break
                else:
                    print("\n" + "标题不能为空或只为空格，请重新输入！")
                    continue
            print("===========已添加过的分类名如下===========")
            print("{:^15}\t{:^10}".format("分类代号", "分类名称"))
            categories_dic = {}
            for i, chr in enumerate(all_categories):
                print("{:^18}\t{:^12}".format(str(i + 1) + "-", chr))
                categories_dic[str(i + 1) + "-"] = chr
            while True:
                input_category = input("\n" + "输入文章分类名(可输入相应分类代号，注意后面的减号):").strip()
                if input_category != "":
                    # 如果输入的是纯数字，要加上双引号:"2"
                    if input_category.isdigit():
                        category = "categories: " + '"' + input_category + '"'
                    elif input_category in categories_dic.keys():
                        category = "categories: " + categories_dic[input_category]
                    else:
                        category = "categories: " + input_category
                    break
                else:
                    print("\n" + "分类名不能为空或只为空格，请重新输入！")
                    continue
            print("分类名为：%s"%category.split("categories: ")[1])
 
            print("\n" + "===========已添加过的标签名如下===========")
            print("{:^15}\t{:^10}".format("标签代号", "标签名称"))
            tags_dic = {}
            for j, chr in enumerate(all_tags):
                print("{:^18}\t{:^12}".format(str(j + 1) + "-", chr))
                tags_dic[str(j + 1) + "-"] = chr
            input_tag = input("\n" + "输入文章标签名(不输入默认为分类名或输入相应标签代号，注意后面的减号):").strip()
            if input_tag != "":
                if input_tag in tags_dic.keys():
                    tag = "tag: " + tags_dic[input_tag]
                else:
                    tag = "tag: " + input_tag
            else:
                if input_category.isdigit():
                    tag = "tag: " + input_category
                else:
                    tag = "tag: " + category.split("categories: ")[1]
            print("标签名为：%s" % tag.split("tag: ")[1])
 
            # 获取当天的日期
            today_date = time.strftime("%Y-%m-%d", time.localtime())
            # 获取现在的时间
            today_time = time.strftime("%H:%M:%S", time.localtime())
            if input_date == "":
                input_date = today_date
            if input_time == "":
                input_time = today_time
            date = "date: " + input_date + " " + input_time + " +0800"
            layout = "layout: post"
            self.contentlist.append(layout)
            self.contentlist.append(title)
            self.contentlist.append(date)
            self.contentlist.append(category)
            self.contentlist.append(tag)
            self.contentlist.append("---")
            self.contentlist.append("")
            self.contentlist.append("* content")
            self.contentlist.append("{:toc}")
            self.contentlist.append("导言：")
            self.contentlist.append("")
            # 这里多写一个注释将日期、时间和图片尺寸组合成图片的名字，方便传图的时候用到
            # <!-- ![]({{ '/styles/article-image/20190301153016_1.jpg' | prepend: site.baseurl  }}) -->
            # before = "<!-- ![]({{ '/styles/article-image/"
            # after = input_date.replace("-","") + input_time.replace(":","")+"_1.jpg' | prepend: site.baseurl }}){:height='80%' width='80%'} -->"
            self.contentlist.append("<!-- ![](https://latex.codecogs.com/gif.latex?) -->")
            char_list = ['*','|',':','?','/','<','>','"','\\']
            while True:
                # 创建文件的时候，名字不能包含一些特殊字符要转义
                url = input("\n" + "md文件名(也是文章url地址名称,不输入默认为标题名字(特殊符号用_代替)):").strip()
                if url == "":
                    url = input_title
                for i in char_list:
                    if i in url :
                        print("'%s'包含特殊符号'%s'已转义！"%(url,i))
                        url = url.replace(i,"_")
                fileName = input_date + "-" + url + ".md"
                if fileName in filelist:
                    print("\n" + "ERROR:该md文件'%s'已存在,创建失败！" % fileName)
                    while True:
                        choice = input("\n" + "输入相应数字(1:重新输入,0:退出系统)：")
                        if choice == '1':
                            break
                        elif choice == '0':
                            print("\n" + "5秒后自动退出系统，谢谢使用！")
                            time.sleep(5)
                            sys.exit()
                        else:
                            print("\n" + "请正确输入相应数字代码！")
                            continue
                else:
                    with open(self.path + "/" + fileName, "a+", encoding="utf-8")as f:
                        for i in self.contentlist:
                            f.write(i + "\n")
                    print("\n" + '恭喜文件已生成,请在文件夹“_posts”中查看，文件名为:“%s”' % fileName)
                    print("\n" + "5秒后自动退出系统...")
                    time.sleep(5)
                    break
if __name__ == "__main__":
    cr = Create_newMD()
    cr.create()
