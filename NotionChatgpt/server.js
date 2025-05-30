import express from "express";
import axios from "axios";
import "dotenv/config";

const app = express();
const headers = {
  Authorization: `Bearer ${process.env.NOTION_TOKEN}`,
  "Notion-Version": "2022-06-28",
};

// ① キーワードで Notion を検索
app.get("/search", async (req, res) => {
  try {
    const q = req.query.q;
    const r = await axios.post(
      "https://api.notion.com/v1/search",
      { query: q, page_size: 5 },
      { headers }
    );
    const pages = r.data.results
      .filter((x) => x.object === "page")
      .map((p) => ({
        id: p.id,
        title:
          p.properties?.Name?.title?.[0]?.plain_text ||
          p.properties?.Title?.title?.[0]?.plain_text ||
          "Untitled",
      }));
    res.json({ pages });
  } catch (e) {
    res.status(500).send(e.message);
  }
});

// ② ページ本文を取得（段落だけ抜粋）
app.get("/page/:id", async (req, res) => {
  try {
    const id = req.params.id;
    const r = await axios.get(
      `https://api.notion.com/v1/blocks/${id}/children?page_size=100`,
      { headers }
    );
    const text = r.data.results
      .filter((b) => b.type === "paragraph")
      .map((b) =>
        b.paragraph.text.map((t) => t.plain_text).join("")
      )
      .join("\n");
    res.send(text.slice(0, 16000)); // GPT の入力上限対策
  } catch (e) {
    res.status(500).send(e.message);
  }
});

app.listen(process.env.PORT, () =>
  console.log(`Proxy running on :${process.env.PORT}`)
);
