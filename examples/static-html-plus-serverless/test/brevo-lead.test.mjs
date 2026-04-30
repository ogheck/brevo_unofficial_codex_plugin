import assert from "node:assert/strict";
import { afterEach, test } from "node:test";

import { handleBrevoLeadRequest } from "../api/brevo-lead.mjs";

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
});

function request(body, method = "POST") {
  return new Request("https://example.com/api/brevo-lead", {
    method,
    headers: {
      "content-type": "application/json",
      origin: "https://example.com",
    },
    body: method === "POST" ? JSON.stringify(body) : undefined,
  });
}

test("rejects invalid email without calling Brevo", async () => {
  let calls = 0;
  globalThis.fetch = async () => {
    calls += 1;
    return Response.json({});
  };

  const response = await handleBrevoLeadRequest(
    request({ email: "invalid" }),
    { BREVO_API_KEY: "test-key", BREVO_LIST_IDS: "12" },
  );

  assert.equal(response.status, 400);
  assert.deepEqual(await response.json(), {
    ok: false,
    message: "Enter a valid email address.",
  });
  assert.equal(calls, 0);
});

test("accepts honeypot submissions without calling Brevo", async () => {
  let calls = 0;
  globalThis.fetch = async () => {
    calls += 1;
    return Response.json({});
  };

  const response = await handleBrevoLeadRequest(
    request({ email: "person@example.com", company: "bot" }),
    { BREVO_API_KEY: "test-key", BREVO_LIST_IDS: "12" },
  );

  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { ok: true });
  assert.equal(calls, 0);
});

test("creates a Brevo contact with normalized email", async () => {
  const calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init });
    return new Response(null, { status: 201 });
  };

  const response = await handleBrevoLeadRequest(
    request({ email: " PERSON@EXAMPLE.COM ", firstName: "Person" }),
    {
      BREVO_API_KEY: "test-key",
      BREVO_LIST_IDS: "12,34",
      ALLOWED_ORIGINS: "https://example.com",
    },
  );

  assert.equal(response.status, 200);
  assert.equal(response.headers.get("access-control-allow-origin"), "https://example.com");
  assert.deepEqual(JSON.parse(calls[0].init.body), {
    email: "person@example.com",
    attributes: {
      FIRSTNAME: "Person",
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

  const response = await handleBrevoLeadRequest(
    request({ email: "person@example.com", lastName: "Customer" }),
    { BREVO_API_KEY: "test-key", BREVO_LIST_IDS: "12" },
  );

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
