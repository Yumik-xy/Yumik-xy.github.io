---
layout: post
title: Android基础知识 Fragment
date: 2021-05-21 19:22:21 +0800
categories: Android
tag: Android
---

* content
{:toc}
Google的 [Frgament](https://developer.android.google.cn/guide/fragments) 学习笔记

### Frgament简介

Fragment是界面中可以重复使用的一部分，其可以独立管理自己的布局，拥有自己的生命周期，处理独立的输入信息……但是Fragment不能独立存在，必须依托于Activity或处在另一个Fragment中

Fragment可以很方便的进行模块化开发，通过模块间的不同布局方式以适应不同的设备，例如Google给出的版本图例

<img src="https://developer.android.google.cn/images/guide/fragments/fragment-screen-sizes.png" style="zoom:67%;" />

我们可以在Activity的生命周期中监测屏幕的状态变化或设备大小，以调整使用不同的Fragment或调整组件的布局方式

### 创建Fragment

由于Fragment存在一些隐形Bug因此Google在androidx中提供了新的Fragment承载器「androidx.fragment.app.FragmentContainerView」

#### 直接添加的方法

类似于先前的「fragment」，FragmentContainerView同样拥有静态绑定Fragment的方法

```xml
<!-- res/layout/example_activity.xml -->
<androidx.fragment.app.FragmentContainerView
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/fragment_container_view"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:name="com.example.ExampleFragment" />
```

其中「android:name="com.example.ExampleFragment"」为实例化的关键，必须指定对应的类名称（即对应的fragment的管理类）

#### 动态添加的方法

相较于先前的「Fragment」，FragmentContainerView动态绑定则无需为其分配对应的类名

```xml
<!-- res/layout/example_activity.xml -->
<androidx.fragment.app.FragmentContainerView
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/fragment_container_view"
    android:layout_width="match_parent"
    android:layout_height="match_parent" />
```

而是在Activity类实例中对其进行动态的绑定，可以通过获取FragmentManager对Fragment进行动态的添加，替换，移除

### Fragment管理器

FragmentManager类负责管理Fragment的一系列操作，即上述所说的动态的添加、替换和移除，其管理着Fragment的返回堆栈

#### FragmentManager的获取

无论是在Activity或是Fragment中都可以获取到FragmentManager，因为Fragment可以生存在Activity和另一个Fragment中，其获取方式如下：

- 在Activity中：使用「getSupportFragmentManager()」进行获取
- 在Fragment中：使用「getChildFragmentManager()」进行获取
- 若是被创建的Fragment想要获取创建它的管理器：使用「getParentFragmentManager()」进行获取

下图清晰的阐明了Fragment于其管理器之间的关系

<img src="https://developer.android.google.cn/images/guide/fragments/manager-mappings.png" alt="FragmentManager获取示例" style="zoom:67%;" />

#### FragmentManager的使用

FragmentManager和Activity很像都是使用返回堆栈来管理Fragment的。

- 用户点击「返回」按钮或执行popBackStack()时，会进行出栈操作移除Fragment，若是栈空则会将返回指令顺次传递到Activity中
- 若执行addToBackStack()时，这会进行压栈操作，即添加Fragment

但是FragmentManager的所有操作都会通过FragmentTransaction作为一个基本单元进行提交，因此FragmentTransaction是FragmentManager执行的重要一环

