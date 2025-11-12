const express = require("express");
const path = require("path");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

app.post("/api/mock", (req, res) => {
  const input = req.body || {};
  res.json({
    status: "ok",
    source: "glue-backend-mock",
    receivedInput: input,
    recommendation: "This is a MOCK response. Later this will call IBM / AI.",
    timestamp: new Date().toISOString()
  });
});

app.listen(PORT, () => {
  console.log(`Glue backend + UI running at http://localhost:${PORT}`);
});
