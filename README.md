# Design Render Skills · 用 Codex 做设计出图

36个功能 Skills，加1个工作台，覆盖室内、建筑、景观、鸟瞰、彩平、家具场景、图片处理和图像辅助建模。

每个 Skill 明确必要输入、修改范围、执行步骤、交付与验收要求，任务由 Codex 和使用者环境中可用且获授权的工具完成。

## 已验证到哪里

2026-10-28，36个功能各执行一个受控样本：**17项样本通过、17项部分通过、2项未通过**。本地图片脚本11项行为测试通过。样本通过只针对本例目标，不代表全部输入、功能分支或真实项目均已通过。

扩图、空房装修的画幅与结构保留仍有问题；家具和抠图存在细节缺口；放大样本仅为LANCZOS插值，三维样本仅为粗略参数化GLB。原始生成、补救合成和失败样本均保留在测试资料中。

- [实践文章：用 Codex 做设计出图，37 个 Skills 实践](docs/37-skills-practice.md)
- [逐功能测试结论](docs/validation/测试报告.md)
- [图文报告 HTML（下载仓库后在浏览器打开）](docs/validation/测试报告.html)

![室内与建筑渲染对照](docs/images/01-室内与建筑渲染对照.png)

## 安装

```bash
git clone https://github.com/liuqing0224/design-render-skills.git
cd design-render-skills
python3 install.py
python3 install.py --check
```

默认安装到`$CODEX_HOME/skills`；未设置`CODEX_HOME`时使用`~/.codex/skills`。遇到任一同名目标，安装器会在写入前停止。可用`--target <目录>`指定位置；`--check`只核对安装副本。

生成与编辑需要环境中实际可用且获授权的图像工具；这些文件不会提供模型服务或转移原机器的授权。执行本地放大、压缩与转线稿脚本前，安装Pillow：

```bash
python3 -m pip install -r requirements.txt
python3 tests/test_image_ops.py
```

## 使用

安装后，在新会话中调用具体Skill，或从工作台开始：

```text
使用 $design-workbench，处理这张客厅图。
只把指定墙面换成深灰石材，保留家具、门窗和相机。
指定区域外像素不变，输出另存PNG并检查差异和接缝。
```

```text
使用 $design-siteplan-colorize，为总平分区上色。
区分建筑、道路、绿地和水体，保留建筑轮廓、路网和标注。
```

```text
使用 $design-image-compress，无损压缩这些PNG。
尺寸和透明通道不变，报告前后字节数与像素核验结果。
```

## 功能索引

| 功能 | 调用名称 | 文件 |
|---|---|---|
| AI模型渲染 | `$design-model-render` | [SKILL.md](skills/design-model-render/SKILL.md) |
| 家装渲染 | `$design-home-render` | [SKILL.md](skills/design-home-render/SKILL.md) |
| 工装渲染 | `$design-commercial-render` | [SKILL.md](skills/design-commercial-render/SKILL.md) |
| AI洗图与图像细节提升 | `$design-image-enhance` | [SKILL.md](skills/design-image-enhance/SKILL.md) |
| 软装硬装替换 | `$design-replace-interior-elements` | [SKILL.md](skills/design-replace-interior-elements/SKILL.md) |
| 室内局部渲染 | `$design-interior-local-edit` | [SKILL.md](skills/design-interior-local-edit/SKILL.md) |
| AI材质替换 | `$design-material-replace` | [SKILL.md](skills/design-material-replace/SKILL.md) |
| 文生图 | `$design-text-to-image` | [SKILL.md](skills/design-text-to-image/SKILL.md) |
| 室内风格迁移 | `$design-interior-style-transfer` | [SKILL.md](skills/design-interior-style-transfer/SKILL.md) |
| 一键彩平图 | `$design-floorplan-colorize` | [SKILL.md](skills/design-floorplan-colorize/SKILL.md) |
| 毛坯装修 | `$design-empty-room-furnish` | [SKILL.md](skills/design-empty-room-furnish/SKILL.md) |
| 建筑渲染 | `$design-building-render` | [SKILL.md](skills/design-building-render/SKILL.md) |
| 室外局部渲染 | `$design-exterior-local-edit` | [SKILL.md](skills/design-exterior-local-edit/SKILL.md) |
| 人物模特添加 | `$design-add-people` | [SKILL.md](skills/design-add-people/SKILL.md) |
| AI环境替换 | `$design-environment-replace` | [SKILL.md](skills/design-environment-replace/SKILL.md) |
| AI旧房改造 | `$design-facade-renovation` | [SKILL.md](skills/design-facade-renovation/SKILL.md) |
| 室外风格迁移 | `$design-exterior-style-transfer` | [SKILL.md](skills/design-exterior-style-transfer/SKILL.md) |
| 大鸟瞰渲染 | `$design-aerial-render` | [SKILL.md](skills/design-aerial-render/SKILL.md) |
| 总彩平渲染 | `$design-siteplan-colorize` | [SKILL.md](skills/design-siteplan-colorize/SKILL.md) |
| 景观渲染 | `$design-landscape-render` | [SKILL.md](skills/design-landscape-render/SKILL.md) |
| AI视角转换 | `$design-viewpoint-change` | [SKILL.md](skills/design-viewpoint-change/SKILL.md) |
| 氛围转换 | `$design-atmosphere-change` | [SKILL.md](skills/design-atmosphere-change/SKILL.md) |
| 建筑万物迁移 | `$design-exterior-object-transfer` | [SKILL.md](skills/design-exterior-object-transfer/SKILL.md) |
| 室内AI棚拍 | `$design-furniture-studio` | [SKILL.md](skills/design-furniture-studio/SKILL.md) |
| 室外AI场景 | `$design-furniture-outdoor` | [SKILL.md](skills/design-furniture-outdoor/SKILL.md) |
| 家具替换 | `$design-furniture-replace` | [SKILL.md](skills/design-furniture-replace/SKILL.md) |
| 一键抠图 | `$design-image-cutout` | [SKILL.md](skills/design-image-cutout/SKILL.md) |
| 拼图美化 | `$design-collage-beautify` | [SKILL.md](skills/design-collage-beautify/SKILL.md) |
| AI图转3D | `$design-image-to-3d` | [SKILL.md](skills/design-image-to-3d/SKILL.md) |
| 图片转提示词 | `$design-image-to-prompt` | [SKILL.md](skills/design-image-to-prompt/SKILL.md) |
| 提示词扩词 | `$design-prompt-expand` | [SKILL.md](skills/design-prompt-expand/SKILL.md) |
| 清晰度放大 | `$design-image-upscale` | [SKILL.md](skills/design-image-upscale/SKILL.md) |
| 无损压缩 | `$design-image-compress` | [SKILL.md](skills/design-image-compress/SKILL.md) |
| 智能扩图 | `$design-image-outpaint` | [SKILL.md](skills/design-image-outpaint/SKILL.md) |
| 图片转线稿 | `$design-image-to-lineart` | [SKILL.md](skills/design-image-to-lineart/SKILL.md) |
| 物体移除 | `$design-object-remove` | [SKILL.md](skills/design-object-remove/SKILL.md) |

调度入口：[设计表现工作台](skills/design-workbench/SKILL.md)。


## 发布副本说明

公开版把原机器专用的图像工具替代命令改为条件式说明；37个Skill统一使用`design-`前缀，调度入口为`design-workbench`；功能流程及处理脚本保持。原始素材为测试生成或人工绘制，不含真实客户项目。发布副本的安装器和本地脚本已单独验证；2026-10-29更新名称、文档和引用时未重新生成图像，原有限样本结论继续适用。
