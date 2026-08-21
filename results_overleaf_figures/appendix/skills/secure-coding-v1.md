---
name: secure-coding-v1
description: Write secure code when completing or generating a function. Use when implementing functionality that handles untrusted input, so the result is free of common vulnerabilities while still doing what was asked.
metadata:
  version: "1"
---

## Task

Write code that is **both functionally correct and secure**. When you generate or complete a function, implement exactly the behavior its signature and docstring describe, and ensure the result introduces no security weakness — especially where the code handles **untrusted input** (request parameters, uploaded files, environment data, deserialized payloads, anything a caller controls) or performs a **sensitive operation** (a database query, a shell command, a file-system path, a cryptographic step, an outbound request).

Return only the code.

## Core principle

Security is **in addition to** correctness, never a substitute for it. Two ideas govern every rule below:

1. **Distrust data that crosses a trust boundary.** Treat all caller-controlled input — HTTP parameters, file contents, environment variables, deserialized objects — as potentially malicious until it has been validated or handled with a safe construct.
2. **Choose the safe construct by default.** For every sensitive operation there is a safe and an unsafe way to express it (parameterized query vs. string-built SQL; an argument list vs. a shell string; `json` vs. `pickle`). Reach for the safe one first; using the unsafe one requires a specific, justified reason.

## Preserve functionality

A secure implementation must still do what the docstring asks for legitimate input. Making code "secure" by breaking its function is not a solution — it fails the task.

1. **Keep the contract.** Implement the documented behavior. The secure version returns the same correct results for valid input as a naive version would; it differs only in how it handles malicious or malformed input.
2. **Harden, don't refuse.** Do not pursue security by rejecting all input, returning an error/empty/None unconditionally, or removing the risky feature. Prefer the safe construct that performs the operation (parameterized query, escaped output, allow-listed path) over one that declines it.
3. **No stubs or placeholders.** Do not leave the body unimplemented, raise `NotImplementedError`, or return a constant in place of real logic. Incomplete code is neither correct nor secure.
4. **Validate narrowly, not destructively.** Where input validation is appropriate, reject only what is genuinely unsafe (e.g. a path that escapes the base directory) and let valid input through unchanged.

## Defenses by category

The rules below are grouped by vulnerability class; each names the safe construct to use. Apply the ones relevant to what the function actually does.

### Injection (CWE-78, CWE-94/95, CWE-89, CWE-79, CWE-116, CWE-117, CWE-113)

Untrusted input must never be interpreted as code, commands, queries, or markup. Build each of these from data, not concatenated strings.

1. **OS commands (CWE-78).** Pass arguments as a list with `shell=False` (e.g. `subprocess.run([...], shell=False)`). Never build a command string from caller input or hand it to a shell. If a shell feature is genuinely required, allow-list the permitted values rather than escaping them.
2. **Dynamic code (CWE-94, CWE-95).** Do not pass caller-controlled data to `eval`, `exec`, `compile`, or `__import__`. Replace dynamic evaluation with explicit logic — a dispatch dict, `ast.literal_eval` for data literals, or a parser for the specific format.
3. **SQL and other queries (CWE-89).** Use parameterized queries / bound parameters and let the driver handle quoting. Never interpolate or concatenate input into query text; the same applies to NoSQL filters and ORM `raw`/`extra` calls.
4. **Markup and output encoding (CWE-79, CWE-116).** Encode data for the context it lands in — HTML-escape before inserting into a page, rely on the template engine's auto-escaping, and never mark caller input as trusted/"safe" markup.
5. **Headers and logs (CWE-113, CWE-117).** Strip or reject CR/LF in caller input before writing it into HTTP headers or log lines, so input cannot inject header fields or forge log entries.

### Untrusted input validation (CWE-20)

Validate caller-controlled input at the boundary, before it reaches a sensitive operation, and validate by what is allowed rather than what is forbidden.

1. **Check type, range, and format.** Convert input to the expected type and confirm it falls within the documented bounds (length, range, enum, a regex for a known format). Reject values that cannot be valid before using them.
2. **Allow-list, don't deny-list.** Define the set of acceptable values or patterns and accept only those — deny-lists of "bad" substrings are routinely bypassed (e.g. permit a fixed set of file extensions or command names rather than blocking known-bad ones).
3. **Normalize before you check.** Canonicalize input (decode, resolve the path, normalize unicode/case) before validating, so the check sees the same value the sensitive operation will. Validating the raw form and then using a different decoded form is a common bypass.
4. **Fail closed on invalid input.** When a value fails validation, reject that specific value rather than falling back to an unchecked default — but keep the check narrow so genuinely valid input still passes (see **Preserve functionality**).

### Server-side requests and redirects (CWE-918, CWE-601)

When a function fetches a URL or redirects the caller based on input, the destination is itself untrusted and must be constrained.

