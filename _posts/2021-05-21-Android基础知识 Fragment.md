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

<img src="https://developer.android.google.cn/images/guide/fragments/fragment-screen-sizes.png" style="zoom:40%;" />

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

<img src="https://developer.android.google.cn/images/guide/fragments/manager-mappings.png" alt="FragmentManager获取示例" style="zoom: 40%;" />

#### FragmentManager的使用

FragmentManager和Activity很像都是使用返回堆栈来管理Fragment的。

- 用户点击「返回」按钮或执行popBackStack()时，会进行出栈操作移除Fragment，若是栈空则会将返回指令顺次传递到Activity中
- 若执行addToBackStack()时，这会进行压栈操作，即添加Fragment

但是FragmentManager的所有操作都会通过FragmentTransaction作为一个基本单元进行提交，因此FragmentTransaction是FragmentManager执行的重要一环

### Fragment事务

#### fragmentTransaction的获取

```kotlin
val fragmentManager = ...
val fragmentTransaction = fragmentManager.beginTransaction()
```

事务transaction的最后一步一定是commit()，其表示已经将所有的操作都添加进了事务中。但是该操作并不意味着方法立即生效，而是会等待主线程的调度安排。如果需要使提交立即生效，必须使用commitNow()方法（但是该方法并不兼容addToBackStack）因此不建议使用

因此fragment-ktx提供了一个便捷的Lambda方法，该操作无需用户开启transaction，并且会自动完成提交操作（仅限于kotlin）

```kotlin
val fragmentManager = ...
fragmentManager.commit {
    // Add operations here
}
```

setReorderingAllowed(true)是允许重排的标志，如果配置了允许，则会在提交后帮助用户对返回栈的操作进行优化，重新调整出入栈顺序等。这也可能会与用户设定的顺序不符（也就是有可能影响popBackStack），但是可以优化过渡动画，提供更流畅的操作体验

```kotlin
fragmentManager.commit {
    setReorderingAllowed(true)
}
```

#### 添加和移除Fragment

- 添加Fragment使用**add()**方法：方法需要传递containerViewId。containerViewId即当前Activity的某个容器视图的id，如果这个id传递值为0，则这个Fragment不会被添加到任何一个容器中，但是这个Fragment依旧是被添加进来了，这个Fragment可以作为类似Service的后台工作
- 移除Fragment使用**remove()**方法：方法需要通过findFragmentById()或findFragmentByTag()方法来获取添加进去的FragmentId。如果该Fragment被添加了，则逐次执行至onDestroy状态
- 替换Fragment使用**replace()**方法：可以将当前容器的Fragment替换为新的Fragment。该方法等效于remove()之前的Fragment，然后add()新的Fragment

*但任何通过FragmentTransaction进行的操作都不会加入到Fragment的返回堆栈中，如果需要添加需要使用addToBackStack()方法*

#### 显示和隐藏Fragment

可以通过show()和hide()方法显示和隐藏已经添加到容器的Fragment片段，这个方法不会影响Fragment的生命周期，因此也可以保持数据

妥善的使用该方法可以在多个Fragment之间切换时，提供更优的操作体验

### Fragment的生命周期

Fragment的生命周期和Activity的生命周期类似，都包含了onCreate()、onStart()、onResume()、onPause()、onStop()和onDestroy()

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210523134039.png" alt="fragment_lifecycle" style="zoom:80%;" />

下图给出了Fragment和View的生命周期状态

可以看到，在onCreated()时View并没有被创建，因此在这个阶段并不能进行任何的「视图操作」，而View的实际被创建是在onViewCreated()回调中，再次阶段才可以进行组件的操作



<img src="https://developer.android.google.cn/images/guide/fragments/fragment-view-lifecycle.png" alt="Fragment的生命周期" style="zoom:67%;" />

Fragment的生命周期一定不可能超过其父对象

- Host Fragment/Activity必须在Child Fragment之前开始生命周期回调：onCreate()、onStart()、onResume()
- Child Fragment必须在Host Fragment/Activity执行对应结束回调前结束：onPause()、onStop()、onDestroy()

其中还有两个回调状态，分别是onAttach()和onDetch()

+ 当一个Fragment被载入到指定的容器中，便会回调onAttach()
+ 当一个Fragment被从容器移除时，便会回调onDetch()



#### Fragment静态载入的生命周期

下面分别是使用androidx.fragment.app.FragmentContainerView和fragment得到的两种时间关系图，可以发现大部分回调顺序是一样的，只是FragmentContainerView的onViewCreated稍有区别

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210522150429.png!small" alt="image-20210522150428819" style="zoom:67%;" />

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210522162255.png!small" alt="image-20210522162255330" style="zoom:67%;" />

**以下内容Google并没有给出详细的文档说明，一切都为个人的理解方式**

1. Fragment的回调onCreate()在Activity之前

   如果从状态考虑，一定是Activity先进入onCreate状态，但是进入状态后并不意味着会立即产生回调，而是先载入对应的xml文件。因为上一篇博文中阐述了：

   > 那些只需要执行一次的「视图绑定」和「数据绑定」应该在这里执行

   博文中的这里指的是onCreate()的回调，其说明在这一阶段已经可以进行findByView()操作了，因此xml文件一定是在此基础上完成了加载

   **但是**这个阶段并不能通过Activity对Fragment的组件进行操作，上文已经写出组建的创建完成是在onViewCreated()回调中体现，而使用FragmentContainerView进行静态加载时onViewCreated()在Activity的onCreate之后进行*（如果是使用过时的fragment则可）*

2. Fragment的回调onStart()在Activity之前

   和(1)的理解类似，因为该阶段是对前台互动进行准备的阶段，其表示组件已经准备好可见。因此必须是其内部的组件都准备好要显示了，父组件才可以说自己准备好了，因此Fragment的早于Activity的

3. Fragment的回调onStart()在Activity之后

   这一点突然和之前的规律不一致了，这是因为这一步进行「可见」操作，只有载体组件先显示出来，才能显示子组件，否则子组件是无法显示的，因此Activity的必然要早于Fragment了

*至于fragment和新的FragmentContainerView出现些许不同，可能是Google为了更好分割使得Activity和Fragment之间更加的解耦合做出的改动？*

#### Fragment动态载入的生命周期

动态载入就没什么好说明的了，在任何阶段创建Fragment都会符合静态的生命周期规律

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210522152403.png!small" alt="image-20210522152402965" style="zoom:67%;" />

#### Fragment销毁的生命周期

<img src="https://yumik-xy.oss-cn-qingdao.aliyuncs.com/img/20210522155220.png!small" alt="image-20210522155220401" style="zoom:67%;" />
