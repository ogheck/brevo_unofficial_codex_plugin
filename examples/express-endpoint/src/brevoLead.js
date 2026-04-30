const BREVO_CONTACTS_URL = "https://api.brevo.com/v3/contacts";

function normalizeEmail(value) {
  return String(value || "").trim().toLowerCase();
}

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function listIds(env) {
  return String(env.BREVO_LIST_IDS || "")
    .split(",")
    .map((value) => Number.parseInt(value.trim(), 10))
    .filter((value) => Number.isInteger(value) && value > 0);
}

function contactPayload(input, ids) {
  const attributes = {};

  if (input.firstName) attributes.FIRSTNAME = String(input.firstName).trim();
  if (input.lastName) attributes.LASTNAME = String(input.lastName).trim();
  if (input.phone) attributes.SMS = String(input.phone).trim();
  if (input.source) attributes.SOURCE = String(input.source).trim().slice(0, 120);
  if (input.message) attributes.MESSAGE = String(input.message).trim().slice(0, 1000);

  return {
    email: normalizeEmail(input.email),
    attributes,
    listIds: ids,
    updateEnabled: true,
  };
}

async function upsertBrevoContact({ env, fetchImpl, payload }) {
  const headers = {
    "api-key": env.BREVO_API_KEY,
    "content-type": "application/json",
    accept: "application/json",
  };

  const create = await fetchImpl(BREVO_CONTACTS_URL, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });

  if (create.ok || create.status === 204) {
    return;
  }

  let error = {};
  try {
    error = await create.json();
  } catch {
    error = {};
  }

  if (create.status !== 400 || error.code !== "duplicate_parameter") {
    throw new Error(`Brevo create contact failed: ${create.status}`);
  }

  const updatePayload = {
    attributes: payload.attributes,
    listIds: payload.listIds,
  };

  const update = await fetchImpl(`${BREVO_CONTACTS_URL}/${encodeURIComponent(payload.email)}`, {
    method: "PUT",
    headers,
    body: JSON.stringify(updatePayload),
  });

  if (!update.ok && update.status !== 204) {
    throw new Error(`Brevo update contact failed: ${update.status}`);
  }
}

function applyCors(req, res, env) {
  const origin = req.get?.("origin") || req.headers?.origin || "";
  const allowed = String(env.ALLOWED_ORIGINS || "")
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);

  if (!origin || allowed.length === 0 || !allowed.includes(origin)) {
    return;
  }

  res.set("access-control-allow-origin", origin);
  res.set("access-control-allow-methods", "POST, OPTIONS");
  res.set("access-control-allow-headers", "content-type");
  res.set("vary", "origin");
}

export function createBrevoLeadHandler(options = {}) {
  const env = options.env || process.env;
  const fetchImpl = options.fetchImpl || globalThis.fetch;

  return async function brevoLeadHandler(req, res) {
    applyCors(req, res, env);

    if (req.method === "OPTIONS") {
      return res.status(204).end();
    }

    if (req.method !== "POST") {
      return res.status(405).json({ ok: false, message: "Method not allowed." });
    }

    if (!env.BREVO_API_KEY) {
      return res.status(500).json({ ok: false, message: "Lead capture is not configured." });
    }

    const ids = listIds(env);
    if (ids.length === 0) {
      return res.status(500).json({ ok: false, message: "Lead capture is not configured." });
    }

    const input = req.body || {};

    if (String(input.company || "").trim()) {
      return res.status(200).json({ ok: true });
    }

    const email = normalizeEmail(input.email);
    if (!isValidEmail(email)) {
      return res.status(400).json({ ok: false, message: "Enter a valid email address." });
    }

    try {
      await upsertBrevoContact({
        env,
        fetchImpl,
        payload: contactPayload({ ...input, email }, ids),
      });
      return res.status(200).json({ ok: true });
    } catch (error) {
      console.error(error instanceof Error ? error.message : error);
      return res.status(500).json({
        ok: false,
        message: "We could not save that request. Try again later.",
      });
    }
  };
}
