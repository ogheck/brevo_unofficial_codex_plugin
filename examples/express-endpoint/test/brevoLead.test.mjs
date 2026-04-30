import assert from "node:assert/strict";
import { test } from "node:test";

import { createBrevoLeadHandler } from "../src/brevoLead.js";

function mockReq({ method = "POST", body = {}, headers = {} } = {}) {
  return {
    method,
    body,
    headers,
    get(name) {
      return headers[name.toLowerCase()];
    },
  };
}

function mockRes() {
  return {
    statusCode: 200,
    headers: {},
    body: undefined,
    ended: false,
    status(code) {
      this.statusCode = code;
      return this;
    },
    set(name, value) {
      this.headers[name.toLowerCase()] = value;
      return this;
    },
    json(value) {
      this.body = value;
      return this;
    },
    end() {
      this.ended = true;
      return this;
    },
  };
}

test("rejects invalid email without calling Brevo", async () => {
  let calls = 0;
  const handler = createBrevoLeadHandler({
    env: { BREVO_API_KEY: "test-key", BREVO_LIST_IDS: "12" },
    fetchImpl: async () => {
      calls += 1;
      return Response.json({});
    },
  });

  const res = mockRes();
  await handler(mockReq({ body: { email: "bad-email" } }), res);

  assert.equal(res.statusCode, 400);
  assert.deepEqual(res.body, { ok: false, message: "Enter a valid email address." });
  assert.equal(calls, 0);
});

test("accepts honeypot submissions without calling Brevo", async () => {
  let calls = 0;
  const handler = createBrevoLeadHandler({
    env: { BREVO_API_KEY: "test-key", BREVO_LIST_IDS: "12" },
    fetchImpl: async () => {
      calls += 1;
      return Response.json({});
    },
  });

  const res = mockRes();
  await handler(mockReq({ body: { email: "person@example.com", company: "bot" } }), res);

  assert.equal(res.statusCode, 200);
  assert.deepEqual(res.body, { ok: true });
  assert.equal(calls, 0);
});

test("creates a Brevo contact", async () => {
  const calls = [];
  const handler = createBrevoLeadHandler({
    env: {
      BREVO_API_KEY: "test-key",
      BREVO_LIST_IDS: "12,34",
      ALLOWED_ORIGINS: "https://example.com",
    },
    fetchImpl: async (url, init) => {
      calls.push({ url, init });
      return new Response(null, { status: 201 });
    },
  });

  const res = mockRes();
  await handler(
    mockReq({
      body: {
        email: " PERSON@EXAMPLE.COM ",
        firstName: "Person",
      },
      headers: { origin: "https://example.com" },
    }),
    res,
  );

  assert.equal(res.statusCode, 200);
  assert.equal(res.headers["access-control-allow-origin"], "https://example.com");
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
  const handler = createBrevoLeadHandler({
    env: { BREVO_API_KEY: "test-key", BREVO_LIST_IDS: "12" },
    fetchImpl: async (url, init) => {
      calls.push({ url, init });
      if (calls.length === 1) {
        return Response.json({ code: "duplicate_parameter" }, { status: 400 });
      }
      return new Response(null, { status: 204 });
    },
  });

  const res = mockRes();
  await handler(mockReq({ body: { email: "person@example.com", source: "express" } }), res);

  assert.equal(res.statusCode, 200);
  assert.equal(calls.length, 2);
  assert.equal(calls[1].url, "https://api.brevo.com/v3/contacts/person%40example.com");
  assert.equal(calls[1].init.method, "PUT");
  assert.deepEqual(JSON.parse(calls[1].init.body), {
    attributes: {
      SOURCE: "express",
    },
    listIds: [12],
  });
});
