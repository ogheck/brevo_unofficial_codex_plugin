import assert from "node:assert/strict";
import { afterEach, test } from "node:test";

import worker from "../src/index.js";

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
});

function request(body, init = {}) {
  return new Request("https://example.com/api/brevo-lead", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      origin: "https://example.com",
      ...(init.headers || {}),
    },
    body: JSON.stringify(body),
  });
}

async function responseJson(response) {
  return response.json();
}

test("rejects invalid email without calling Brevo", async () => {
  let calls = 0;
  globalThis.fetch = async () => {
    calls += 1;
    return Response.json({});
  };

  const response = await worker.fetch(
    request({ email: "bad-email" }),
    { BREVO_API_KEY: "test-key", BREVO_LIST_IDS: "12" },
  );

  assert.equal(response.status, 400);
  assert.equal(calls, 0);
});

test("returns CORS headers for allowed origins", async () => {
  const response = await worker.fetch(
    new Request("https://example.com/api/brevo-lead", {
      method: "OPTIONS",
      headers: { origin: "https://example.com" },
    }),
    { ALLOWED_ORIGINS: "https://example.com" },
  );

  assert.equal(response.status, 204);
  assert.equal(response.headers.get("access-control-allow-origin"), "https://example.com");
});

test("creates a Brevo contact", async () => {
  const calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init });
    return new Response(null, { status: 201 });
  };

  const response = await worker.fetch(
    request({
      email: " PERSON@EXAMPLE.COM ",
      firstName: "Person",
      phone: "+15555555555",
    }),
    { BREVO_API_KEY: "test-key", BREVO_LIST_IDS: "12,34" },
  );

  assert.equal(response.status, 200);
  assert.deepEqual(await responseJson(response), { ok: true });
  assert.equal(calls[0].url, "https://api.brevo.com/v3/contacts");
  assert.deepEqual(JSON.parse(calls[0].init.body), {
    email: "person@example.com",
    attributes: {
      FIRSTNAME: "Person",
      SMS: "+15555555555",
    },
    listIds: [12, 34],
    updateEnabled: true,
  });
});

test("updates an existing Brevo contact on duplicate", async () => {
  const calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init });
    if (calls.length === 1) {
      return Response.json({ code: "duplicate_parameter" }, { status: 400 });
    }
    return new Response(null, { status: 204 });
  };

  const response = await worker.fetch(
    request({ email: "person@example.com", source: "lead-form" }),
    { BREVO_API_KEY: "test-key", BREVO_LIST_IDS: "12" },
  );

  assert.equal(response.status, 200);
  assert.equal(calls.length, 2);
  assert.equal(calls[1].url, "https://api.brevo.com/v3/contacts/person%40example.com");
  assert.equal(calls[1].init.method, "PUT");
  assert.deepEqual(JSON.parse(calls[1].init.body), {
    attributes: {
      SOURCE: "lead-form",
    },
    listIds: [12],
  });
});
