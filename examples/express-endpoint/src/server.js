import express from "express";

import { createBrevoLeadHandler } from "./brevoLead.js";

const app = express();
const port = Number.parseInt(process.env.PORT || "3000", 10);

app.use(express.json({ limit: "32kb" }));
app.all("/api/brevo-lead", createBrevoLeadHandler());

app.listen(port, () => {
  console.log(`Brevo lead capture example listening on http://localhost:${port}`);
});
