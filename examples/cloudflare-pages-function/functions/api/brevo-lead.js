const BREVO_CONTACTS_URL = "https://api.brevo.com/v3/contacts";

function json(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      ...headers,
    },
  });
}

function corsHeaders(request, env) {
  const origin = request.headers.get("origin") || "";
  const allowed = (env.ALLOWED_ORIGINS || "")
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);

  if (!origin || allowed.length === 0 || !allowed.includes(origin)) {
    return {};
  }

  return {
    "access-control-allow-origin": origin,
    "access-control-allow-methods": "POST, OPTIONS",
    "access-control-allow-headers": "content-type",
    "vary": "origin",
  };
}

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

async function upsertBrevoContact(env, payload) {
  const headers = {
    "api-key": env.BREVO_API_KEY,
    "content-type": "application/json",
    accept: "application/json",
  };

  const create = await fetch(BREVO_CONTACTS_URL, {
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

  const update = await fetch(`${BREVO_CONTACTS_URL}/${encodeURIComponent(payload.email)}`, {
    method: "PUT",
    headers,
    body: JSON.stringify(updatePayload),
  });

  if (!update.ok && update.status !== 204) {
    throw new Error(`Brevo update contact failed: ${update.status}`);
  }
}

export async function onRequestOptions({ request, env }) {
  return new Response(null, {
    status: 204,
    headers: corsHeaders(request, env),
  });
}

export async function onRequestPost({ request, env }) {
  const cors = corsHeaders(request, env);

  if (!env.BREVO_API_KEY) {
    return json({ ok: false, message: "Lead capture is not configured." }, 500, cors);
  }

  const ids = listIds(env);
  if (ids.length === 0) {
    return json({ ok: false, message: "Lead capture is not configured." }, 500, cors);
  }

  let input;
  try {
    input = await request.json();
  } catch {
    return json({ ok: false, message: "Send valid JSON." }, 400, cors);
  }

  if (String(input.company || "").trim()) {
    return json({ ok: true }, 200, cors);
  }

  const email = normalizeEmail(input.email);
  if (!isValidEmail(email)) {
    return json({ ok: false, message: "Enter a valid email address." }, 400, cors);
  }

  try {
    await upsertBrevoContact(env, contactPayload({ ...input, email }, ids));
    return json({ ok: true }, 200, cors);
  } catch (error) {
    console.error(error instanceof Error ? error.message : error);
    return json({ ok: false, message: "We could not save that request. Try again later." }, 500, cors);
  }
}

export async function onRequest() {
  return json({ ok: false, message: "Method not allowed." }, 405);
}
