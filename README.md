# smzdm
抓取“什么值得买”海淘专区的信息，并存储在mongodb中

待更新：
  1. 扩展信息结构
  2. url的解析和遍历
  3. 内容页的信息获取

requests的响应式工作流

response = requsets.get('http://www.baidu.com', stream=True)
默认情况下,当发送网络请求时, 响应体会直接下载. 可以通过修改 stream 的值来覆盖这个行为, 直到访问 Response.content .
当使用 stream=True 时, 仅有 response 的 headers 被下载下来,连接连接一直是保持打开状态, 因此可以通过一些条件来决定是否下载响应体,
可以通过 Response.close  或者  Response.content 关闭连接

link:http://docs.python-requests.org/zh_CN/latest/user/advanced.html#body-content-workflow
