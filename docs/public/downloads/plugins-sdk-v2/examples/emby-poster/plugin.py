from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageDraw, ImageFont, ImageOps
from mt_plugin import Context, Plugin as BasePlugin, action, query, ui


class Plugin(BasePlugin):
    def get_page(self, ctx: Context):
        servers = ctx.mt.emby.servers.list()
        return ui.page(
            ui.Card(
                ui.Text(text="下载条目主图，合成为 1920×1080 预览。上传将替换该条目的主图，请核对目标 ID。"),
                ui.Select(label="已授权 Emby 服务器", bind="state.serverId", options=[
                    {"label": server["name"], "value": server["id"]} for server in servers
                ]),
                ui.Input(label="媒体库或条目 ID", bind="state.itemId"),
                ui.Input(label="海报文字（示例使用默认字体）", bind="state.caption"),
                ui.Button(label="下载并生成预览", onClick=[{
                    "type": "invoke", "actionId": "prepare", "input": {
                        "serverId": ui.ref("state.serverId"), "itemId": ui.ref("state.itemId"),
                        "caption": ui.ref("state.caption"),
                    },
                }]),
            ),
            ui.Image(src=ui.ref("query.latest.data.preview"), alt="生成的海报"),
            ui.Text(text=ui.ref("query.latest.data.target")),
            ui.Button(label="将预览图上传并替换目标主图", onClick=[{"type": "invoke", "actionId": "upload"}]),
            ui.RunLog(),
            state={"serverId": "", "itemId": "", "caption": "MediaTidy"},
            queries=[{"id": "latest", "name": "latest"}],
        )

    @action("prepare")
    def prepare(self, input: dict, ctx: Context):
        item_id = quote(input["itemId"], safe="")
        result = ctx.mt.emby.request(
            server_id=input["serverId"], path=f"/Items/{item_id}/Images/Primary", response_type="file",
        )
        if result["status"] != 200 or not result.get("file"):
            raise ValueError(f"素材下载未成功：HTTP {result['status']}")
        output = Path(ctx.work_dir) / "poster.jpg"
        with Image.open(result["file"]["path"]) as source:
            poster = ImageOps.fit(source.convert("RGB"), (1920, 1080))
        draw = ImageDraw.Draw(poster)
        draw.rectangle((0, 880, 1920, 1080), fill=(16, 24, 32))
        draw.text((80, 940), input["caption"], fill="white", font=ImageFont.load_default(size=64))
        poster.save(output, "JPEG", quality=90)
        artifact = ctx.mt.artifacts.publish(path=str(output))
        latest = {"artifact": artifact, "serverId": input["serverId"], "itemId": input["itemId"]}
        ctx.mt.storage.set(key="latest", value=latest)
        return latest

    @query("latest")
    def latest(self, input: dict, ctx: Context):
        latest = ctx.mt.storage.get(key="latest").get("value")
        if not latest:
            return {"preview": "", "target": "请先生成预览图"}
        return {"preview": "file:" + latest["artifact"]["ref"],
                "target": f"目标：{latest['serverId']} / {latest['itemId']}；有效至 {latest['artifact']['expiresAt']}"}

    @action("upload")
    def upload(self, input: dict, ctx: Context):
        latest = ctx.mt.storage.get(key="latest").get("value")
        if not latest:
            raise ValueError("请先生成并检查预览图")
        artifact = latest["artifact"]
        result = ctx.mt.emby.request(
            server_id=latest["serverId"], method="POST",
            path=f"/Items/{quote(latest['itemId'], safe='')}/Images/Primary",
            body_ref=artifact["ref"], body_encoding="base64", content_type=artifact["contentType"],
        )
        if not 200 <= result["status"] < 300:
            raise ValueError(f"上传未成功：HTTP {result['status']}")
        ctx.mt.log(level="info", message="Emby 已接受预览图上传，请在 Emby 中查看目标主图")
        return {"status": result["status"], "itemId": latest["itemId"]}
