import assert from "node:assert/strict";
import { afterEach, beforeEach, test } from "node:test";

import { OPTIONS, POST } from "../app/api/brevo-lead/route.js";

const originalEnv = { ...process.env };
const originalFetch = globalThis.fetch;

beforeEach(() => {
  process.env.BREVO_API_KEY = "test-key";
  process.env.BREVO_LIST_IDS = "12";
  delete process.env.ALLOWED_ORIGINS;
});

afterEach(() => {
  process.env = { ...originalEnv };
  globalThis.fetch = originalFetch;
});

function request(body) {
  return new Request("https://example.com/api/brevo-lead", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      origin: "https://example.com",
    },
    body: JSON.stringify(body),
  });
}

test("rejects invalid email without calling Brevo", async () => {
  let calls = 0;
  globalThis.fetch = async () => {
    calls += 1;
    return Response.json({});
  };

  const response = await POST(request({ email: "invalid" }));

  assert.equal(response.status, 400);
  assert.equal(calls, 0);
});

test("returns CORS headers for allowed origins", async () => {
  process.env.ALLOWED_ORIGINS = "https://example.com";

  const response = await OPTIONS(
    new Request("https://example.com/api/brevo-lead", {
      method: "OPTIONS",
      headers: { origin: "https://example.com" },
    }),
  );

  assert.equal(response.status, 204);
  assert.equal(response.headers.get("access-control-allow-origin"), "https://example.com");
});

test("creates a Brevo contact", async () => {
  process.env.BREVO_LIST_IDS = "12,34";
  const calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init });
    return new Response(null, { status: 201 });
  };

  const response = await POST(
    request({
      email: " PERSON@EXAMPLE.COM ",
      firstName: "Person",
      message: "More info",
    }),
  );

  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { ok: true });
  assert.deepEqual(JSON.parse(calls[0].init.body), {
    email: "person@example.com",
    attributes: {
      FIRSTNAME: "Person",
      MESSAGE: "More info",
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

  const response = await POST(request({ email: "person@example.com", lastName: "Customer" }));

  assert.equal(response.status, 200);
  assert.equal(calls.length, 2);
  assert.equal(calls[1].url, "https://api.brevo.com/v3/contacts/person%40example.com");
  assert.equal(calls[1].init.method, "PUT");
  assert.deepEqual(JSON.parse(calls[1].init.body), {
    attributes: {
      LASTNAME: "Customer",
    },
    listIds: [12],
  });
});