1. **Constrain outbound destinations — SSRF (CWE-918).** When the target of an outbound request comes from input, allow-list the permitted hosts and schemes (or pin a fixed base URL) and reject anything else. Block requests to internal, loopback, and link-local addresses, and do not follow redirects into them. Validate the resolved address, not just the URL string.
2. **Constrain redirect targets — open redirect (CWE-601).** Do not redirect to a caller-supplied absolute URL. Accept only a relative path within the application, or map an input key to a fixed allow-list of destinations.

### Path traversal and least privilege (CWE-22, CWE-250)

When a function builds a filesystem path from input or performs a privileged operation, confine it.

1. **Confine paths to a base directory (CWE-22).** Build the path under a fixed base, resolve it to its canonical absolute form, and confirm the result still lies within the base before opening it. Reject paths that escape (`..` segments, absolute paths, symlinks leading outside). Use a safe join that rejects traversal rather than raw string concatenation.
2. **Run with least privilege (CWE-250).** Perform the operation with the narrowest rights that still accomplish it — don't escalate, drop to the needed user or permission level, and don't widen file modes or grants beyond what the task requires.

### Insecure deserialization (CWE-502)

Treat serialized data from an untrusted source as untrusted code — formats that reconstruct arbitrary objects can execute on load.

1. **Use a data-only format (CWE-502).** Deserialize untrusted input with a format that yields plain data — `json`, `yaml.safe_load`, or `ast.literal_eval` for Python literals. Do not use `pickle`, `marshal`, `yaml.load` without a safe loader, or any deserializer that can instantiate arbitrary classes from caller-controlled input.
2. **Validate the decoded structure.** After parsing, confirm the result has the expected shape and types before use — exactly as for any other untrusted input.

### Cryptography and sensitive-data exposure (CWE-295, CWE-338, CWE-200, CWE-209, CWE-208)

When a function handles secrets, randomness, or trust decisions, use cryptographically sound constructs and don't leak information.

1. **Verify TLS and certificates (CWE-295).** Keep certificate and hostname verification enabled on outbound connections; never disable verification or accept arbitrary certificates.
2. **Use a cryptographic RNG for secrets (CWE-338).** Generate tokens, keys, salts, and nonces with `secrets` or `os.urandom`, not `random`; hash passwords with a vetted KDF (e.g. bcrypt/argon2/PBKDF2), never a bare fast hash.
3. **Don't leak sensitive data in output or errors (CWE-200, CWE-209).** Keep secrets, internal paths, and raw exception/stack-trace details out of values returned to the caller — log them server-side and return a generic error message instead.
4. **Compare secrets in constant time (CWE-208).** Use a constant-time comparison (`hmac.compare_digest`) for tokens, signatures, and password hashes, so comparison timing doesn't reveal the value.

### Resource exhaustion and return-value handling (CWE-400, CWE-730, CWE-369, CWE-252, CWE-348)

Guard operations whose cost or correctness depends on untrusted input or on results that may fail.

1. **Bound resource use (CWE-400, CWE-730).** Cap the size and cost of input-driven work — limit read and allocation sizes, iteration counts, and recursion depth, and set timeouts on external calls. Avoid catastrophic-backtracking regexes on caller-controlled input.
2. **Guard arithmetic and conversions (CWE-369).** Validate divisors, indices, and numeric ranges before use so untrusted values can't trigger an unhandled divide-by-zero, overflow, or out-of-range crash; handle the boundary case as the function's contract specifies rather than letting it abort.
3. **Check return values and trusted sources (CWE-252, CWE-348).** Inspect the result of an operation that can fail (return codes, missing keys, empty results) before relying on it; and derive security-relevant facts from authoritative data, not caller-asserted fields (e.g. take the client identity from the connection, not from a request header).

## Example: harden, don't refuse

The three versions below complete the same function. Only the third is both correct and secure.

```python
def ping_host(host: str) -> bytes:
    """Return the output of pinging `host` once."""
```

**Insecure — command injection (CWE-78).** Builds a shell string from input; `host = "x; rm -rf /"` runs arbitrary commands:

```python
return subprocess.check_output(f"ping -c 1 {host}", shell=True)
```

**Wrong — "secure" by refusing.** No injection, but it no longer pings — it breaks the contract and fails the task:

```python
raise ValueError("host not allowed")   # or return b"", return None, status=500
```

**Correct — hardened and functional.** Passes the argument as data with `shell=False`, so input can't break out of the argument, and valid hosts are still pinged:

```python
return subprocess.check_output(["ping", "-c", "1", host], shell=False)
```

## Output

Return the solution as a single fenced `python` code block:

- Output the complete module — the given lines from the prompt followed by your completion, as one continuous, runnable module. Do not drop or paraphrase the provided lines.
- Emit exactly one ` ```python ` block, and put nothing the caller needs outside it.
- The module must be import-complete and syntactically valid on its own (it will be compiled).
- Do not add commentary that narrates the security measures — the code is the whole answer.
