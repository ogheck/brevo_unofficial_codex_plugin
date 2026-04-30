import assert from "node:assert/strict";
import { afterEach, test } from "node:test";

import { onRequestPost } from "../functions/api/brevo-lead.js";

const originalFetch = globalThis.fetch;

afterEach(() => {
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

async function responseJson(response) {
  return response.json();
}

test("rejects invalid email without calling Brevo", async () => {
  let calls = 0;
  globalThis.fetch = async () => {
    calls += 1;
    return Response.json({});
  };

  const response = await onRequestPost({
    request: request({ email: "not-an-email" }),
    env: {
      BREVO_API_KEY: "test-key",
      BREVO_LIST_IDS: "12",
    },
  });

  assert.equal(response.status, 400);
  assert.deepEqual(await responseJson(response), {
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

  const response = await onRequestPost({
    request: request({
      email: "person@example.com",
      company: "Filled by bot",
    }),
    env: {
      BREVO_API_KEY: "test-key",
      BREVO_LIST_IDS: "12",
    },
  });

  assert.equal(response.status, 200);
  assert.deepEqual(await responseJson(response), { ok: true });
  assert.equal(calls, 0);
});

test("creates a Brevo contact with normalized email and list ids", async () => {
  const calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init });
    return new Response(null, { status: 201 });
  };

  const response = await onRequestPost({
    request: request({
      email: " PERSON@EXAMPLE.COM ",
      firstName: "Person",
      source: "landing-page",
    }),
    env: {
      BREVO_API_KEY: "test-key",
      BREVO_LIST_IDS: "12, 34",
      ALLOWED_ORIGINS: "https://example.com",
    },
  });

  assert.equal(response.status, 200);
  assert.deepEqual(await responseJson(response), { ok: true });
  assert.equal(calls.length, 1);
  assert.equal(calls[0].url, "https://api.brevo.com/v3/contacts");
  assert.equal(calls[0].init.method, "POST");
  assert.equal(calls[0].init.headers["api-key"], "test-key");
  assert.deepEqual(JSON.parse(calls[0].init.body), {
    email: "person@example.com",
    attributes: {
      FIRSTNAME: "Person",
      SOURCE: "landing-page",
    },
    listIds: [12, 34],
    updateEnabled: true,
  });
});

test("updates an existing Brevo contact when create returns duplicate", async () => {
  const calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init });
    if (calls.length === 1) {
      return Response.json({ code: "duplicate_parameter" }, { status: 400 });
    }
    return new Response(null, { status: 204 });
  };

  const response = await onRequestPost({
    request: request({
      email: "person@example.com",
      lastName: "Customer",
    }),
    env: {
      BREVO_API_KEY: "test-key",
      BREVO_LIST_IDS: "12",
    },
  });

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
