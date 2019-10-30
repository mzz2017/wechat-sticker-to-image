# wechat-sticker-to-image

一个基于[ItChat](https://github.com/littlecodersh/ItChat)的微信个人账号机器人，将用户发送来的图片、表情包以文件形式发送回去。

显然，它适合那些微信表情包很多而其他社交软件表情包很少的人。

## 为什么不基于公众号

公众号的接口虽说有官方背景，但无法识别用户的表情包，所以无法实现功能。

## 如何使用

建议在生产环境下配合docker-compose使用：

```bash
docker-compose up
```

docker-compose还有其他常见用法，请自行查阅文档。

## 风险

ItChat基于微信网页版，网页版接口不稳定，且有被封号的概率 [ItChat#420](https://github.com/littlecodersh/ItChat/issues/420#)。