"""Local-only example: paged scan results and row actions; no media is modified."""
from mt_plugin import Plugin as BasePlugin, Context, SDKError, action, query, ui


class Plugin(BasePlugin):
    def get_page(self, ctx: Context):
        return ui.page(
            ui.Text(text="生成演示结果后，按页读取；行内操作仅标记结果，不删除文件。"),
            ui.Button(label="生成 120 组演示结果", onClick=[
                {"type": "set", "path": "state.cursor", "value": ""},
                {"type": "invoke", "actionId": "scan", "input": {"count": 120}},
            ]),
            ui.Text(text=ui.ref("query.summary.data.message")),
            ui.Table(source=ui.ref("query.summary.data.groups"), rowKey="id", pageSize=20, columns=[
                {"label": "作品名称", "field": "name", "cells": []},
                {"label": "已标记保留", "field": "kept", "cells": []},
                {"label": "操作", "cells": [ui.Button(
                    label="标记保留", size="sm", variant="outline", onClick=[
                        {"type": "invoke", "actionId": "decide", "input": {"id": ui.ref("row.id")}},
                    ])]},
            ]),
            ui.Button(label="下一页", disabled=ui.expr("not", ui.ref("query.summary.data.nextCursor")), onClick=[
                {"type": "set", "path": "state.cursor", "value": ui.ref("query.summary.data.nextCursor")},
            ]),
            ui.Button(label="回到首页并刷新", onClick=[
                {"type": "set", "path": "state.cursor", "value": ""},
                {"type": "query", "queryId": "summary"},
            ]),
            state={"cursor": ""},
            queries=[{"id": "summary", "name": "summary", "input": {"cursor": ui.ref("state.cursor")}}],
        )

    @action("scan")
    def scan(self, input: dict, ctx: Context):
        scan_id = ctx.run_id
        prefix = f"scans/{scan_id}/groups/"
        summary_key = f"scans/{scan_id}/summary"
        # Keep this pointer tiny. Queries can show running/failed without loading all rows.
        ctx.mt.storage.set(key=summary_key, value={"status": "running", "count": 0})
        ctx.mt.storage.set(key="currentScan", value=scan_id)
        count = 0
        try:
            for index in range(input["count"]):
                key = prefix + f"{index:06d}"
                ctx.mt.storage.set(key=key, expected_revision="", value={
                    "id": key, "name": f"演示作品 {index + 1}", "kept": False,
                    "versions": ["演示目录/版本A.strm", "演示目录/版本B.strm"],
                })
                count += 1
            ctx.mt.storage.set(key=summary_key, value={"status": "done", "count": count})
            return {"scanId": scan_id, "count": count}
        except Exception:
            # Preserve rows already written and propagate the original failure.
            # Even if quota/cancellation prevents this marker, queries will never
            # label a still-running scan as a completed empty result.
            try:
                ctx.mt.storage.set(key=summary_key, value={"status": "failed", "count": count})
            except Exception:
                pass
            raise

    @query("summary")
    def summary(self, input: dict, ctx: Context):
        current = ctx.mt.storage.get(key="currentScan")
        if not current["found"]:
            return {"groups": [], "nextCursor": "", "message": "尚未生成结果"}
        scan_id = current["value"]
        summary = ctx.mt.storage.get(key=f"scans/{scan_id}/summary")["value"]
        prefix = f"scans/{scan_id}/groups/"
        cursor = input.get("cursor", "")
        if cursor and not cursor.startswith(prefix):
            cursor = ""  # A newer scan invalidates the previous scan's page cursor.
        page = ctx.mt.storage.list(prefix=prefix, cursor=cursor, limit=20, values=True)
        status = summary["status"]
        message = {"done": f"完成：共 {summary['count']} 组", "running": "尚未完成，请检查运行状态", "failed": "生成失败，保留部分结果，请查看运行日志"}[status]
        return {"groups": [entry["value"] for entry in page["items"]],
                "nextCursor": page.get("nextCursor", ""), "message": message}

    @action("decide")
    def decide(self, input: dict, ctx: Context):
        key = input["id"]
        current = ctx.mt.storage.get(key="currentScan")
        prefix = f"scans/{current.get('value', '')}/groups/"
        if not current["found"] or not key.startswith(prefix):
            raise SDKError("结果已更新，请刷新后重试", "CONFLICT")
        entry = ctx.mt.storage.get(key=key)
        if not entry["found"]:
            raise SDKError("结果不存在，请刷新后重试", "NOT_FOUND")
        value = {**entry["value"], "kept": True}
        ctx.mt.storage.set(key=key, value=value, expected_revision=entry["revision"])
        return {"id": key, "kept": True}
