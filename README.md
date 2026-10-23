# AppTool public resources

所有 App 自有远程静态配置和文件的唯一仓库。应用源码保留在私有仓库；新 App 直接新增 `apps/<app-slug>/`，不要再建独立内容仓库。slug 必须跨项目唯一，发布后不改名。

| 目录 | App | 来源 |
|---|---|---|
| apps/kids-learning-park | 宝宝早教乐园 | clover-content main；内容包数量以清单为准 |
| apps/webclean | WebClean | webclean-rules 已签名线上快照与 RulesSource |
| apps/leafread | 青页小说 | 应用内置完整 voices.json 与试听文件；原官方远程地址 404 |
| apps/sparks | 悸动 | couplegames-content main；原客户端当前没有远程下载入口，资源归档待后续版本接入 |

## 获取与更新

- Base URL: `https://raw.githubusercontent.com/zhongaiyemaozi/app-resources/main/`
- 清单使用 main；不可变内容使用 tag 或 commit。首批内容 tag：`resources-v1`，禁止移动或重写此 tag。后续内容更新用新 tag，最后更新 main 清单。
- CDN 只代理本仓库，如 `https://fastly.jsdelivr.net/gh/zhongaiyemaozi/app-resources@resources-v1/apps/kids-learning-park/packs/<id>.json`。
- 宝宝早教生成器：`CONTENT_REF=<新tag> python3 apps/kids-learning-park/Scripts/build_manifest.py`；先核对包体、版本、大小、SHA-256，再发布 tag 和 main 清单。
- WebClean 保留原 Ed25519 公钥和签名，不能直接编辑已签名 envelope。新 payload 必须用原私钥重新签名，脚本在 apps/webclean/scripts/；私钥原来只在旧仓库 Actions secret，本次无法读取 GitHub secret，也未复制私钥。离线或在可信签名环境生成后提交，本仓 CI 只验签，不依赖私钥。
- 只允许有权公开的静态数据；不得提交用户数据、凭证、私钥或内部源码。保留各资源许可：WebClean Proprietary；LeafRead 的许可随 voices.json 每条记录保留；宝宝早教和悸动延续原仓库资源许可，不附加开源授权。
- 提交前运行 `python3 scripts/verify_resources.py`；CI 同样校验包体哈希、大小和 WebClean 签名。

## 兼容与范围

旧 clover-content、couplegames-content、webclean-rules 仓库保留供已安装版本访问；本次不删除或归档旧入口。新客户端更新后才会切换。本仓为后续自有静态内容唯一维护位置；需要照顾旧客户端时从本仓同步兼容快照。

第三方实时 API（如汇率、Apple 查询）、SkillForge 用户 GitHub 搜索和自定义源、WebClean 用户主动订阅的第三方过滤源不属于自有静态托管，继续使用其原始服务以保留更新和许可语义。商店支持/隐私网站 app-sum 保持原址。

悸动原 manifest.checksums 与部分加密 .bin 的传输哈希不一致，迁移保留原字节和原业务校验值；transport-sha256.json 单独记录迁移文件哈希。当前客户端无下载入口，未宣称解密/业务校验通过。

青页小说三个超过 100MB 的语音模型原样托管在本仓 resources-v1 Release（名称保持原文件名），不加入 Git 历史。来源为 k2-fsa/sherpa-onnx 的 tts-models Release；源地址及许可在 apps/leafread/model-provenance.json。上传前核对清单已有字节数与 SHA-256，保留模型包内许可证。
